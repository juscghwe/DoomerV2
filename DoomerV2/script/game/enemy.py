'''
Code based on:
    Copyright (c) 2004-2020, Lode Vandevenne

    All rights reserved.

    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

        * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
        * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
    A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
    CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
Translated to Python and adjusted by:
Julian Schweizer
'''

import pygame
import math
import numpy as np
import script.general.loader as ld
from SETTINGS import SETTINGS

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_tupple):
        pygame.sprite.Sprite.__init__(self)
        self.pos = self.pos_x, self.pos_y = pos_tupple
        self.__still_img = ld.loadimage(SETTINGS.FOLDER, "images/gameobjects","enemy.png")
        self.__left_img = ld.loadimage(SETTINGS.FOLDER, "images/gameobjects","enemyleft.png")
        self.__right_img = ld.loadimage(SETTINGS.FOLDER, "images/gameobjects","enemyright.png")
        self.__shot_img1 = ld.loadimage(SETTINGS.FOLDER, "images/gameobjects","enemyshot1.png")
        self.__shot_img2 = ld.loadimage(SETTINGS.FOLDER, "images/gameobjects","enemyshot2.png")
        self.__shot_img3 = ld.loadimage(SETTINGS.FOLDER, "images/gameobjects","enemyshot3.png")
        self.__death_img = ld.loadimage(SETTINGS.FOLDER, "images/gameobjects","enemydeath.png")
        self.__DISPLAY_WIDTH, self.__DISPLAY_HEIGHT = SETTINGS.SIZE
        self.__img = self.__still_img
        self.__rect = self.__img.get_rect()
        self.__rect.center = (self.pos_x, self.pos_y)
        self.sprite_width, self.__sprite_height = 64, 64
        self.health = SETTINGS.ENEMY_START_HEALTH
        self.__death_timer = SETTINGS.ENEMY_DEATH_TIMER * SETTINGS.FPS
        self.__death_counter = 0
        self.dead = False
        self.__shooting = False
        self.__shoot_timer = 0

    def update(self,player_pos_tupple, player_dir_tupple, plane_tupple, dist_buffer):
        self.__attrs=(player_pos_tupple, player_dir_tupple, plane_tupple, dist_buffer)
        player_pos_x, player_pos_y = player_pos_tupple
        player_dir_x, player_dir_y = player_dir_tupple
        plane_x, plane_y = plane_tupple
        self.dist = ((player_pos_x - self.pos_x) * (player_pos_x - self.pos_x) + (player_pos_y - self.pos_y) * (player_pos_y - self.pos_y))
        tex_width = SETTINGS.TEX_WIDTH
        w, h = SETTINGS.SIZE
        self.visible = False
        ''' Position relative to Camera '''
        sprite_x = self.pos_x - player_pos_x
        sprite_y = self.pos_y - player_pos_y
        ''' Inverse camera Matrix '''
        invDet = 1.0 / (plane_x * player_dir_y - player_dir_x * plane_y)
        transform_x = invDet * (player_dir_y * sprite_x - player_dir_x * sprite_y)
        transform_y = invDet * (-plane_y * sprite_x + plane_x * sprite_y)
        if transform_y != 0: 
            sprite_screen_x = int((w / 2) * (1 + transform_x / transform_y))
            self.__sprite_height = abs(int(h / (transform_y)))
            self.sprite_width = abs(int(h / (transform_y)))
        else: 
            sprite_screen_x = 0
            self.__sprite_height = 0
            self.__sprite_width = 0
        ''' lowest and highest pixel to fill in current stripe '''
        self.__draw_start_y = int(-self.__sprite_height / 2 + h / 2)
        if self.__draw_start_y < 0: self.__draw_start_y = 0
        draw_end_y = int(self.__sprite_height / 2 + h / 2)
        if draw_end_y >= h: draw_end_y = h - 1
        self.__draw_start_x = int(-self.sprite_width / 2 + sprite_screen_x)
        self.center = self.__draw_start_x + self.sprite_width / 2
        if self.__draw_start_x < 0: self.__draw_start_x = 0
        draw_end_x = int(self.sprite_width / 2 + sprite_screen_x)
        if draw_end_x >= w: draw_end_x = w - 1
        ''' stripe analysing '''
        self.__image_data = []
        #d = self.__draw_start_y * 256 - h*128 + self.__sprite_height*128
        #self.tex_y = ((d*tex_width)/self.__sprite_height)
        for stripe in range(self.__draw_start_x, draw_end_x):
            if transform_y > 0 and stripe > 0 and stripe < w and transform_y < dist_buffer[stripe]:
                self.__image_data.append(stripe)
                self.visible = True
        self.__image_data.sort()
        self.pos = self.pos_x, self.pos_y

    def render(self, true_fps):
        if true_fps == 0: true_fps = SETTINGS.FPS
        screen = pygame.display.get_surface()
        self.width = 0
        ''' sprite rendering '''
        if self.__death_counter >= 1:
            if self.__death_counter >= self.__deathtime:
                    self.dead = True
            self.__death_counter +=1
        if self.visible:
            if self.health <= 0 and self.__death_counter == 0:
                self.__deathtime = int(SETTINGS.ENEMY_DEATH_TIMER * true_fps)
                self.__img = self.__death_img
                self.__death_counter = 1
            left = self.__image_data[0] - self.__draw_start_x
            right = self.__image_data[-1] - self.__draw_start_x
            self.width = right - left
            self.sprite_width = min(self.sprite_width, self.__DISPLAY_WIDTH*3)
            self.__sprite_height = min(self.__sprite_height, self.__DISPLAY_HEIGHT*3)
            image = pygame.transform.scale(self.__img, (self.sprite_width, self.__sprite_height))
            if self.__draw_start_x == 0 and left == 1:
                ''' links aus dem Bildschirm '''
                screen.blit(image, (0, self.__draw_start_y), (self.sprite_width - right, 0, self.width, self.__sprite_height))
            else:
                # Fehler wenn bspw links am Bildschirm und teilverdeckt
                # Verschiebt Item nach rechts innerhalb der Box
                # Anders rum wahrscheinlich identisch
                screen.blit(image, (self.__draw_start_x + left, self.__draw_start_y), (left, 0, self.width, self.__sprite_height))

    def npc(self, player_object, true_fps):
        if true_fps == 0: true_fps = SETTINGS.FPS
        self.__shoottime = int(SETTINGS.ENEMY_SHOOT_TIME * true_fps)
        self.__cooldowntime = int(SETTINGS.ENEMY_COOLDOWN_TIME * true_fps)
        timer = self.__shoottime / 3
        if math.sqrt(self.dist) <= 3 and self.__shoot_timer == 0 and self.visible:
            self.__shoot_timer = 1
        if self.__shoot_timer >= 1:
            if self.__shoot_timer <= timer:
                self.__shooting == True
                self.__img = self.__shot_img1
            elif timer < self.__shoot_timer <= timer * 2:
                self.__img = self.__shot_img2
            elif timer * 2 < self.__shoot_timer < timer * 3:
                self.__img = self.__shot_img3
            elif self.__shoot_timer == timer * 3:
                self.projectile = self.Projectile(self.pos, player_object.pos, self.dist)
            elif self.__shoottime < self.__shoot_timer <= self.__shoottime + self.__cooldowntime:
                self.__img = self.__still_img
            elif self.__shoottime + self.__cooldowntime < self.__shoot_timer and self.projectile.shooting == False:
                self.__shoot_timer = 0
                self.projectile.kill()

            if self.__shoottime < self.__shoot_timer:
                self.projectile.draw(*self.__attrs)
                player_object = self.projectile.update(player_object)
            self.__shoot_timer += 1
        return player_object

    class Projectile(pygame.sprite.Sprite):
        def __init__(self, pos_tupple, player_pos, dist):
            pygame.sprite.Sprite.__init__(self)
            self.pos = self.pos_x, self.pos_y = pos_tupple
            self.__img = ld.loadimage(SETTINGS.FOLDER, "images/gameobjects", "fireball.png")
            self.__rect = self.__img.get_rect()
            self.__rect.center = (self.pos_x, self.pos_y)
            self.__sprite_width, self.__sprite_height = 64, 64
            self.__dir = self.__normalize(pos_tupple, player_pos)
            self.__DISPLAY_WIDTH, self.__DISPLAY_HEIGHT = SETTINGS.SIZE
            self.__movement_speed = 1
            self.__time = 0
            self.shooting = True
            self.dist = dist
            # scaling
            self.u_div = 1
            self.v_div = 1
            self.v_move = 64 * 1

        def __normalize(self, pos_tupple, player_pos):
            player_x, player_y = player_pos
            fire_x, fire_y = pos_tupple
            v = np.array([player_x - fire_x, player_y - fire_y])
            norm = np.linalg.norm(v)
            if norm == 0:
                return v
            return v / norm

        def draw(self,player_pos_tupple, player_dir_tupple, plane_tupple, dist_buffer):
            self.pos_x = self.pos[0] + self.__movement_speed * self.__dir[0]
            self.pos_y = self.pos[1] + self.__movement_speed * self.__dir[1]
            player_pos_x, player_pos_y = player_pos_tupple
            player_dir_x, player_dir_y = player_dir_tupple
            plane_x, plane_y = plane_tupple
            self.dist = ((player_pos_x - self.pos_x) * (player_pos_x - self.pos_x) + (player_pos_y - self.pos_y) * (player_pos_y - self.pos_y))
            tex_width = SETTINGS.TEX_WIDTH
            w, h = SETTINGS.SIZE
            self.visible = False
            ''' Position relative to Camera '''
            sprite_x = self.pos_x - player_pos_x
            sprite_y = self.pos_y - player_pos_y
            ''' Inverse camera Matrix '''
            invDet = 1.0 / (plane_x * player_dir_y - player_dir_x * plane_y)
            transform_x = invDet * (player_dir_y * sprite_x - player_dir_x * sprite_y)
            transform_y = invDet * (-plane_y * sprite_x + plane_x * sprite_y)
            sprite_screen_x = int((w / 2) * (1 + transform_x / transform_y))
            v_move_screen = int(self.v_move / transform_y)
            ''' calculate height of the sprite on screen '''
            self.__sprite_height = int(abs(h / (transform_y)) / self.v_div)
            ''' lowest and highest pixel to fill in current stripe '''
            self.__draw_start_y = int(-self.__sprite_height / 2 + h / 2 + v_move_screen)
            if self.__draw_start_y < 0: self.__draw_start_y = 0
            draw_end_y = int(self.__sprite_height / 2 + h / 2 + v_move_screen)
            if draw_end_y >= h: draw_end_y = h - 1
            ''' calculate width of the sprite '''
            self.__sprite_width = int(abs(h / (transform_y)) / self.u_div)
            self.__draw_start_x = int(-self.__sprite_width / 2 + sprite_screen_x)
            self.center = self.__draw_start_x + self.__sprite_width / 2
            if self.__draw_start_x < 0: self.__draw_start_x = 0
            draw_end_x = int(self.__sprite_width / 2 + sprite_screen_x)
            if draw_end_x >= w: draw_end_x = w - 1
            ''' stripe analysing '''
            self.__image_data = []
            for stripe in range(self.__draw_start_x, draw_end_x):
                if transform_y > 0 and stripe > 0 and stripe < w and transform_y < dist_buffer[stripe]:
                    self.__image_data.append(stripe)
                    self.visible = True
            self.__image_data.sort()
            self.pos = self.pos_x, self.pos_y
            ''' draw '''
            screen = pygame.display.get_surface()
            if self.visible:
                left = self.__image_data[0] - self.__draw_start_x
                right = self.__image_data[-1] - self.__draw_start_x
                self.__width = right - left
                self.__sprite_width = min(self.__sprite_width, self.__DISPLAY_WIDTH*2)
                self.__sprite_height = min(self.__sprite_height, self.__DISPLAY_HEIGHT*2)
                image = pygame.transform.scale(self.__img, (self.__sprite_width, self.__sprite_height))
                if self.__draw_start_x == 0 and left == 1:
                    screen.blit(image, (0, self.__draw_start_y), (self.__sprite_width - right, 0, self.__width, self.__sprite_height))
                else:
                    screen.blit(image, (self.__draw_start_x + left, self.__draw_start_y), (left, 0, self.__width, self.__sprite_height))

        def update(self, player):
            if self.__time >= 50:
                self.shooting = False
            if math.sqrt(self.dist) < 0.3:
                self.shooting = False
                player.incoming_hit(30)
            self.__time += 1
            return player
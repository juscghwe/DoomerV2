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

class Item(pygame.sprite.Sprite):
    def __init__(self, pos_tupple, value, scale, hight_shift):
        pygame.sprite.Sprite.__init__(self)
        self.pos = self.pos_x, self.pos_y = pos_tupple
        value_dict = SETTINGS.MAPITEMS
        self.__name = list(value_dict.keys())[list(value_dict.values()).index(value)]
        self.__img = ld.loadimage(SETTINGS.FOLDER, "images/gameobjects", self.__name+".png")
        self.__rect = self.__img.get_rect()
        self.__rect.center = (self.pos_x, self.pos_y)
        self.__sprite_width, self.__sprite_height = 64, 64
        self.dead = False
        # scaling
        self.u_div = scale
        self.v_div = scale
        self.v_move = 64*hight_shift

    def update(self,player_pos_tupple, player_dir_tupple, plane_tupple, dist_buffer):
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

    def pickup(self, player_instance, weapon_instance):
        ''' Nimmt Item bei Möglichkeit auf '''
        dist = math.sqrt(self.dist)
        if dist < 1:
            if self.__name == "health" and player_instance.health < 100:
                ''' Gesundheit aufnehmen '''
                player_instance.health = min(player_instance.health + player_instance.health_pickup, 100)
                self.dead = True
            elif self.__name == "armour" and player_instance.armor < 100:
                ''' Rüstung aufnehmen '''
                player_instance.armor = min(player_instance.armor + player_instance.armor_pickup, 100)
                self.dead = True
            elif self.__name == "shotgunshell" and weapon_instance.amo < weapon_instance.max_amo:
                ''' Munition aufnehmen '''
                weapon_instance.amo = min(weapon_instance.amo + weapon_instance.amo_pickup, weapon_instance.max_amo)
                weapon_instance.img = weapon_instance.weapon_img
                self.dead = True
        return player_instance, weapon_instance

    def render(self, fps):
        screen = pygame.display.get_surface()
        ''' sprite rendering '''
        if self.visible:
            left = self.__image_data[0] - self.__draw_start_x
            right = self.__image_data[-1] - self.__draw_start_x
            self.__width = right - left
            image = pygame.transform.scale(self.__img, (self.__sprite_width, self.__sprite_height))
            if self.__draw_start_x == 0 and left == 1:
                ''' links aus dem Bildschirm '''
                screen.blit(image, (0, self.__draw_start_y), (self.__sprite_width - right, 0, self.__width, self.__sprite_height))
            else:
                # Fehler wenn bspw links am Bildschirm und teilverdeckt
                # Verschiebt Item nach rechts innerhalb der Box
                # Anders rum wahrscheinlich identisch
                screen.blit(image, (self.__draw_start_x + left, self.__draw_start_y), (left, 0, self.__width, self.__sprite_height))
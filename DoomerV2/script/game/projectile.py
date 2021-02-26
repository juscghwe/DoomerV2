import pygame
import math
import numpy as np
from SETTINGS import SETTINGS
import script.general.loader as ld

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos_tupple, player_pos, dist, maparray):
        pygame.sprite.Sprite.__init__(self)
        self.pos = self.pos_x, self.pos_y = pos_tupple
        self.__img = ld.loadimage(SETTINGS.FOLDER, "images/gameobjects", "fireball.png")
        self.__rect = self.__img.get_rect()
        self.__rect.center = (self.pos_x, self.pos_y)
        self.__sprite_width, self.__sprite_height = 64, 64
        self.__maparray = maparray
        self.__maparray_fine = np.kron(maparray, np.ones((10,10)))
        self.__dir = self.__normalize(pos_tupple, player_pos)
        self.__DISPLAY_WIDTH, self.__DISPLAY_HEIGHT = SETTINGS.SIZE
        self.__movement_speed = SETTINGS.PROJECTILE_SPEED
        self.__time = 0
        self.dead = False
        self.visible = False
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

    def update(self,player_pos_tupple, player_dir_tupple, plane_tupple, dist_buffer):
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

    def render(self, true_fps):
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

    def attack(self, player):
        if 0 < self.__maparray[int(self.pos_x), int(self.pos_y)] <50:
            # Kollision
            self.dead = True
        if self.__time >= SETTINGS.PROJECTILE_DURATION:
            # Lebensdauer
            self.dead = True
        if math.sqrt(self.dist) < SETTINGS.PROJECTILE_MAX_DIST:
            # Treffer
            player.incoming_hit(30)
            self.dead = True
        self.__time += 1
        return player

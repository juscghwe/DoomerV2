#!/usr/bin/env python3
'''
Code based on:
    Raycasting Method by:
    Copyright (c) 2004-2019, Lode Vandevenne
    All rights reserved.
    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are
    met:
        * Redistributions of source code must retain the above copyright
        notice,
        this list of conditions and the following disclaimer.
        * Redistributions in binary form must reproduce the above copyright
        notice, this list of conditions and the following disclaimer in the
        documentation and/or other materials provided with the distribution.
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
    A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
    OWNER OR
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
from random import randint
from time   import time
from PIL import Image
from SETTINGS import SETTINGS
import time

class Camera(object):
    def __init__(self, maparray):
        #self.__SCREEN = pygame.display.get_surface()
        self.map = maparray
        self.__MAP_WIDTH = len(maparray)
        self.__MAP_HEIGHT = len(maparray[1])
        self.__FPS = SETTINGS.FPS
        self.__RGB_RED = (200, 0, 0)
        self.__RGB_GREEN = (0, 200, 0)
        self.__RGB_BLUE = (0, 0, 128)
        self.__RGB_WHITE = (255, 255, 255)
        self.__RGB_YELLOW = (255, 255, 0)
        self.__F_TIME = 1 / self.__FPS
        self.__DISPLAY_WIDTH, self.__DISPLAY_HEIGHT = SETTINGS.SIZE
        self.__TEX_WIDTH, self.__TEX_HEIGHT = SETTINGS.TEX_WIDTH, SETTINGS.TEX_HEIGHT
        self.pretimings = []
        self.posttimings = []
        self.__texture = SETTINGS.MAPITEMS
        ''' Texture Code '''
        self.textures = {
            self.__texture["wallbloodeye"]: [ld.loadimage(SETTINGS.FOLDER, "images/gameobjects/wallbloodeye", f"wallbloodeye{i}.png") for i in range(SETTINGS.TEX_WIDTH * 2)],
            self.__texture["wallbrick"]: [ld.loadimage(SETTINGS.FOLDER, "images/gameobjects/wallbrick", f"wallbrick{i}.png") for i in range(SETTINGS.TEX_WIDTH * 2)],
            self.__texture["wallcolumn"]: [ld.loadimage(SETTINGS.FOLDER, "images/gameobjects/wallcolumn", f"wallcolumn{i}.png") for i in range(SETTINGS.TEX_WIDTH * 2)],
            self.__texture["wallwhite"]: [ld.loadimage(SETTINGS.FOLDER, "images/gameobjects/wallwhite", f"wallwhite{i}.png") for i in range(SETTINGS.TEX_WIDTH * 2)]
            }

    def __minmax(self, n, maxn, minn=0):
        return max(min(maxn, n), minn)

    def update(self, player_pos, player_dir, player_plane):
        walls = []
        floor = []
        self.WallDistBuffer = [None] * self.__DISPLAY_WIDTH
        w = self.__DISPLAY_WIDTH
        h = self.__DISPLAY_HEIGHT
        x_pos, y_pos = player_pos
        x_dir, y_dir = player_dir
        plane_x, plane_y = player_plane
        tex_width = self.__TEX_WIDTH
        tex_height = self.__TEX_HEIGHT
        #x = 0
        #y = 0
        #''' Floor Casting '''
        #for y in range(h):
        #    ''' Äußerst rechter und linker Ray '''
        #    ray_dir_x0 = x_dir - plane_x
        #    ray_dir_y0 = y_dir - plane_y
        #    ray_dir_x1 = x_dir + plane_x
        #    ray_dir_y1 = y_dir + plane_y
        #    ''' y-Position im Verhältnis zum Horizont '''
        #    p = int(y - h / 2)
        #    ''' Vertikale Kameraposition'''
        #    z_pos = 0.5 * h
        #    row_dist = z_pos / p
        #    floor_step_x = row_dist * (ray_dir_x1 - ray_dir_x0) / w
        #    floor_step_y = row_dist * (ray_dir_y1 - ray_dir_y0) / w
        #    floor_x = pos_x + row_dist * ray_dir_x0
        #    floor_y = pos_y + row_dist * ray_dir_y0
        #    for x in range(w):
        #        cell_x = int(floor_x)
        #        cell_y = int(floor_y)
        #        ''' Texturkoordinaten '''
        #        tx = int(tex_width*(floor_x - cell_x))
        #        ty = int(tex_height*(floor_y - cell_y))
        #        floor_x += floor_step_x
        #        floor_y += floor_step_y
        #        floor.append([ty, (x, draw_start), (x, draw_end), tex_pos])

        ''' Wall Casting '''
        x = 0
        y = 0
        for x in range(w):
            ''' Ray Position und Richtung '''
            camera_x = 2 * x / w - 1
            ray_dir_x = x_dir + plane_x * camera_x
            ray_dir_y = y_dir + plane_y * camera_x

            ''' Mapposition auf Box '''
            map_x, map_y = int(x_pos), int(y_pos)

            ''' Ray-Länge in x/y-Richtung '''
            if ray_dir_x != 0:  delta_dist_x = abs(1 / ray_dir_x)
            else:               delta_dist_x = 0
            if ray_dir_y != 0:  delta_dist_y = abs(1 / ray_dir_y)
            else:               delta_dist_y = 0

            ''' Richtung und sideDist bestimmen '''
            if ray_dir_x < 0:
                step_x = -1
                side_dist_x = (x_pos - map_x) * delta_dist_x
            else:
                step_x = 1
                side_dist_x = (map_x + 1 - x_pos) * delta_dist_x
            if ray_dir_y < 0:
                step_y = -1
                side_dist_y = (y_pos - map_y) * delta_dist_y
            else:
                step_y = 1
                side_dist_y = (map_y + 1 - y_pos) * delta_dist_y

            ''' DDA '''
            hit = 0
            while hit == 0:
                if (side_dist_x < side_dist_y):
                    side_dist_x += delta_dist_x
                    map_x += step_x
                    side = 0
                else:
                    side_dist_y += delta_dist_y
                    map_y += step_y
                    side = 1
                if self.map[map_x][map_y] > 0 and self.map[map_x][map_y] < 50:
                    hit = 1

            ''' Abstand von geradem Ray '''
            if side == 0:
                if ray_dir_x != 0: perp_wall_dist = (map_x - x_pos + (1 - step_x) / 2) / ray_dir_x
                else: perp_wall_dist = 0
            else:
                if ray_dir_y != 0: perp_wall_dist = (map_y - y_pos + (1 - step_y) / 2) / ray_dir_y
                else: perp_wall_dist = 0

            ''' Höhe der Wand berechnen '''
            if perp_wall_dist != 0: line_height = int(h / perp_wall_dist)
            else: line_height = 0
            
            ''' Start und Ende des Wandstreifens '''
            draw_start = -1 * line_height / 2 + h / 2
            if draw_start < 0: draw_start = 0
            draw_end = line_height / 2 + h / 2
            if draw_end >= h: draw_end = h - 1

            #''' Farbe bestimmen '''
            #if self.map[map_x][map_y] == 1: color = self.__RGB_RED
            #elif self.map[map_x][map_y] == 2: color = self.__RGB_GREEN
            #elif self.map[map_x][map_y] == 3: color = self.__RGB_BLUE
            #elif self.map[map_x][map_y] == 4: color = self.__RGB_WHITE
            #elif self.map[map_x][map_y] == 5: color = self.__RGB_YELLOW
            #if side == 1: color = tuple(int(i / 2) for i in color)
            ''' Texturstreifen bestimmen '''
            tex_num = self.map[map_x][map_y]
            if side == 0:
                wall_x = y_pos + perp_wall_dist * ray_dir_y
            else:
                wall_x = x_pos + perp_wall_dist * ray_dir_x
            wall_x -= math.floor(wall_x)
            tex_x = int(wall_x * self.__TEX_WIDTH)
            if side == 0 and ray_dir_x > 0:
                tex_x = self.__TEX_WIDTH - tex_x - 1
            if side == 1 and ray_dir_y < 0:
                tex_x = self.__TEX_WIDTH - tex_x - 1
                tex_x += self.__TEX_WIDTH       # shift to dark
            tex_pos = int((draw_start - h / 2 + line_height / 2) * perp_wall_dist * self.__TEX_HEIGHT / h)
            # tex_pos in wall_pos umrechnen um negativwert zu berechnen

            ''' Zeichenliste anlegen '''
            walls.append([tex_num, tex_x, (x, draw_start), (x, draw_end), tex_pos, line_height])
            self.WallDistBuffer[x] = perp_wall_dist
            x+=1
        return walls

    def draw(self, walls, target_surface):
        ''' Zeichnet Wände und Boden aus Wallarray'''
        screen = pygame.display.get_surface()
        for i in walls:
            value = i[0]
            tex_name = list(self.__texture.keys())[list(self.__texture.values()).index(value)]
            stripe = i[1]
            top = i[2]
            bottom = i[3]
            tex_pos = i[4]
            size = i[5]
            img = self.textures[value][stripe]
            image = pygame.transform.scale(img, (1, size))
            if top[1]<=0:
                #Beheben: Texturen sind verdreht
                scale = tex_pos * size / self.__TEX_HEIGHT
                image = image.subsurface((0, scale, 1, size - scale))
            target_surface.blit(image, top)
            pygame.draw.line(target_surface, (105,105,105), bottom, (bottom[0], self.__DISPLAY_HEIGHT))
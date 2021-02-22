import pygame
import math
from script.general.text import Text
from SETTINGS import SETTINGS

class Player(object):
    def __init__(self, maparray):
        self.__SCREEN = pygame.display.get_surface()
        self.__DISPLAY_WIDTH, self.__DISPLAY_HEIGHT = self.__SCREEN.get_size()
        self.__hud = pygame.sprite.Group()
        ''' Stats '''
        self.health = SETTINGS.PLAYER_START_HEALTH
        self.armor = SETTINGS.PLAYER_START_ARMOR
        self.health_pickup = SETTINGS.HEALTH_PICKUP
        self.armor_pickup = SETTINGS.ARMOR_PICKUP
        self.death = False
        self.__movement_speed = SETTINGS.PLAYER_MOVE_SPEED
        self.__rotation_speed = SETTINGS.PLAYER_ROT_SPEED
        self.__straf_speed = SETTINGS.PLAYER_STRAF_SPEED
        ''' MapData '''
        self.__map = maparray
        self.pos = self.x_pos, self.y_pos = 22, 12
        self.dir = self.x_dir, self.y_dir = -1, 0
        self.plane = self.plane_x, self.plane_y = 0, 0.66

    def incoming_hit(self, damage):
        if damage <= self.armor:
            self.armor -= damage
        elif 0 < damage < self.armor:
            self.armor = 0
            self.health -= damage - self.armor
        else:
            if self.health < 20:
                self.health -= damage / 2
            else:
                self.health -= damage
            if self.health <= 0:
                self.death = True

    def update(self, target_surface, position, weaponstats):
        """weaponstats as tupplelist: Name as string, current load as int, total amo as int"""
        self.position = position
        self.__hud.empty()
        hud_health = Text(10,self.__DISPLAY_HEIGHT - 50, "Health: " + str(self.health), 20,(255,255,255))
        hud_armor = Text(10,self.__DISPLAY_HEIGHT - 25, "Armor: " + str(self.armor), 20,(255,255,255))
        self.__hud.add(hud_health, hud_armor)
        name, load, amo = weaponstats
        hud_weaponname = Text(self.__DISPLAY_WIDTH - 100, self.__DISPLAY_HEIGHT - 25, name + ":", 20, (255,255,255))
        hud_load = Text(self.__DISPLAY_WIDTH - 30, self.__DISPLAY_HEIGHT - 25, str(load), 20, (255,255,255))
        hud_amo = Text(self.__DISPLAY_WIDTH - 20, self.__DISPLAY_HEIGHT - 25, "/ " + str(amo), 20, (255,255,255))
        self.__hud.add(hud_weaponname, hud_load, hud_amo)
        for text in self.__hud:
            text.render_text(target_surface)

    def movement(self, realfps):
        if realfps == 0: realfps = SETTINGS.FPS
        move_speed = 1 / realfps * self.__movement_speed
        rot_speed = 1 / realfps * self.__rotation_speed
        straf_speed = 1 / realfps * self.__straf_speed
        
        if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]: 
            ''' Vor '''
            col_x = self.__map[int(self.x_pos + self.x_dir * move_speed)][int(self.y_pos)]
            col_y = self.__map[int(self.x_pos)][int(self.y_pos + self.y_dir * move_speed)]
            if col_x == 0 or col_x > 50:
                self.x_pos = self.x_pos + self.x_dir * move_speed
            if col_y == 0 or col_y > 50:
                self.y_pos = self.y_pos + self.y_dir * move_speed
        if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]: 
            ''' Zurück '''
            col_x = self.__map[int(self.x_pos - self.x_dir * move_speed)][int(self.y_pos)]
            col_y = self.__map[int(self.x_pos)][int(self.y_pos - self.y_dir * move_speed)]
            if col_x == 0 or col_x > 50:
                self.x_pos = self.x_pos - self.x_dir * move_speed
            if col_y == 0 or col_y > 50:
                self.y_pos = self.y_pos - self.y_dir * move_speed
        if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]: 
            ''' Links '''
            old_rotation = (self.x_dir, self.y_dir)
            self.__rotate(1)
            col_x = self.__map[int(self.x_pos + self.x_dir * straf_speed)][int(self.y_pos)]
            col_y = self.__map[int(self.x_pos)][int(self.y_pos + self.y_dir * straf_speed)]
            if col_x == 0 or col_x > 50:
                self.x_pos = self.x_pos + self.x_dir * straf_speed
            if col_y == 0 or col_y > 50:
                self.y_pos = self.y_pos + self.y_dir * straf_speed
            self.x_dir, self.y_dir = old_rotation
        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]: 
            ''' Rechts '''
            old_rotation = (self.x_dir, self.y_dir)
            self.__rotate(-1)
            col_x = self.__map[int(self.x_pos + self.x_dir * straf_speed)][int(self.y_pos)]
            col_y = self.__map[int(self.x_pos)][int(self.y_pos + self.y_dir * straf_speed)]
            if col_x == 0 or col_x > 50:
                self.x_pos = self.x_pos + self.x_dir * straf_speed
            if col_y == 0 or col_y > 50:
                self.y_pos = self.y_pos + self.y_dir * straf_speed
            self.x_dir, self.y_dir = old_rotation
        ''' Rotation '''
        rot_speed, delta_x = pygame.mouse.get_rel()
        rot_speed = -rot_speed / SETTINGS.MOUSE_SENSITIVITY     # EINBAUEN: Mausbeschleunigung, exponentielle Anpassung
        old_x_dir = self.x_dir
        self.x_dir = self.x_dir * math.cos(rot_speed) - self.y_dir * math.sin(rot_speed)
        self.y_dir = old_x_dir * math.sin(rot_speed) + self.y_dir * math.cos(rot_speed)
        old_plane_x = self.plane_x
        self.plane_x = self.plane_x * math.cos(rot_speed) - self.plane_y * math.sin(rot_speed)
        self.plane_y = old_plane_x * math.sin(rot_speed) + self.plane_y * math.cos(rot_speed)

        ''' Redeclaration '''
        self.pos = self.x_pos, self.y_pos
        self.dir = self.x_dir, self.y_dir
        self.plane = self.plane_x, self.plane_y

    def __rotate(self, rotation_direction):
        ''' Rotate dir vector by 90 angle of roation_direction (-1 or 1)'''
        angle = rotation_direction * 90 * 3.14 / 180
        qx = math.cos(angle) * (self.x_dir) - math.sin(angle) * (self.y_dir)
        qy = math.sin(angle) * (self.x_dir) + math.cos(angle) * (self.y_dir)
        self.x_dir = qx
        self.y_dir = qy
#!/usr/bin/env python3
import pygame
import math
import numpy as np
from random import randint
from time   import time
from SETTINGS import SETTINGS
import script.general.loader as ld
from script.game.camera import Camera
from script.game.weapon import Weapon
from script.game.player import Player
from script.game.enemy import Enemy
from script.game.item import Item
from script.general.text import Text

class GameLoop(object):
    def __init__(self, mapname):
        self.__WIDTH, self.__HEIGHT = SETTINGS.SIZE
        self.__FPS = SETTINGS.FPS
        self.__FILEPATH = SETTINGS.FOLDER
        self.__maparray = np.load(ld.completepath(self.__FILEPATH,"maps",mapname + ".npy"))
        ''' Images '''
        ''' Sounds '''

    def __item_loader(self, value):
        '''Returns unified array of all items of value.'''
        itemstupple = np.where(self.__maparray == value)
        item_y, item_x = itemstupple
        all_items = np.empty((0,2),int)
        for i in range(len(item_x)):
            temp = []
            temp.extend([item_y[i] + 0.5, item_x[i] + 0.5])
            all_items = np.vstack([all_items,np.array(temp)])
        return np.unique(all_items, axis = 0)

    def Main(self):
        ''' Inintialize '''
        pygame.mouse.set_visible(False)
        clock = pygame.time.Clock()
        start_ticks = pygame.time.get_ticks()
        screen = pygame.display.get_surface()
        flag = False
        despawn = False
        realfps = 0
        frames = 0
        end = 0
        ''' Sprites '''
        FPS_clock = Text(10,10,realfps,25,(255,255,255))
        Ending = Text(self.__WIDTH / 2 - 120,self.__HEIGHT - 100,"Press E to finish",40,(255,255,255))
        camera = Camera(self.__maparray)
        weapon = Weapon()
        ''' Sprites - Player '''
        player = Player(self.__maparray)
        try:
            player.x_pos, player.y_pos = np.where(self.__maparray == SETTINGS.MAPITEMS["spawn"])
            player.x_pos = player.x_pos + 0.5
            player.y_pos = player.y_pos + 0.5
        except Exception as e:
            print("SpawnPoint Error: ", e)
        try:
            despawn_x, despawn_y = np.where(self.__maparray == SETTINGS.MAPITEMS["despawn"])
            despawn_x = despawn_x + 0.5
            despawn_y = despawn_y + 0.5
        except Exception as e:
            print("DespawnPoint Error: ", e)
        ''' Sprites - Enemy '''
        enemies_items = pygame.sprite.LayeredUpdates()
        enemies = pygame.sprite.LayeredUpdates()
        enemie_array = self.__item_loader(SETTINGS.MAPITEMS["enemy"])
        lay = 1
        for i in enemie_array:
            enemy = Enemy(tuple(i))
            enemies.add(enemy, layer = lay)
            enemies_items.add(enemy, layer=lay)
            lay+=1
        ''' Sprites - Items '''
        items = pygame.sprite.LayeredUpdates()
        item_array = self.__item_loader(SETTINGS.MAPITEMS["despawn"])
        for i in item_array:
            item = Item(tuple(i),SETTINGS.MAPITEMS["despawn"], 1, 0)
            items.add(item, layer = lay)
            enemies_items.add(item, layer=lay)
            lay+=1     
        item_array = self.__item_loader(SETTINGS.MAPITEMS["health"])
        for i in item_array:
            item = Item(tuple(i),SETTINGS.MAPITEMS["health"], 3, 4)
            items.add(item, layer = lay)
            enemies_items.add(item, layer=lay)
            lay+=1     
        item_array = self.__item_loader(SETTINGS.MAPITEMS["armour"])
        for i in item_array:
            item = Item(tuple(i),SETTINGS.MAPITEMS["armour"], 3, 3)
            items.add(item, layer = lay)
            enemies_items.add(item, layer=lay)
            lay+=1 
        item_array = self.__item_loader(SETTINGS.MAPITEMS["shotgunshell"])
        for i in item_array:
            item = Item(tuple(i),SETTINGS.MAPITEMS["shotgunshell"], 3, 4)
            items.add(item, layer = lay)
            enemies_items.add(item, layer=lay)
            lay+=1     

        ''' Gameloop '''
        while True:
            clock.tick(self.__FPS)
            screen.fill((0,0,0))
            ''' Events '''
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE): 
                    ''' Klick '''
                    enemies = weapon.shoot(screen, player.pos, enemies)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    ''' Reload '''
                    if weapon.load < weapon.mag:
                        weapon._Weapon__reloading = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_e and despawn:
                    ''' Despawn erreicht '''
                    flag = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    ''' Exit -> Pause '''
                    # Pause Code
                    flag = True
                elif event.type == pygame.QUIT:
                    ''' Exit '''
                    flag = True
            ''' Update '''
            fps = int(clock.get_fps())
            player.movement(fps)
            walls = camera.update(player.pos, player.dir, player.plane)
            camera.draw(walls, screen)
            ''' NPCs and Items, Weapon, Player, ... '''
            enemies_items.update(player.pos, player.dir, player.plane, camera.WallDistBuffer)
            for item in items:
                player, weapon = item.pickup(player, weapon)
            for enemy in enemies:
                if enemy.health > 0: player = enemy.npc(player, fps)
            for sprite in sorted(enemies_items, key=lambda spr: spr.dist, reverse=True):
                sprite.render(fps)
                if sprite.dead:
                    sprite.kill()
            ''' Weapon & Player'''
            weapon.update(screen, fps)
            player.update(screen,player.pos,(weapon.name, weapon.load, weapon.amo))
            ''' FPS Counter'''
            if despawn:
                Ending.render_text(screen)
            FPS_clock.text = str(fps)
            FPS_clock.render_text(screen)
            if flag == True or player.health <= 0:
                print("LOST: ", player.health)
                break
            if abs(player.x_pos - despawn_x) < 1 and abs(player.y_pos - despawn_y) < 1:
                ''' Despawn erreicht '''
                despawn = True
            else: 
                despawn = False
            pygame.display.flip()
        pygame.mouse.set_visible(True)
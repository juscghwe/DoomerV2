#!/usr/bin/env python3
import pygame
import math
import os
from time import time
from script.general.text   import Text
from script.general.button import Button
from script.general.toggle import ToggleMenu
from SETTINGS import SETTINGS
import script.general.loader as ld

class SelectMenu(object):
    def __init__(self, editor=False):
        self.__screen = pygame.display.get_surface()
        self.__WIDTH, self.__HEIGHT = SETTINGS.SIZE
        self.__FPS = SETTINGS.FPS
        self.__FILEPATH = SETTINGS.FOLDER
        self.__bg_img = ld.loadimage(self.__FILEPATH, "images/fillings", "selectkarte.png")
        self.schluss = False
        self.__editor = editor

    def Main(self):
        '''Main Loop'''
        self.__clock = pygame.time.Clock()
        start_ticks = pygame.time.get_ticks()
        refresh = False
        old_value = False
        flag = 0
        button_sprites = pygame.sprite.Group()
        ''' Load all Maps '''
        filenames = ld.foldercontent(self.__FILEPATH,"maps")
        for i in range(len(filenames)):
            string = filenames[i]
            filenames[i]=string[:-4]
        select_button = ToggleMenu(50, 50, filenames,30)
        ''' Buttons '''
        if self.__editor==False:
            start_button = Button(self.__WIDTH / 2, 600, "rundeaktiviert", "runaktiviert")
            button_sprites.add(start_button)
        else:
            start_button = Button(self.__WIDTH / 2 - 150, 600, "rundeaktiviert", "runaktiviert")
            newmap_button = Button(self.__WIDTH / 2 + 150, 600, "newmapdeaktiviert", "newmapaktiviert")
            button_sprites.add(start_button,newmap_button)
        ''' Menu Loop '''
        while True:
            self.__clock.tick(self.__FPS)
            for sprite_object in button_sprites.sprites():
                sprite_object.collision()
            ''' EVENT HANDLER '''
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.schluss = True
                    flag = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.schluss = True
                    flag = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.is_touched:
                        self.schluss = False
                        self.result = select_button.active_value
                        flag = True
                    elif self.__editor==True and newmap_button.is_touched:
                        self.schluss = False
                        self.result = "New"
                        flag = True
                    else:
                        select_button.on_mouse_down()
            if flag == True: break
            ''' Draw '''
            self.__screen.blit(self.__bg_img,(0,0))
            for sprite_object in button_sprites.sprites():
                sprite_object.draw(self.__screen)
            select_button.update(self.__screen)
            refresh = False

            pygame.display.flip()
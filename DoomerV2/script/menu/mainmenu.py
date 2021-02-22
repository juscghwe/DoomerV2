#!/usr/bin/env python3
import pygame
import math
import os
from time import time
from script.general.text   import Text
from script.general.button import Button
from script.menu.selectmenu import SelectMenu
import script.general.loader as ld
from SETTINGS import SETTINGS

class MainMenu(object):
    def __init__(self):
        self.__screen = pygame.display.get_surface()
        self.__WIDTH, self.__HEIGHT = SETTINGS.SIZE
        self.__FPS = SETTINGS.FPS
        self.__FILEPATH = SETTINGS.FOLDER
        self.__bg_img = ld.loadimage(self.__FILEPATH, "images/fillings", "titelkarte.png")
        self.schluss = False

    def __mapselector(self, editor=False):
        '''Läd das Mapauswahlmenü und gibt den Mapnahmen zurück'''
        select_menu = SelectMenu(editor)
        select_menu.Main()
        if select_menu.schluss == True:
            self.schluss = True
        else:
            self.mapselection = select_menu.result

    def Main(self):
        '''Main Loop'''
        ''' Init '''
        self.clock = pygame.time.Clock()
        start_ticks = pygame.time.get_ticks()
        refresh = False
        old_value = False
        flag = 0
        text_sprites = pygame.sprite.Group()
        button_sprites = pygame.sprite.Group()
        ''' Buttons '''
        start_button = Button(self.__WIDTH / 2 - 150,600,"startdeaktiviert","startaktiviert")
        editor_button = Button(self.__WIDTH / 2 + 150,600,"editordeaktiviert","editoraktiviert")
        button_sprites.add(start_button, editor_button)
        ''' Game Loop '''
        while True:
            self.clock.tick(self.__FPS)
            for sprite_object in button_sprites.sprites():
                sprite_object.collision()
            ''' Event Handler '''
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.schluss = True
                    flag = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.schluss = True
                    flag = True
                elif event.type == pygame.MOUSEBUTTONDOWN and start_button.is_touched:
                    self.schluss = False
                    self.result = "START"
                    self.__mapselector()
                    flag = True
                elif event.type == pygame.MOUSEBUTTONDOWN and editor_button.is_touched:
                    self.schluss = False
                    self.result = "EDITOR"
                    self.__mapselector(editor=True)
                    flag = True
            ''' Draw '''
            self.__screen.blit(self.__bg_img,(0,0))
            for sprite_object in text_sprites.sprites():
                sprite_object.render_text(self.__screen)
            for sprite_object in button_sprites.sprites():
                sprite_object.draw(self.__screen)
            refresh = False
            pygame.display.flip()
            if flag == True: break

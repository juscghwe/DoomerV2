#!/usr/bin/env python3
'''
Used Media:
- freeimages.com/de/photo/technology-background-1632715 (20.01.2021)
  Titelkarte: Füllung des Schriftzugs (nachbearbeitet)
- rigeshop.com/content/profiles/25/25.png (20.02.2021)
  Gameloop: Despawn (nachbearbeitet)
- Sounds by BFXR
'''

import pygame
import os
import sys
import subprocess
from script.game.gameloop import GameLoop
from script.menu.mainmenu import MainMenu
from script.mapeditor.mapeditortiles import MapEditor
import script.general.loader as ld
from SETTINGS import SETTINGS

WIDTH = SETTINGS.WIDTH
HEIGHT = SETTINGS.HEIGHT
FPS = SETTINGS.FPS
TITLE = SETTINGS.TITLE

''' Inintialize '''
pygame.init()
pygame.mixer.init(buffer=2048)
if SETTINGS.FULLSCREEN:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
pygame.font.init()

''' File System '''
game_folder = SETTINGS.FOLDER = os.path.dirname(__file__)

if __name__ == "__main__":
    ''' Main Menu '''
    main_menu = MainMenu()
    main_menu.Main()
    if main_menu.schluss == False:
        result = main_menu.result
        selectedmap = main_menu.mapselection
        while True:
            if result == "START":
                ''' Game Loop '''
                gameloop = GameLoop(selectedmap)
                #screen = pygame.display.set_mode((WIDTH, HEIGHT))
                gameloop.Main()
            elif result == "EDITOR": 
                ''' Map Editor '''
                mapeditor = MapEditor(selectedmap)
                mapeditor.Main()
            ''' End Menu '''
            end_menu = MainMenu()
            end_menu.Main()
            if end_menu.schluss == True:
                break
            result = end_menu.result
            selectedmap = end_menu.mapselection
        ''' Spiel beenden '''
        pygame.quit
    else:
        pygame.quit
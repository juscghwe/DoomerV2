#!/usr/bin/env python3
import pygame
import math
import numpy as np
from time   import time
from script.mapeditor.itemtiles import Tile
from script.mapeditor.preview import Preview
from script.general.button import Button
from script.general.toggle import ToggleMenu
from script.general.text import Text
from script.general.textfield import TextField
from SETTINGS import SETTINGS
import script.general.loader as ld

class MapEditor(object):
    def __init__(self, selectedmap=""):
        self.__WIDTH, self.__HEIGHT = SETTINGS.SIZE
        self.__value_dict = SETTINGS.MAPITEMS
        self.__FPS = SETTINGS.FPS
        self.__FILEPATH = SETTINGS.FOLDER
        self.__timer = 0
        self.__spawn = False
        if selectedmap == "New" or selectedmap == "":
            self.__new = True
            self.__selected_map = "New"
        else:
            self.__new = False
            self.__selected_map = selectedmap

    def __loadfile(self):
        '''Create new map file or open old'''
        if self.__new == True:
            self.__mapdata = self.__emptylist()
        else:
            self.__mapdata = np.load(ld.completepath(self.__FILEPATH,"maps",self.__selected_map+".npy"))
            self.__tile_finder()

    def __tile_finder(self):
        '''Search in maparray for existing tiles.'''
        tiletupple = np.where(self.__mapdata != 0)
        tile_y, tile_x = tiletupple
        all_tiles = np.empty((0,3),int)
        for i in range(len(tile_x)):
            temp=[]
            value = self.__mapdata[tile_y[i], tile_x[i]]
            temp.extend([tile_x[i], tile_y[i]])
            temp.extend([value])
            if value == self.__value_dict["spawn"]: self.__spawn=True
            all_tiles = np.vstack([all_tiles,np.array(temp)])
        self.__all_tiles = np.unique(all_tiles, axis = 0)

    def __emptylist(self):
        '''Create empty list'''
        gridsize = 10
        square = int(int(self.__HEIGHT / 100) * 100 / gridsize)
        array = np.zeros((square, square), dtype=int)
        #array[[0,-1],:] = 4
        #array[:,[0,-1]] = 4
        return array

    def __save_data(self, mapname):
        '''Saves walls into dataframe'''
        self.__mapdata = self.__emptylist()
        for tile in self.__tiles:
            x,y = tile.pos
            x = int(x/10)
            y = int(y/10)
            try:
                self.__mapdata[y][x] = tile.value
            except Exception:
                print(x, y)
        np.save(ld.completepath(self.__FILEPATH,"maps",mapname+".npy"),self.__mapdata)

    def __drawGrid(self, surface):
        '''Create surface grid'''
        gridsize = 10
        square = int(self.__HEIGHT / 100) * 100
        background_rect = pygame.Rect(0, 0, square, square)
        pygame.draw.rect(surface, (0,0,0), background_rect)
        for x in range(int(square / gridsize)):
            for y in range(int(square / gridsize)):
                rect = pygame.Rect(x * gridsize, y * gridsize, gridsize, gridsize)
                pygame.draw.rect(surface, (105,105,105), rect, 1)

    def Main(self):
        ''' Inintialize '''
        clock = pygame.time.Clock()
        start_ticks = pygame.time.get_ticks()
        screen = pygame.display.get_surface()
        flag = False
        remove = False
        self.__loadfile()
        size = len(self.__mapdata) * 10
        square = int(self.__HEIGHT / 100) * 100
        ''' Sprites - Tiles '''
        self.__tiles = pygame.sprite.Group()
        if self.__new:
            self.__textinput = TextField(square+50,20,70,30)
            self.__spawn = False
            for x in range(square-1):
                self.__tiles.add(Tile("wallwhite",(x,0)))
                self.__tiles.add(Tile("wallwhite",(x,square-1)))
            for y in range(square-3):
                self.__tiles.add(Tile("wallwhite",(0,y+1)))
                self.__tiles.add(Tile("wallwhite",(square-1,y+1)))
        else:
            mapname = Text(square + 50,20,self.__selected_map,30)
            for tile in self.__all_tiles:
                try:
                    name = list(self.__value_dict.keys())[list(self.__value_dict.values()).index(tile[2])]
                    self.__tiles.add(Tile(name, (tile[0]*10, tile[1]*10)))
                except Exception as e:
                    print("Tile unknown: ", e)
        ''' Sprites - UI '''
        warning_a = Text(square + 50,590,"Insert Spawn Point.")
        warning_b = Text(square + 50,600,"Else no saving possible.")
        objecttype = ToggleMenu(square + 50, 50, ["Spawn", "Despawn", "Wall Bloodeye", "Wall Brick", "Wall Column", "Wall White", "Health", "Armour", "Shotgun Shell", "Enemy", "Remove"])
        savebutton = Button(square + 50 + 100, self.__HEIGHT - 100, "savedeaktiviert", "saveaktiviert")
        preview = Preview(["despawn", "wallbloodeye", "wallbrick", "wallcolumn", "wallwhite", "health", "armour", "shotgunshell", "enemy"], (square + 50, 500))
        ''' Gameloop '''
        while True:
            clock.tick(self.__FPS)
            screen.fill((128,128,128))
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] <= size and mouse_pos[1] <= size:
                on_grid = True
            else:
                on_grid = False
            position = tuple(map(lambda a: int(a / 10) * 10, pygame.mouse.get_pos()))
            savebutton.collision()
            drawingtool = objecttype.active_value
            drawingtool = drawingtool.replace(" ", "")
            drawingtool = drawingtool.lower()

            ''' Events '''
            events = pygame.event.get()
            for event in events:
                if (event.type == pygame.MOUSEBUTTONDOWN or pygame.mouse.get_pressed()[0]) and on_grid == True: 
                    ''' Klick auf Grid '''
                    if not(drawingtool == "spawn" and self.__spawn) and drawingtool != "remove":
                        if drawingtool == "spawn": 
                            self.__spawn = True
                        else: 
                            pass
                        tile = Tile(drawingtool, position)
                        self.__tiles.add(tile)
                    elif drawingtool == "remove":
                        for tile in self.__tiles:
                            if tile.pos == position:
                                if tile.value == self.__value_dict["spawn"]:
                                    self.__spawn = False
                                if position[0]==0 or position[0]==size or position[1]==0 or position[1]==size:
                                    self.__tiles.add(Tile("wallwhite",position))
                                tile.kill()
                elif event.type == pygame.MOUSEBUTTONDOWN and on_grid == False:
                    ''' Klick auf Tools '''
                    if self.__new:
                        ''' MapName anlegen '''
                        self.__textinput.on_mouse_down()
                    ''' Werkzeugauswahl '''
                    objecttype.on_mouse_down()
                    if objecttype.active_value=="Remove": remove = True
                    else: remove = False
                    if savebutton.is_touched and self.__spawn: 
                        ''' Speichern '''
                        flag = True
                        if self.__new==True:
                            self.__textinput.update(events,screen)
                            if self.__textinput.textvalue=="":
                                self.__save_data("default")
                            else:
                                self.__save_data(self.__textinput.textvalue)
                        else:
                            self.__save_data(self.__selected_map)                  
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    flag = True
                elif event.type == pygame.QUIT:
                    flag = True
            ''' Update '''
            if self.__new:
                self.__textinput.update(events, screen)
            else:
                mapname.render_text(screen)
            if self.__spawn==False:
                warning_a.render_text(screen)
                warning_b.render_text(screen)

            objecttype.update(screen)
            savebutton.collision()
            savebutton.draw(screen)
            preview.update(screen, drawingtool)
            self.__drawGrid(screen)
            self.__tiles.update(screen)
            if on_grid:
                rect = pygame.Rect(position[0], position[1], 10, 10)
                if remove: color = (128,0,0)
                else: color = (255,255,0)
                pygame.draw.rect(screen, color, rect, 2)
            if flag == True: break
            pygame.display.flip()
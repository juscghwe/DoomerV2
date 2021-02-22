"""Dieses Modul erlaubt das einfache Laden von Dateien"""
import pygame
import os

def completepath(filepath_os,foldername, filename):
    """Gibt kompletten Dateipfad. Erfordert Ordner- und Dateiname."""
    folderpath = os.path.join(filepath_os,foldername)
    filepath = os.path.join(folderpath,filename)
    return filepath

def foldercontent(filepath_os,foldername):
    """Gibt liste aller Dateien in Ordner. Erfordert Ordnername. Ordner darf nicht leer sein."""
    folderpath = os.path.join(filepath_os,foldername)
    filenames = os.listdir(folderpath)
    return filenames

def loadimage(filepath_os,foldername, picturename):
    """Gibt Bild als pygame.surface zurück. Erfordert Ordner- und Bildname."""
    surface = pygame.image.load(completepath(filepath_os,foldername,picturename))
    return surface.convert_alpha()

def loadsound(filepath_os, foldername, soundname):
    """Gibt Sound als pygame.mixer.sound zurück. Erfordert Ordner- und Bildname."""
    sound = pygame.mixer.Sound(self.completepath(foldername,soundname))
    return sound
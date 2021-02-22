import pygame
import script.general.loader as ld
from SETTINGS import SETTINGS

class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x_center, pos_y_center, imagename_inactive, imagename_active):
        pygame.sprite.Sprite.__init__(self)
        self.__inactive_img = ld.loadimage(SETTINGS.FOLDER, "images/buttons", imagename_inactive + ".png")
        self.__active_img = ld.loadimage(SETTINGS.FOLDER, "images/buttons", imagename_active + ".png")

        self.__imagecheck(imagename_inactive,imagename_active)
        self.__img = self.__inactive_img
        self.__rect = self.__img.get_rect()
        self.__rect.center = (pos_x_center, pos_y_center)
        
        self.is_touched = False
        
    def collision(self):
        """Prüft, ob der Button berührt wird"""
        mouse_pos = pygame.mouse.get_pos()
        collision = self.__rect.collidepoint(mouse_pos)
        if collision and self.is_touched == False:
            self.is_touched = True
            self.change = True
            self.__img = self.__active_img
        elif collision == False and self.is_touched:
            self.is_touched = False
            self.change = True
            self.__img = self.__inactive_img
        else:
            self.change = False

    def draw(self,target_surface):
        target_surface.blit(self.__img, self.__rect.topleft)

    def __imagecheck(self, active, inactive):
        """Prüft, ob Bilder dieselbe Größe haben. Gibt sonst Fehler in Konsole aus"""
        width_i, height_i = self.__inactive_img.get_size()
        width_a, height_a = self.__active_img.get_size()
        if width_i != width_a or height_i != height_a:
            print("Fehler: Bildvorlagen für Button {} & {} haben unterschiedliche Größen".format(active, inactive))
import pygame
import script.general.loader as ld
from script.general.text import Text
from SETTINGS import SETTINGS
        
class ToggleMenu(pygame.sprite.Sprite):
    def __init__(self, pos_x_lefttop, pos_y_lefttop, items=[], fontsize=20):
        pygame.sprite.Sprite.__init__(self)
        self.__text_sprites = pygame.sprite.Group()
        self.__button_sprites = pygame.sprite.Group()
        self.change = False
        for i in range(len(items)):
            button = self.Inner_ToggleButton(pos_x_lefttop, pos_y_lefttop + i * fontsize, items[i])
            text = Text(pos_x_lefttop + 30, pos_y_lefttop + 10 + i * fontsize, items[i], fontsize)
            self.__button_sprites.add(button)
            self.__text_sprites.add(text)
            if i == 0:
                button.status = True
                button.prestatus = True
                self.active_value = items[i]

    def on_mouse_down(self):
        """Prüft auf Neuauswahl"""
        values = []
        self.change = False
        self.__button_sprites.update()
        for item in self.__button_sprites:
            values.append(item.prestatus)
            if item.prestatus == True:
                selection = item.name
        if True in values:
            self.change = True
            self.active_value = selection
        
    def update(self, target_surface):
        for item in self.__button_sprites:
            item.draw(target_surface, self.change)
        for item in self.__text_sprites:
            item.render_text(target_surface)

    class Inner_ToggleButton(pygame.sprite.Sprite):
        """Innere Klasse: Nur Toggle Bubbles ohne Text"""
        def __init__(self, pos_x, pos_y, name=""):
            pygame.sprite.Sprite.__init__(self)
            self.inactive_img = ld.loadimage(SETTINGS.FOLDER, "images/buttons", "toggleinactive.png")
            self.active_img = ld.loadimage(SETTINGS.FOLDER, "images/buttons", "toggleactive.png")
            self.name = name
            self.status = False
            self.prestatus = False
            self.image = self.inactive_img
            width, height = self.image.get_size()
            self.rect = self.image.get_rect()
            self.rect.center = (pos_x + width / 2, pos_y + height / 2)

        def update(self):
            """Prüft, ob der Button berührt wird"""
            mouse_pos = pygame.mouse.get_pos()
            collision = self.rect.collidepoint(mouse_pos)
            self.prestatus = False
            if collision and pygame.mouse.get_pressed():
                self.prestatus = True

        def draw(self, target_surface,change=False):
            if change == True:
                self.status = self.prestatus
            if self.status == True:
                self.image = self.active_img
            else:
                self.image = self.inactive_img
            target_surface.blit(self.image,self.rect.topleft)
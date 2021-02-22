import pygame
from script.general.text import Text

class TextField(pygame.sprite.Sprite):
    def __init__(self, x, y, width, fontsize=20):
        pygame.sprite.Sprite.__init__(self)
        self.textvalue = ""
        self.color = (255,255,255)
        self.pos = (x,y)
        self.background_rect = pygame.Rect(x, y, width, fontsize)
        self.input = Text(x+5, y+fontsize/2+5, self.textvalue)
        self.active = False

    def on_mouse_down(self):
        mouse_pos = pygame.mouse.get_pos()
        collision = self.background_rect.collidepoint(mouse_pos)
        if collision:
            self.active = True
        else:
            self.active = False

    def update(self, events, targetsurface):
        x,y = self.pos
        for event in events:
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.textvalue = self.textvalue[:-1]
                else:
                    self.textvalue += event.unicode
        if self.textvalue != "":
            self.input.text = self.textvalue
        else:
            self.input.text = "__"
        pygame.draw.rect(targetsurface, self.color, self.background_rect)
        self.input.render_text(targetsurface)
        pass
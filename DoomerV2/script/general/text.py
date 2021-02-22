import pygame

class Text(pygame.sprite.Sprite):
    def __init__(self, x, y, text, fontsize=20, color = (0,0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.pos = (x,y)
        self.allign = "left"
        self.font = pygame.font.SysFont("Fixedsys", fontsize)
        self.text = text

    def render_text(self, target_surface):
        t_surf = self.font.render(self.text, True, self.color)
        self.image = t_surf
        if self.allign == "left":
            self.rect = self.image.get_rect(midleft = self.pos)
        elif self.allign == "center":
            self.rect = self.image.get_rect(center = self.pos)
        elif self.allign == "right":
            self.rect = self.image.get_rect(midright = self.pos)
        else:
            self.rect = self.image.get_rect(center = self.pos)
        target_surface.blit(self.image, self.rect)
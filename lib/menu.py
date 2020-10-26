import pygame
from .settings import *

class Pause(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("Ubuntu", 30)
        self.text = "Paused"
        self.center = (x, y)
        self.image = self.font.render(self.text, True, WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = self.center
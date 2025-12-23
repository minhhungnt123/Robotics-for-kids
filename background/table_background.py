import os
import pygame
from config import *

class TableBackground:
    def __init__(self):
        self.image = pygame.transform.smoothscale(
            pygame.image.load(
                os.path.join("Images", "Backgrounds", "table_background.png")
            ).convert(),
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
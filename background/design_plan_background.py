import pygame
import os
from config import *

class DesignPlanBackground:
    def __init__(self):
        self.image = pygame.transform.smoothscale(
            pygame.image.load(
                os.path.join("Images", "Backgrounds", "design_plan_background.png")
            ).convert(),
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.x = SCREEN_WIDTH
        self.speed = 40
        self.done = False
        self.locked = False   # ⭐ THÊM

    def update(self):
        if not self.locked:
            if self.x > 0:
                self.x -= self.speed
            else:
                self.x = 0
                self.done = True

    def lock(self):
        """Gọi khi bắt đầu gameplay"""
        self.locked = True
        self.x = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, 0))

    def __init__(self):
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.image = pygame.transform.smoothscale(
            pygame.image.load(
                os.path.join("Images", "Backgrounds", "design_plan_background.png")
            ).convert(),
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        self.x = SCREEN_WIDTH
        self.speed = 50
        self.done = False

    def update(self):
        if self.x > 0:
            self.x -= self.speed
        else:
            self.x = 0
            self.done = True

    def draw(self, screen):
        screen.blit(self.image, (self.x, 0))

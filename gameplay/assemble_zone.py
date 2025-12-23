import pygame
from config import *

class AssembleZone:
    def __init__(self):
        self.image = pygame.Surface((250,250))
        self.image.fill((180,180,255))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.current_state = None
        self.teeter_time = 0

    def set_state(self, new_state):
        self.current_state = new_state

    def wrong_animation(self):
        self.teeter_time = 30

    def draw(self, screen):
        offset = 0
        if self.teeter_time > 0:
            offset = (-1)**self.teeter_time * 5
            self.teeter_time -= 1

        r = self.rect.copy()
        r.x += offset
        screen.blit(self.image, r)

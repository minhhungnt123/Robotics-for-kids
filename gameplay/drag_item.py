import pygame
from config import *

class DragItem:
    def __init__(self, name, pos):
        self.name = name
        self.image = pygame.Surface((100,100))
        self.image.fill((200,200,200))
        self.rect = self.image.get_rect(topleft=pos)
        self.dragging = False
        self.start_pos = pos

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.rect.center = event.pos

    def reset(self):
        self.rect.topleft = self.start_pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)

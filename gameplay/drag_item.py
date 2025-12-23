import pygame
import os
from config import PROJECT_ROOT

class DragItem:
    def __init__(self, name, pos, robot_id):
        self.name = name
        self.start_pos = pos
        self.dragging = False

        # ===== ĐƯỜNG DẪN CHUẨN =====
        img_path = os.path.join(
            PROJECT_ROOT,
            "Images",
            robot_id,              # Robot_1
            f"{name}.png"          # head.png, body.png, track.png...
        )

        if os.path.exists(img_path):
            self.image = pygame.image.load(img_path).convert_alpha()
        else:
            print("❌ Missing DragItem image:", img_path)
            self.image = pygame.Surface((80, 80))
            self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect(topleft=pos)

    # ---------------------------------
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.dragging = True
            mx, my = event.pos
            self.offset = (self.rect.x - mx, self.rect.y - my)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, my = event.pos
            self.rect.x = mx + self.offset[0]
            self.rect.y = my + self.offset[1]

    # ---------------------------------
    def reset(self):
        self.rect.topleft = self.start_pos

    # ---------------------------------
    def draw(self, surface):
        surface.blit(self.image, self.rect)

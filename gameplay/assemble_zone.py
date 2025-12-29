import pygame
import os
from config import *
from config import PROJECT_ROOT

class AssembleZone:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 260, 260)
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.image = None
        self.current_state = None
        self.robot_id = None
        self.teeter_time = 0

    def set_state(self, new_state, robot_id):
        self.current_state = new_state
        self.robot_id = robot_id

        img_path = os.path.join(
            PROJECT_ROOT,
            "Images",
            robot_id,
            f"{new_state}.png"
        )

        if os.path.exists(img_path):
            img = pygame.image.load(img_path).convert_alpha()
            self.image = pygame.transform.smoothscale(
                img,
                (self.rect.width, self.rect.height)
            )
        else:
            print("❌ Missing assemble image:", img_path)
            self.image = None

    def wrong_animation(self):
        self.teeter_time = 25

    def draw(self, screen):
        offset = 0
        if self.teeter_time > 0:
            offset = (-1) ** self.teeter_time * 6
            self.teeter_time -= 1

        r = self.rect.copy()
        r.x += offset

        if self.image:
            screen.blit(self.image, r)
        else:
            pygame.draw.rect(screen, (180, 180, 255), r, border_radius=12)
            pygame.draw.rect(screen, (120, 120, 200), r, 3, border_radius=12)

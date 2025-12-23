import pygame
import os
from menu.robot_card import RobotCard

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.normpath(
    os.path.join(BASE_DIR, "..", "Images", "Menu")
)

class RobotSelectMenu:
    def __init__(self, screen):
        self.screen = screen
        self.w, self.h = screen.get_size()

        self.cards = []
        self.selected_robot = None
        self.fade_alpha = 0   # fade nền khi chọn

        robots = ["robot_1", "robot_2", "robot_3"]
        spacing = 280
        start_x = self.w // 2 - spacing
        y = self.h // 2

        for i, robot_id in enumerate(robots):
            img_path = os.path.join(ASSET_DIR, f"{robot_id}_full_body.png")
            if os.path.exists(img_path):
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.smoothscale(img, (140, 180))
            else:
                img = pygame.Surface((140, 180))
                img.fill((200, 200, 200))

            card = RobotCard(
                robot_id,
                img,
                (start_x + i * spacing, y)
            )
            self.cards.append(card)

    # ---------------------------------
    def handle_event(self, event):
        # ❗ Đã chọn rồi thì không cho click nữa
        if self.selected_robot:
            return None

        for card in self.cards:
            result = card.handle_event(event)
            if result:
                self.selected_robot = result
                return result
        return None

    # ---------------------------------
    def update(self):
        for card in self.cards:
            card.update()

        # Fade nền khi đã chọn
        if self.selected_robot:
            self.fade_alpha = min(180, self.fade_alpha + 8)

    # ---------------------------------
    def draw(self):
        # ❗ KHÔNG fill nền → để table_background vẽ bên dưới
        for card in self.cards:
            card.draw(
                self.screen,
                dim=(self.selected_robot and not card.selected)
            )

        # overlay fade
        if self.fade_alpha > 0:
            overlay = pygame.Surface(self.screen.get_size())
            overlay.set_alpha(self.fade_alpha)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

    # ---------------------------------
    def get_selected_robot(self):
        return self.selected_robot

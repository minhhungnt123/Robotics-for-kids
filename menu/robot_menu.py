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
        self.selected_robot = None   # ⭐ THÊM BIẾN NÀY

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
        for card in self.cards:
            result = card.handle_event(event)
            if result:
                self.selected_robot = result   # ⭐ LƯU LẠI
        return None

    # ---------------------------------
    def update(self):
        for card in self.cards:
            card.update()

    # ---------------------------------
    def draw(self):
        self.screen.fill((40, 50, 70))
        for card in self.cards:
            card.draw(self.screen)

    # ---------------------------------
    def get_selected_robot(self):
        """Được main.py gọi để lấy robot đã chọn"""
        return self.selected_robot
    
    # ---------------------------------
    def get_clicked_card(self):
        for card in self.cards:
            if card.clicked:
                return card
        return None

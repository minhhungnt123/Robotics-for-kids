import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSET_DIR = os.path.join(
    BASE_DIR,        # .../menu
    "..",            # quay ra robotics_game
    "Images",
    "Menu"
)
ASSET_DIR = os.path.normpath(ASSET_DIR)


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()

        # ===== SIZE =====
        self.menu_text_size = (750, 400)
        self.btn_size = (350, 150)

        # ===== LOAD ASSETS (PLACEHOLDER OK) =====
        try:
            self.bg_image = pygame.image.load(
                os.path.join(ASSET_DIR, "menu_text.png")
            ).convert_alpha()
            self.bg_image = pygame.transform.scale(
                self.bg_image, self.menu_text_size
            )

            self.btn_start_img = pygame.image.load(
                os.path.join(ASSET_DIR, "start_button.png")
            ).convert_alpha()
            self.btn_start_img = pygame.transform.scale(
                self.btn_start_img, self.btn_size
            )

            self.btn_setting_img = pygame.image.load(
                os.path.join(ASSET_DIR, "setting_button.png")
            ).convert_alpha()
            self.btn_setting_img = pygame.transform.scale(
                self.btn_setting_img, self.btn_size
            )

        except Exception as e:
            print("⚠ Menu asset missing, using placeholder:", e)
            self.bg_image = pygame.Surface(self.menu_text_size)
            self.bg_image.fill((255, 220, 120))

            self.btn_start_img = pygame.Surface(self.btn_size)
            self.btn_start_img.fill((120, 255, 120))

            self.btn_setting_img = pygame.Surface(self.btn_size)
            self.btn_setting_img.fill((120, 120, 255))

        # ===== POSITION =====
        self.bg_rect = self.bg_image.get_rect(
            center=(self.width // 2, self.height // 2 - 120)
        )
        self.btn_start_rect = self.btn_start_img.get_rect(
            center=(self.width // 2, self.height // 2 + 100)
        )
        self.btn_setting_rect = self.btn_setting_img.get_rect(
            center=(self.width // 2, self.height // 2 + 230)
        )

        # ===== ANIMATION STATE =====
        self.state = "INTRO"   # INTRO → ACTIVE → OUTRO
        self.alpha = 0
        self.fade_speed = 6

    # --------------------------------------------------
    def update(self):
        if self.state == "INTRO":
            self.alpha += self.fade_speed
            if self.alpha >= 255:
                self.alpha = 255
                self.state = "ACTIVE"

        elif self.state == "OUTRO":
            self.alpha -= self.fade_speed
            if self.alpha <= 0:
                self.alpha = 0
                return "START_GAME"

        return None

    # --------------------------------------------------
    def handle_event(self, event):
        if self.state != "ACTIVE":
            return None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_start_rect.collidepoint(event.pos):
                self.state = "OUTRO"
            elif self.btn_setting_rect.collidepoint(event.pos):
                print("⚙ Setting (chưa làm)")

        return None

    # --------------------------------------------------
    def draw(self):
        self.bg_image.set_alpha(self.alpha)
        self.btn_start_img.set_alpha(self.alpha)
        self.btn_setting_img.set_alpha(self.alpha)

        self.screen.blit(self.bg_image, self.bg_rect)
        self.screen.blit(self.btn_start_img, self.btn_start_rect)
        self.screen.blit(self.btn_setting_img, self.btn_setting_rect)

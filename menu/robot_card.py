import pygame

class RobotCard:
    def __init__(self, robot_id, image, center_pos):
        self.robot_id = robot_id

        self.base_size = (220, 260)
        self.base_rect = pygame.Rect(0, 0, *self.base_size)
        self.base_rect.center = center_pos

        self.image = image
        self.img_base_size = self.image.get_size()

        # animation
        self.scale = 1.0
        self.target_scale = 1.0
        self.scale_speed = 0.12

        self.hovered = False
        self.clicked = False

    def handle_event(self, event):
        if self.clicked:
            return None

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.base_rect.collidepoint(event.pos)
            self.target_scale = 1.08 if self.hovered else 1.0

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.base_rect.collidepoint(event.pos):
                self.clicked = True
                self.target_scale = 1.25   # ⭐ bật to khi click
                return self.robot_id

        return None

    def update(self):
        self.scale += (self.target_scale - self.scale) * self.scale_speed

    def get_rect(self):
        w = int(self.base_size[0] * self.scale)
        h = int(self.base_size[1] * self.scale)
        rect = pygame.Rect(0, 0, w, h)
        rect.center = self.base_rect.center
        return rect

    def draw(self, screen):
        rect = self.get_rect()

        bg_color = (235, 245, 255) if self.hovered else (190, 210, 230)
        pygame.draw.rect(screen, bg_color, rect, border_radius=18)
        pygame.draw.rect(screen, (120, 150, 190), rect, 3, border_radius=18)

        img = pygame.transform.smoothscale(
            self.image,
            (int(self.img_base_size[0] * self.scale),
             int(self.img_base_size[1] * self.scale))
        )
        img_rect = img.get_rect(center=(rect.centerx, rect.centery - 10))
        screen.blit(img, img_rect)

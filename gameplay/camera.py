import pygame

class CameraZoom:
    def __init__(self):
        self.scale = 1.05
        self.target = 1.0
        self.speed = 0.06

    def update(self):
        self.scale += (self.target - self.scale) * self.speed

    def apply(self, surface):
        w, h = surface.get_size()
        new_size = (int(w * self.scale), int(h * self.scale))
        zoomed = pygame.transform.smoothscale(surface, new_size)

        x = (new_size[0] - w) // 2
        y = (new_size[1] - h) // 2
        return zoomed.subsurface((x, y, w, h))
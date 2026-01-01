import pygame
import os
from config import PROJECT_ROOT

class DragItem(pygame.sprite.Sprite):
    def __init__(self, name, pos, robot_id, scale_factor=1.0):
        super().__init__()
        self.name = name
        self.robot_id = robot_id
        
        # --- CẤU HÌNH KÍCH THƯỚC CHUẨN ---
        # Đây là kích thước "1.0" mà bạn mong muốn.
        # Nghĩa là nếu scale_factor = 1.0, ảnh sẽ nằm gọn trong khung 100x100
        self.BASE_SIZE = 100 

        image_path = os.path.join(PROJECT_ROOT, "Images", robot_id, f"{name}.png")
        
        if os.path.exists(image_path):
            try:
                self.image = pygame.image.load(image_path).convert_alpha()
                
                # --- LOGIC MỚI: ÉP VỀ KÍCH THƯỚC CHUẨN RỒI MỚI SCALE ---
                # 1. Lấy kích thước ảnh gốc
                orig_w = self.image.get_width()
                orig_h = self.image.get_height()

                # 2. Tính tỉ lệ để ép ảnh gốc về BASE_SIZE (giữ nguyên tỉ lệ khung hình)
                # Nó sẽ chọn cạnh dài nhất để ép về 100px
                fit_scale = self.BASE_SIZE / max(orig_w, orig_h)
                
                # 3. Nhân thêm hệ số tùy chỉnh của bạn (scale_factor)
                final_scale = fit_scale * scale_factor

                # 4. Tính kích thước cuối cùng
                new_w = int(orig_w * final_scale)
                new_h = int(orig_h * final_scale)
                
                # 5. Thực hiện resize
                self.image = pygame.transform.smoothscale(self.image, (new_w, new_h))
                    
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")
                self._create_fallback_surface()
        else:
            print(f"Image not found: {image_path}")
            self._create_fallback_surface()

        # --- THIẾT LẬP VỊ TRÍ ---
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.start_pos = pos 
        
        # Trạng thái kéo thả
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def _create_fallback_surface(self):
        """Tạo hình vuông đỏ tạm nếu lỗi ảnh"""
        self.image = pygame.Surface((self.BASE_SIZE, self.BASE_SIZE))
        self.image.fill((255, 0, 0))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.dragging = True
                mouse_x, mouse_y = event.pos
                self.offset_x = self.rect.x - mouse_x
                self.offset_y = self.rect.y - mouse_y
                return True 

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
                
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x + self.offset_x
                self.rect.y = mouse_y + self.offset_y
                return True
        return False

    def reset(self):
        self.rect.topleft = self.start_pos
        self.dragging = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
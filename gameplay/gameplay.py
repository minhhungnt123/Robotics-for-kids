import pygame
import json
import itertools
import os
from gameplay.drag_item import DragItem
from gameplay.assemble_zone import AssembleZone
from quiz.quiz import QuizManager
from menu.finish_menu import FinishMenu
from config import *

# --- CLASS ANIMATION (Dùng lại logic cắt ảnh) ---
class SpriteAnimation:
    def __init__(self, image_path, scale_size, n_frames=1): # <--- Thêm n_frames
        self.frames = []
        self.current_frame = 0
        self.last_update = 0
        self.cooldown = 100 

        if os.path.exists(image_path):
            sprite_sheet = pygame.image.load(image_path).convert_alpha()
            sheet_w, sheet_h = sprite_sheet.get_size()
            
            if n_frames > 0:
                frame_width = sheet_w // n_frames # <--- Tính toán chuẩn xác
                for i in range(n_frames):
                    frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, sheet_h))
                    self.frames.append(pygame.transform.smoothscale(frame, scale_size))
        
        if not self.frames:
            s = pygame.Surface(scale_size); s.fill((0, 255, 0))
            self.frames.append(s)

class Gameplay:
    def __init__(self, screen, robot_id, blueprint_bg):
        self.screen = screen
        self.robot_id = robot_id
        self.blueprint_bg = blueprint_bg
        self.robot_key = robot_id.lower()
        
        self.finish_menu = FinishMenu(screen)
        self.zone = AssembleZone()
        self.zone.set_state("body", robot_id)

        # CẤU HÌNH BỘ PHẬN (Giữ nguyên như bạn đã làm)
        ROBOT_CONFIGS = {
            "robot_1": ["gun", "pinwheel"],                 
            "robot_2": ["engine", "head", "law"],           
            "robot_3": ["arm", "head", "power", "track"],   
        }
        
        # MAPPING FOLDER & FILE RUN CHO TỪNG ROBOT
        # Dựa trên file bạn upload:
        # Robot 1: Images/Robot_1/robot_1_run.png (Bạn có file robot_1_run.png không? Tôi check thấy có robot_1_idle, tôi đoán tên file Run tương tự hoặc bạn cần đổi tên)
        # Tôi sẽ giả định tên file dựa trên pattern Idle bạn cung cấp
        RUN_FILES = {
            "robot_1": {"folder": "Robot_1", "file": "robot_1_run.png"}, # File Uploaded: robot_1_run.png ? (Nếu chưa có, hãy đảm bảo tên đúng)
            "robot_2": {"folder": "Robot_2", "file": "robot_2_run.png"},
            "robot_3": {"folder": "Robot_3", "file": "robot_3_run.png"},
        }
        
        PART_POSITIONS = {
            "gun": (350, 500), "pinwheel": (600, 500),
            "engine": (300, 520), "head": (500, 520), "law": (700, 520),
            "track": (400, 550), "arm": (600, 550), "power": (800, 550),
        }

        self.opt_parts = ROBOT_CONFIGS.get(self.robot_key, [])
        self.parts = []
        for part_name in self.opt_parts:
            pos = PART_POSITIONS.get(part_name, (100 + len(self.parts)*150, 500))
            self.parts.append(DragItem(part_name, pos, self.robot_id))

        # LOGIC LẮP RÁP
        self.assembly_logic = {}
        def make_state_name(part_list):
            if len(part_list) == len(self.opt_parts): return f"{self.robot_key}_full_body"
            if not part_list: return "body"
            return "body_" + "_".join(sorted(part_list))

        for i in range(len(self.opt_parts) + 1): 
            for current_combo in itertools.combinations(self.opt_parts, i):
                current_state = make_state_name(current_combo)
                for part in self.opt_parts:
                    if part not in current_combo:
                        new_combo = list(current_combo) + [part]
                        self.assembly_logic[(current_state, part)] = make_state_name(new_combo)

        # QUIZ (Giữ nguyên)
        self.quiz = QuizManager(SCREEN_WIDTH, SCREEN_HEIGHT)
        try:
            with open("quiz/questions.json", encoding="utf-8") as f:
                self.questions = json.load(f).get(self.robot_key, [])
        except: self.questions = []
        
        # CHUẨN HÓA CÂU HỎI
        self.formatted_qs = []
        for q in self.questions:
            self.formatted_qs.append({
                "question": q["question"],
                "options": q["options"],
                "correct_index": q["answer"]
            })

        self.pending_part = None

        # ⭐ BIẾN CHO ANIMATION CHẠY KHI THẮNG ⭐
        self.is_victory_run = False
        self.victory_start_time = 0
        self.run_duration = 5000 # 5 giây
        
        # Load Animation Run
        run_info = RUN_FILES.get(self.robot_key, {"folder": "Robot_1", "file": "robot_1_run.png"})
        run_path = os.path.join(PROJECT_ROOT, "Images", run_info["folder"], run_info["file"])
        # Scale robot chạy to ra một chút (300x300)
        self.run_anim = SpriteAnimation(run_path, (300, 300))
        
        # Vị trí robot chạy (giữa màn hình)
        self.run_pos_x = SCREEN_WIDTH // 2 - 150
        self.run_pos_y = SCREEN_HEIGHT // 2 - 150

    def handle_event(self, event):
        # 1. Menu chiến thắng
        if self.finish_menu.is_active:
            return self.finish_menu.handle_event(event)

        # ⭐ Nếu đang chạy animation thắng -> Không cho tương tác gì cả
        if self.is_victory_run:
            return None

        # 2. Quiz
        if self.quiz.is_active:
            self.quiz.handle_input(event)
            return

        # 3. Kéo thả
        for part in reversed(self.parts):
            if part.handle_event(event): break 

        if event.type == pygame.MOUSEBUTTONUP:
            for part in self.parts:
                if part.rect.colliderect(self.zone.rect):
                    self.pending_part = part
                    if len(self.formatted_qs) > 0:
                        self.quiz.start_quiz(self.formatted_qs.pop(0))
                    else:
                        self._try_assemble()
                    break

    def update(self):
        # 1. Menu thắng
        if self.finish_menu.is_active:
            self.finish_menu.update()
            return

        # ⭐ 2. XỬ LÝ ANIMATION RUN 5 GIÂY
        if self.is_victory_run:
            self.run_anim.update()
            
            # (Tùy chọn) Cho robot chạy từ trái qua phải
            # self.run_pos_x += 2 
            # if self.run_pos_x > SCREEN_WIDTH: self.run_pos_x = -300

            # Kiểm tra hết giờ chưa
            elapsed = pygame.time.get_ticks() - self.victory_start_time
            if elapsed >= self.run_duration:
                self.is_victory_run = False
                self.finish_menu.show() # Hiện bảng thành tích
            return

        # 3. Logic game bình thường
        result = self.quiz.update()
        if result is not None and self.pending_part:
            if result: self._try_assemble()
            else:
                self.pending_part.reset()
                self.zone.wrong_animation()
            self.pending_part = None
        
        # ⭐ CHECK WIN -> KÍCH HOẠT CHẠY 5s TRƯỚC
        if not self.parts and not self.pending_part and not self.quiz.is_active:
            if not self.is_victory_run and not self.finish_menu.is_active:
                print("🎉 Assembly Done! Starting Victory Run...")
                self.is_victory_run = True
                self.victory_start_time = pygame.time.get_ticks()

    def _try_assemble(self):
        current = self.zone.current_state
        part = self.pending_part.name
        nxt = self.assembly_logic.get((current, part))
        
        if nxt and os.path.exists(os.path.join(PROJECT_ROOT, "Images", self.robot_id, f"{nxt}.png")):
            self.zone.set_state(nxt, self.robot_id)
            self.parts.remove(self.pending_part)
        else:
            self.pending_part.reset()
            self.zone.wrong_animation()

    def draw(self):
        # Vẽ nền
        self.blueprint_bg.draw(self.screen)
        
        # ⭐ NẾU ĐANG CHẠY VICTORY RUN -> CHỈ VẼ ROBOT ĐANG CHẠY
        if self.is_victory_run:
            # Có thể vẽ thêm dòng chữ "COMPLETED!"
            run_img = self.run_anim.get_image()
            self.screen.blit(run_img, (self.run_pos_x, self.run_pos_y))
            
        else:
            # Vẽ bàn lắp ráp bình thường
            self.zone.draw(self.screen)
            for part in self.parts:
                part.draw(self.screen)
            self.quiz.draw(self.screen)
        
        # Menu thắng (vẽ đè lên cùng khi xong run)
        self.finish_menu.draw()
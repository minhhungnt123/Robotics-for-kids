import pygame
import json
import itertools
import os
from gameplay.drag_item import DragItem
from gameplay.assemble_zone import AssembleZone
from quiz.quiz import QuizManager
from menu.finish_menu import FinishMenu
from config import *

# --- CLASS ANIMATION (ĐẦY ĐỦ) ---
class SpriteAnimation:
    def __init__(self, image_path, scale_size, n_frames=1):
        self.frames = []
        self.current_frame = 0
        self.last_update = 0
        self.cooldown = 100  # Tốc độ animation (ms)

        if os.path.exists(image_path):
            try:
                sprite_sheet = pygame.image.load(image_path).convert_alpha()
                sheet_w, sheet_h = sprite_sheet.get_size()
                
                # Cắt frame dựa trên số lượng frame khai báo (n_frames)
                if n_frames > 0:
                    frame_width = sheet_w // n_frames
                    for i in range(n_frames):
                        # Cắt từng hình nhỏ
                        frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, sheet_h))
                        # Resize
                        scaled_frame = pygame.transform.smoothscale(frame, scale_size)
                        self.frames.append(scaled_frame)
            except Exception as e:
                print(f"⚠ Lỗi load animation {image_path}: {e}")
        
        # Nếu không load được, tạo hình xanh lá cây tạm
        if not self.frames:
            s = pygame.Surface(scale_size)
            s.fill((0, 255, 0))
            self.frames.append(s)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.cooldown:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def get_image(self):
        return self.frames[self.current_frame]


class Gameplay:
    def __init__(self, screen, robot_id, blueprint_bg):
        self.screen = screen
        self.robot_id = robot_id
        self.blueprint_bg = blueprint_bg
        self.robot_key = robot_id.lower()
        
        self.finish_menu = FinishMenu(screen)
        self.zone = AssembleZone()
        self.zone.set_state("body", robot_id)

        # ====================================================
        # 1. CẤU HÌNH CÁC BỘ PHẬN
        # ====================================================
        ROBOT_CONFIGS = {
            "robot_1": ["gun", "pinwheel"],                 
            "robot_2": ["engine", "head", "law"],           
            "robot_3": ["arm", "head", "power", "track"],   
        }
        
        # ====================================================
        # 2. CẤU HÌNH ANIMATION CHẠY (VICTORY RUN)
        # ====================================================
        # Lưu ý: "frames" là số lượng hình nhỏ trong file ảnh chạy
        RUN_FILES = {
            "robot_1": {
                "folder": "Robot_1", 
                "file": "Scout_run.png", 
                "scale": (300, 300),
                "frames": 10
            },
            "robot_2": {
                "folder": "Robot_2", 
                "file": "robot_2_run.png",
                "scale": (280, 320),
                "frames": 9
            },
            "robot_3": {
                "folder": "Robot_3", 
                "file": "robot_3_run.png",
                "scale": (400, 400),
                "frames": 4
            },
        }
        
        # Vị trí các bộ phận trên bàn
        PART_POSITIONS = {
            "gun": (350, 500), "pinwheel": (600, 500),
            "engine": (300, 520), "head": (500, 520), "law": (700, 520),
            "track": (400, 550), "arm": (600, 550), "power": (800, 550),
        }

        # --- SETUP GAMEPLAY ---
        self.opt_parts = ROBOT_CONFIGS.get(self.robot_key, [])
        self.parts = []
        for part_name in self.opt_parts:
            pos = PART_POSITIONS.get(part_name, (100 + len(self.parts)*150, 500))
            self.parts.append(DragItem(part_name, pos, self.robot_id))

        # Logic lắp ráp
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

        # Quiz Manager
        self.quiz = QuizManager(SCREEN_WIDTH, SCREEN_HEIGHT)
        try:
            with open("quiz/questions.json", encoding="utf-8") as f:
                raw_data = json.load(f).get(self.robot_key, [])
        except: 
            raw_data = []
        
        self.questions = []
        for q in raw_data:
            self.questions.append({
                "question": q["question"],
                "options": q["options"],
                "correct_index": q["answer"]
            })

        self.pending_part = None

        # --- SETUP ANIMATION RUN ---
        self.is_victory_run = False
        self.victory_start_time = 0
        self.run_duration = 5000 # 5 giây
        
        # Load Animation Run
        run_info = RUN_FILES.get(self.robot_key, {"folder": "Robot_1", "file": "Scout_run.png", "frames": 1})
        run_path = os.path.join(PROJECT_ROOT, "Images", run_info.get("folder"), run_info.get("file"))
        
        run_scale = run_info.get("scale", (300, 300))
        run_frames = run_info.get("frames", 1)
        
        self.run_anim = SpriteAnimation(run_path, run_scale, run_frames)
        
        # Vị trí chạy
        self.run_pos_x = SCREEN_WIDTH // 2 - run_scale[0] // 2
        self.run_pos_y = SCREEN_HEIGHT // 2 - run_scale[1] // 2

    def handle_event(self, event):
        # 1. Menu chiến thắng
        if self.finish_menu.is_active:
            return self.finish_menu.handle_event(event)

        # Nếu đang chạy animation thắng -> Chặn input
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
                    if len(self.questions) > 0:
                        self.quiz.start_quiz(self.questions.pop(0))
                    else:
                        self._try_assemble()
                    break

    def update(self):
        if self.finish_menu.is_active:
            self.finish_menu.update()
            return

        # UPDATE VICTORY RUN
        if self.is_victory_run:
            self.run_anim.update()
            
            elapsed = pygame.time.get_ticks() - self.victory_start_time
            if elapsed >= self.run_duration:
                self.is_victory_run = False
                self.finish_menu.show()
            return

        # Logic bình thường
        result = self.quiz.update()
        if result is not None and self.pending_part:
            if result: self._try_assemble()
            else:
                self.pending_part.reset()
                self.zone.wrong_animation()
            self.pending_part = None
        
        # Check Win
        if not self.parts and not self.pending_part and not self.quiz.is_active:
            if not self.is_victory_run and not self.finish_menu.is_active:
                print("🎉 Starting Victory Run...")
                self.is_victory_run = True
                self.victory_start_time = pygame.time.get_ticks()

    def _try_assemble(self):
        current = self.zone.current_state
        part = self.pending_part.name
        nxt = self.assembly_logic.get((current, part))
        
        # Check file ảnh tồn tại
        if nxt and os.path.exists(os.path.join(PROJECT_ROOT, "Images", self.robot_id, f"{nxt}.png")):
            self.zone.set_state(nxt, self.robot_id)
            self.parts.remove(self.pending_part)
        else:
            print(f"❌ Thiếu ảnh: {nxt}.png")
            self.pending_part.reset()
            self.zone.wrong_animation()

    def draw(self):
        self.blueprint_bg.draw(self.screen)
        
        if self.is_victory_run:
            # Vẽ animation chạy
            run_img = self.run_anim.get_image() # Hàm này đã có trong class SpriteAnimation ở trên
            self.screen.blit(run_img, (self.run_pos_x, self.run_pos_y))
        else:
            self.zone.draw(self.screen)
            for part in self.parts:
                part.draw(self.screen)
            self.quiz.draw(self.screen)
        
        self.finish_menu.draw()
import pygame
import json
from gameplay.drag_item import DragItem
from gameplay.assemble_zone import AssembleZone
from quiz.quiz import QuizManager
from config import *

class Gameplay:
    def __init__(self, screen, robot_id, blueprint_bg):
        self.screen = screen
        self.robot_id = robot_id
        self.blueprint_bg = blueprint_bg
        self.robot_folder = robot_id
        self.robot_key = robot_id.lower()

        self.zone = AssembleZone()
        self.zone.set_state("body", robot_id)   # ⭐ BODY BAN ĐẦU

        self.parts = [
            DragItem("head",  (300, 520), self.robot_folder),
            DragItem("track", (450, 520), self.robot_folder),
            DragItem("arm",   (600, 520), self.robot_folder),
            DragItem("power", (750, 520), self.robot_folder),
        ]

        # --- LOGIC LẮP RÁP MỚI ---
        # Định nghĩa: (Trạng thái hiện tại, Bộ phận thêm vào) -> Trạng thái mới
        self.assembly_logic = {
            ("body", "head"): "head_body",
            ("head_body", "track"): "head_body_track",
            ("head_body_track", "arm"): "head_body_track_arm",
            ("head_body_track", "power"): "head_body_track_power",
            # Hai trường hợp cuối để hoàn thành robot
            ("head_body_track_arm", "power"): "robot_1_full_body",
            ("head_body_track_power", "arm"): "robot_1_full_body"
        }

        self.quiz = QuizManager(SCREEN_WIDTH, SCREEN_HEIGHT)

        with open("quiz/questions.json", encoding="utf-8") as f:
            raw_data = json.load(f)[self.robot_key]
            
        # Chuyển đổi key 'answer' -> 'correct_index' để khớp với QuizManager
        self.questions = []
        for q in raw_data:
            # Tạo dictionary mới đúng chuẩn
            formatted_q = {
                "question": q["question"],
                "options": q["options"],
                "correct_index": q["answer"]  # Đổi tên key ở đây
            }
            self.questions.append(formatted_q)
        # --------------------

        self.pending_part = None

    # -----------------------------------------
    def handle_event(self, event):
        # Quiz đang mở → chỉ quiz nhận input
        if self.quiz.is_active:
            self.quiz.handle_input(event)
            return

        for part in self.parts:
            part.handle_event(event)

        if event.type == pygame.MOUSEBUTTONUP:
            for part in self.parts:
                if part.rect.colliderect(self.zone.rect):
                    self.pending_part = part
                    # Lấy câu hỏi tiếp theo (nếu còn)
                    if self.questions:
                        question = self.questions.pop(0)
                        self.quiz.start_quiz(question)
                    else:
                        print("Hết câu hỏi!")
                        # Có thể xử lý logic khi hết câu hỏi ở đây nếu cần
                    break

    # -----------------------------------------
    def update(self):
        result = self.quiz.update()
        if result is not None and self.pending_part:
            if result:
                # --- SỬA LOGIC CẬP NHẬT TRẠNG THÁI ---
                current_state = self.zone.current_state
                part_name = self.pending_part.name
                
                # Tìm trạng thái tiếp theo trong từ điển quy tắc
                next_state = self.assembly_logic.get((current_state, part_name))
                
                if next_state:
                    self.zone.set_state(next_state, self.robot_id)
                    self.parts.remove(self.pending_part)
                else:
                    # Nếu lắp sai thứ tự (VD: chưa có đầu mà đã lắp tay)
                    print(f"⚠️ Lắp sai thứ tự! Không thể gắn '{part_name}' vào '{current_state}'")
                    self.pending_part.reset()
                    self.zone.wrong_animation()
                # -------------------------------------
            else:
                # Trả lời sai -> Reset vị trí mảnh ghép
                self.pending_part.reset()
                self.zone.wrong_animation()

            self.pending_part = None

    # -----------------------------------------
    def draw(self):
        # 1. Blueprint nền
        self.blueprint_bg.draw(self.screen)

        # 2. Robot lắp ráp
        self.zone.draw(self.screen)

        # 3. Parts
        for part in self.parts:
            part.draw(self.screen)

        # 4. Quiz
        self.quiz.draw(self.screen)
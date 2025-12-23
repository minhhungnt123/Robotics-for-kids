import pygame
import json
from config import *

from gameplay.drag_item import DragItem
from gameplay.assemble_zone import AssembleZone
from gameplay.camera import CameraZoom
from quiz.quiz import QuizManager


class Gameplay:
    def __init__(self, screen, robot_id, blueprint_bg):
        self.screen = screen
        self.robot_id = robot_id
        self.blueprint_bg = blueprint_bg

        # ===== CAMERA =====
        self.camera = CameraZoom()

        # ===== ASSEMBLE ZONE =====
        self.zone = AssembleZone()

        # ===== DRAG PARTS (PLACEHOLDER) =====
        self.parts = [
            DragItem("head", (450, 560), robot_id),
            DragItem("track", (600, 560), robot_id),
            DragItem("arm", (750, 560), robot_id),
            DragItem("power", (900, 560), robot_id),
        ]

        # ===== QUIZ =====
        self.quiz = QuizManager(SCREEN_WIDTH, SCREEN_HEIGHT)

        with open("quiz/questions.json", encoding="utf-8") as f:
            self.questions = json.load(f)[robot_id]

        self.pending_part = None
        self.state = "IDLE"

    # ==================================================
    def handle_event(self, event):
        if self.quiz.is_active:
            return

        for part in self.parts:
            part.handle_event(event)

        # Thả part vào zone
        if event.type == pygame.MOUSEBUTTONUP:
            for part in self.parts:
                if part.rect.colliderect(self.zone.rect):
                    self.pending_part = part
                    question = self.questions.pop(0)
                    self.quiz.start_quiz(question)
                    break

    # ==================================================
    def update(self):
        self.camera.update()

        # Quiz trả kết quả
        result = self.quiz.update()
        if result is not None and self.pending_part:
            if result:
                # ĐÚNG → lắp thành công
                self.zone.set_state(self.pending_part.name, self.robot_id)
                self.parts.remove(self.pending_part)
            else:
                # SAI → rung + trả part
                self.pending_part.reset()
                self.zone.wrong_animation()

            self.pending_part = None

    # ==================================================
    def draw_game_objects(self, surface):
        """
        Vẽ gameplay LÊN blueprint
        """
        # 1. Blueprint background
        self.blueprint_bg.draw(surface)

        # 2. Assemble zone
        self.zone.draw(surface)

        # 3. Parts
        for part in self.parts:
            part.draw(surface)

        # 4. Quiz
        self.quiz.draw(surface)

    # ==================================================
    def draw(self):
        # Surface trung gian để zoom
        temp = pygame.Surface(self.screen.get_size())

        self.draw_game_objects(temp)

        # Áp camera zoom
        zoomed = self.camera.apply(temp)

        self.screen.blit(zoomed, (0, 0))

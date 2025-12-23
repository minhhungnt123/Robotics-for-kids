import pygame
import json
import os
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class QuizManager:
    def __init__(self, screen_width, screen_height):
        self.sw = screen_width
        self.sh = screen_height

        # ===== FONT =====
        self.font_q = pygame.font.SysFont("Arial", 26, bold=True)
        self.font_a = pygame.font.SysFont("Arial", 20)

        # ===== LOAD QUESTIONS =====
        with open(os.path.join(BASE_DIR, "questions.json"), encoding="utf-8") as f:
            self.data = json.load(f)

        # ===== STATE =====
        self.active = False
        self.current_question = None
        self.correct_index = None
        self.result = None

        # ===== UI =====
        self.panel = pygame.Rect(
            self.sw * 0.15, self.sh * 0.2,
            self.sw * 0.7, self.sh * 0.5
        )

        self.answer_rects = []

    # --------------------------------------------------
    def start_quiz(self, robot_id):
        """
        robot_id: 'robot_1' | 'robot_2' | 'robot_3'
        """
        pool = self.data.get(robot_id, [])
        if not pool:
            return

        q = random.choice(pool)

        self.current_question = q
        self.correct_index = q["answer"]
        self.active = True
        self.result = None

        # create answer hitboxes
        self.answer_rects.clear()
        for i in range(4):
            r = pygame.Rect(
                self.panel.x + 40,
                self.panel.y + 120 + i * 60,
                self.panel.width - 80,
                45
            )
            self.answer_rects.append(r)

    # --------------------------------------------------
    def handle_event(self, event):
        if not self.active:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(self.answer_rects):
                if rect.collidepoint(event.pos):
                    self.result = (i == self.correct_index)
                    self.active = False
                    return self.result

        return None

    # --------------------------------------------------
    def draw(self, screen):
        if not self.active:
            return

        # dark background
        overlay = pygame.Surface((self.sw, self.sh))
        overlay.set_alpha(160)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # panel
        pygame.draw.rect(screen, (240, 240, 240), self.panel, border_radius=16)
        pygame.draw.rect(screen, (180, 180, 180), self.panel, 3, border_radius=16)

        # question
        q_text = self.font_q.render(
            self.current_question["question"], True, BLACK
        )
        screen.blit(q_text, (self.panel.x + 40, self.panel.y + 40))

        # answers
        for i, option in enumerate(self.current_question["options"]):
            rect = self.answer_rects[i]
            pygame.draw.rect(screen, (200, 200, 255), rect, border_radius=8)

            text = self.font_a.render(option, True, BLACK)
            screen.blit(
                text,
                text.get_rect(center=rect.center)
            )

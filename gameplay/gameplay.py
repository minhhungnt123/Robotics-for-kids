import json
from gameplay.drag_item import DragItem
from gameplay.assemble_zone import AssembleZone
from quiz.quiz import QuizManager
from background.design_plan_background import DesignPlanBackground
from robots.robot_1 import Robot1

class Gameplay:
    def __init__(self, screen, robot_id):
        self.screen = screen
        self.robot = Robot1()
        self.bg = DesignPlanBackground()
        self.zone = AssembleZone()
        self.quiz = QuizManager()

        self.parts = [
            DragItem("body", (200, 550)),
            DragItem("head", (350, 550))
        ]

        with open("quiz/questions.json", encoding="utf-8") as f:
            self.questions = json.load(f)

        self.pending_part = None

    def handle_event(self, event):
        for p in self.parts:
            p.handle_event(event)

        if event.type == pygame.MOUSEBUTTONUP:
            for p in self.parts:
                if p.rect.colliderect(self.zone.rect):
                    q = self.questions["robot_1"]["easy"][0]
                    self.quiz.start(q)
                    self.pending_part = p

        result = self.quiz.handle_event(event)
        if result is not None:
            if result:
                self.zone.set_state(self.pending_part.name)
                self.parts.remove(self.pending_part)
            else:
                self.pending_part.reset()
                self.zone.wrong_animation()

    def update(self):
        self.bg.update()

    def draw(self):
        self.screen.fill((255,255,255))
        self.bg.draw(self.screen)
        self.zone.draw(self.screen)

        for p in self.parts:
            p.draw(self.screen)

        self.quiz.draw(self.screen)

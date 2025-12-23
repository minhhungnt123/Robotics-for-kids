import pygame
from config import *

from menu.main_menu import Menu
from menu.robot_menu import RobotSelectMenu

from background.table_background import TableBackground
from background.design_plan_background import DesignPlanBackground

from gameplay.gameplay import Gameplay


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Robotics Assembly Game")
clock = pygame.time.Clock()

# ===== STATES =====
STATE_MAIN_MENU = "main_menu"
STATE_ROBOT_MENU = "robot_menu"
STATE_DESIGN_PLAN = "design_plan"
STATE_GAME = "game"

state = STATE_MAIN_MENU

# ===== OBJECTS =====
main_menu = Menu(screen)
robot_menu = RobotSelectMenu(screen)

table_bg = TableBackground()
design_plan = None
gameplay = None

selected_robot = None

running = True
while running:
    clock.tick(FPS)

    # ================= EVENT =================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == STATE_MAIN_MENU:
            main_menu.handle_event(event)

        elif state == STATE_ROBOT_MENU:
            robot_menu.handle_event(event)

        elif state == STATE_GAME:
            gameplay.handle_event(event)

    # ================= DRAW BACKGROUND =================
    if state in (STATE_MAIN_MENU, STATE_ROBOT_MENU):
        table_bg.update()
        table_bg.draw(screen)

    elif state == STATE_DESIGN_PLAN:
        table_bg.draw(screen)   # nền cũ phía sau

    # ================= STATE LOGIC =================
    if state == STATE_MAIN_MENU:
        result = main_menu.update()
        main_menu.draw()

        if result == "START_GAME":
            state = STATE_ROBOT_MENU

    elif state == STATE_ROBOT_MENU:
        robot_menu.update()
        robot_menu.draw()

        result = robot_menu.get_selected_robot()
        if result:
            selected_robot = result
            design_plan = DesignPlanBackground()
            state = STATE_DESIGN_PLAN

    elif state == STATE_DESIGN_PLAN:
        design_plan.update()
        design_plan.draw(screen)

        if design_plan.done:
            design_plan.lock()                 
            gameplay = Gameplay(
                screen,
                selected_robot,
                design_plan             
            )
            state = STATE_GAME

    elif state == STATE_GAME:
        gameplay.update()
        gameplay.draw()

    pygame.display.flip()

pygame.quit()

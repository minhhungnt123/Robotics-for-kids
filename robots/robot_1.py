from robots.robot_base import RobotBase

class Robot1(RobotBase):
    def __init__(self):
        super().__init__()

        self.parts = ["body", "head"]

        self.preview_image = "#robot1_full.png"

        self.assemble_map = {
            ("body", "head"): "#robot1_body_head.png"
        }

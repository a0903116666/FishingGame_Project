import pygame
import system.BaseClass as BaseClass
import system.UI as UI
import system.Engine as Engine
from config import WINDOW_WIDTH, WINDOW_HEIGHT

class HomePage(BaseClass.GameObject):
    def __init__(self):
        super().__init__(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.texture = Engine.get_image("game/assets/homepage_menu.png")
        Engine.object_pools["homepage"] = [
            self,
            UI.Button(
                WINDOW_WIDTH / 2, 
                WINDOW_HEIGHT / 2 - 25,
                200,
                80,
                "game/assets/GameStart_button.png",
                lambda: Engine.static_object["CutScene"][1].swap_scene(["main"]),
                Engine.static_object["Cursor"][1]
                ),
            UI.Button(
                WINDOW_WIDTH / 2, 
                WINDOW_HEIGHT / 2 + 50,
                200,
                80,
                "game/assets/DigitalFieldGuide_button.png",
                lambda: Engine.static_object["CutScene"][1].swap_scene(["gallery", "1star"], True),
                Engine.static_object["Cursor"][1]
                ),
            UI.Button(
                WINDOW_WIDTH / 2, 
                WINDOW_HEIGHT / 2 + 125,
                200,
                80,
                "game/assets/GameExit_button.png",
                lambda :setattr(Engine, 'running', False),
                Engine.static_object["Cursor"][1]
                ),
        ]
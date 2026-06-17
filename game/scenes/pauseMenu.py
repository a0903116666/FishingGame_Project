import pygame
import system.BaseClass as BaseClass
import system.UI as UI
import system.Engine as Engine
import system.Math as Math
from config import WINDOW_WIDTH, WINDOW_HEIGHT, TITLE_FONT, DESC_FONT

class PauseMenu(BaseClass.GameObject):
    def __init__(self):
        super().__init__(WINDOW_WIDTH / 2, -WINDOW_HEIGHT / 2, 400, 440)
        
        self.texture = Engine.get_image("game/assets/game_menu.png")
        Engine.static_object["pause-menu"] = (2, self)
        Engine.static_object["pause-homepage"] = (2, UI.Button(
            self.x, self.y - 90,
            300, 120,
            "game/assets/backtohomepage_button.png",
            lambda: self.press(["homepage"]),
            Engine.static_object["Cursor"][1]
        ))
        Engine.static_object["pause-gallery"] = (2, UI.Button(
            self.x, self.y - 15,
            300, 120,
            "game/assets/gotodigitalfieldguide_button.png",
            lambda: self.press(["gallery", "1star"]),
            Engine.static_object["Cursor"][1]
        ))
        Engine.static_object["pause-exit"] = (2, UI.Button(
            self.x, self.y + 60,
            300, 120,
            "game/assets/exitgame_button.png",
            lambda :setattr(Engine, "running", False),
            Engine.static_object["Cursor"][1]
        ))

    def press(self, pools):
        Engine.pauseMenu = False
        Engine.static_object["CutScene"][1].swap_scene(pools, True)
    
    def update(self):
        if "homepage" in Engine.working_pools or "gallery" in Engine.working_pools:
            Engine.pauseMenu = False
        Engine.pause = Engine.pauseMenu
        if Engine.pauseMenu:
            self.y = Math.clamp(Math.lerp(self.y, WINDOW_HEIGHT / 2 + 20, Engine.delta_time * 20), -WINDOW_HEIGHT, WINDOW_HEIGHT / 2)
        else:
            self.y = Math.lerp(self.y, -WINDOW_HEIGHT / 2 - 20, Engine.delta_time * 20)

        Engine.static_object["pause-homepage"][1].y = self.y - 90
        Engine.static_object["pause-gallery"][1].y = self.y - 15
        Engine.static_object["pause-exit"][1].y = self.y + 60
        if self.y < -WINDOW_HEIGHT / 2:
            Engine.static_object["pause-homepage"][1]
            Engine.static_object["pause-gallery"][1]
            Engine.static_object["pause-exit"][1]

    def render(self, screen):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150 * Math.clamp(self.y / WINDOW_HEIGHT + 0.5, 0, 1)))
        screen.blit(overlay, (0, 0))
        super().render(screen)
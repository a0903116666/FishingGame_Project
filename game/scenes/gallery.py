import json
import time
import pygame
import system.BaseClass as BaseClass
import system.UI as UI
import system.Engine as Engine
import system.Math as Math
from config import WINDOW_WIDTH, WINDOW_HEIGHT, CUTSCENE_DURATION

class Display(BaseClass.GameObject):
    def __init__(self):
        super().__init__(WINDOW_WIDTH / 2, -WINDOW_HEIGHT / 2, 700, 400)
        self.texture = Engine.get_image("game/assets/display_icon-removebg-preview.png")
        self.enabled = False
        self.display = False
        self.close_button = UI.Button(
            WINDOW_WIDTH / 2 + 275, -100, 180, 100, "game/assets/cross.png", self.close, Engine.static_object["Cursor"][1]
        )
        Engine.static_object["fish_display"] = (2, self)
        Engine.static_object["close_button"] = (1, self.close_button)
        self.close_button.enabled = False
    
    def show_record(self, record):
        self.y = -WINDOW_HEIGHT / 2
        self.close_button.enabled = True
        self.enabled = True
        self.display = True
        Engine.pause = True
    
    def close(self):
        self.display = False
        Engine.pause = False
    
    def update(self):
        if self.display:
            self.y = int(Math.lerp(self.y, WINDOW_HEIGHT / 2, Engine.delta_time * 20))
        else:
            self.y = Math.lerp(self.y, -WINDOW_HEIGHT / 2 - 20, Engine.delta_time * 20)
        self.close_button.y = self.y - 200
        if self.y < -WINDOW_HEIGHT / 2:
            self.enabled = False
            self.close_button.enabled = False
    
    def render(self, screen):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150 * Math.clamp(self.y / WINDOW_HEIGHT + 0.5, 0, 1)))
        screen.blit(overlay, (0, 0))
        super().render(screen)

class Gallery(BaseClass.GameObject):
    def __init__(self):
        super().__init__(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.texture = Engine.get_image("game/assets/DigitalFieldGuide_background.png")
        Display()
        display = Engine.static_object["fish_display"][1]
        Engine.object_pools["gallery"] = [
            self,
            UI.StaticImage(
                WINDOW_WIDTH // 2 - 250, WINDOW_HEIGHT // 2 - 160,
                200, 80,
                "game/assets/button.png"
            ),
            UI.Button(
                WINDOW_WIDTH // 2 - 250,
                WINDOW_HEIGHT // 2 + 200,
                200, 80,
                "game/assets/backtohomepage_button.png",
                lambda :Engine.static_object["CutScene"][1].swap_scene(["homepage"], True),
                Engine.static_object["Cursor"][1]
            )
            ]
        for i in range(1, 6):
            Engine.spawn_entity(
                UI.Button(
                    WINDOW_WIDTH // 2 - 250,
                    WINDOW_HEIGHT // 2 - 160 + i * 60,
                    200, 80,
                    f"game/assets/{i}star.png",
                    lambda current_star = f"{i}star": Engine.change_pool(1, current_star, True),
                    Engine.static_object["Cursor"][1]
                ),
                f"gallery"
            )
            Engine.object_pools[f"{i}star"] = [
                UI.StaticImage(WINDOW_WIDTH // 2 + 100, WINDOW_HEIGHT // 2, 600, 440, f"game/assets/{i}star_column.png")
            ]
        
        try:
            with open('game/fishing_master_save.json', 'r', encoding='utf-8') as f:
                player_data = json.load(f)
                records = player_data.get("records", [])
        except FileNotFoundError:
            print("⚠️ 找不到 fishing_master_save.json，圖鑑將呈現空白狀態。")
            records = []
    
        fish_counters = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for record in records:
            fish_id = record["id"]
            is_unlocked = record["is_unlocked"]

            star_level = (fish_id // 100) + 1  
                
            if star_level > 5 or star_level < 1: 
                continue

            img_path = f"fish_img/fish_{fish_id}.png" if is_unlocked else f"fish_silhouette/fish_{fish_id}_silhouette.png"

            current_index = fish_counters[star_level]
            row, col = current_index // 5, current_index % 5
            button = UI.Button(
                    307 + col * 76,
                    150 + row * 90,
                    64, 64,
                    img_path,
                    lambda current_record = record: display.show_record(current_record),
                    Engine.static_object["Cursor"][1]
                )
            button.enabled = is_unlocked
            Engine.spawn_entity(
                button,
                f"{star_level}star"
            )
            
            fish_counters[star_level] += 1
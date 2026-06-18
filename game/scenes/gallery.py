import json
import time
import pygame
import system.BaseClass as BaseClass
import system.UI as UI
import system.Engine as Engine
import system.Math as Math
from config import WINDOW_WIDTH, WINDOW_HEIGHT, TITLE_FONT, DESC_FONT, game_save
from fish_data import get_fish_data, FISH_MASTER_DATA

class Display(BaseClass.GameObject):
    def __init__(self):
        super().__init__(WINDOW_WIDTH / 2, -WINDOW_HEIGHT / 2, 700, 400)
        self.texture = Engine.get_image("game/assets/display_icon-removebg-preview.png")
        self.enabled = False
        self.display = False
        self.close_button = UI.Button(
            WINDOW_WIDTH / 2 + 275, -100, 180, 100, "game/assets/cross.png", self.close, Engine.static_object["Cursor"][1]
        )
        self.fish_img = UI.StaticImage(self.x, -WINDOW_HEIGHT, 96, 96, None)
        Engine.static_object["fish_display"] = (2, self)
        Engine.static_object["close_button"] = (1, self.close_button)
        Engine.static_object["fish_image"] = (1, self.fish_img)
        self.fish_id = None
        self.master_data = None
        self.close_button.enabled = False
        self.fish_img.enabled = False
        self.record = None
    
    def show_record(self, record):
        self.y = -WINDOW_HEIGHT / 2
        self.close_button.enabled = True
        self.enabled = True
        self.display = True
        self.record = record
        self.fish_id = self.record["id"]
        self.master_data = get_fish_data(self.fish_id)
        self.json_data = game_save.get_fish_save_data(self.fish_id)
        self.fish_img.enabled = True
        self.fish_img.texture = Engine.get_image(f"fish_img/fish_{self.fish_id}.png")
        Engine.pause = True
    
    def close(self):
        self.display = False
        Engine.pause = False
    
    def update(self):
        if self.display:
            self.y = Math.clamp(Math.lerp(self.y, WINDOW_HEIGHT / 2 + 20, Engine.delta_time * 20), -WINDOW_HEIGHT, WINDOW_HEIGHT / 2)
        else:
            self.y = Math.lerp(self.y, -WINDOW_HEIGHT / 2 - 20, Engine.delta_time * 20)
        self.close_button.y = self.y - 200
        if self.y < -WINDOW_HEIGHT / 2:
            self.enabled = False
            self.close_button.enabled = False
            self.fish_img.enabled = False
    
    def render(self, screen):
        if not self.enabled: return
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150 * Math.clamp(self.y / WINDOW_HEIGHT + 0.5, 0, 1)))
        screen.blit(overlay, (0, 0))
        super().render(screen)
        if self.record == None: return
        
        title_color = (60, 40, 20)
        desc_color = (100, 80, 60)

        # 🐟 畫魚的名字 (置中於寶藏圖上方的橫幅)
        title_surface = TITLE_FONT.render(self.master_data["name"], True, title_color)
        title_x = self.x - (title_surface.get_width() // 2)
        title_y = self.y - 190 # 依據你的橫幅高度微調
        screen.blit(title_surface, (title_x, title_y))

        # 🐟 畫星級 (置中於畫框下方)
        level_surface = DESC_FONT.render(f"星級: {self.master_data['level']}  捕獲次數: {self.json_data['catch_count']}  最大重量: {self.json_data['max_weight']}", True, title_color)
        level_x = self.x - (level_surface.get_width() // 2)
        level_y = self.y + 140 # 從底部往上推
        screen.blit(level_surface, (level_x, level_y))

        # 🐟 畫介紹筆記 (每 16 個字換行，並置中對齊)
        full_text = self.master_data["comment"]
        lines = []
        
        for i in range(0, len(full_text), 20):
            single_line = full_text[i:i+20]
            lines.append(single_line)
            
        base_y = self.y + 50  # 第一行文字的起始 Y 座標
        line_height = 28  # 每行文字之間的高度差 (可依據你的字體大小微調這個數字)
        
        for index in range(len(lines)):
            line_text = lines[index]
            comment_surface = DESC_FONT.render(line_text, True, desc_color)
            comment_x = self.x - (comment_surface.get_width() // 2)
            comment_y = base_y + (index * line_height)
            screen.blit(comment_surface, (comment_x, comment_y))
        
        self.fish_img.y = self.y - 42

class Gallery(BaseClass.GameObject):
    def __init__(self):
        super().__init__(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.texture = Engine.get_image("game/assets/DigitalFieldGuide_background.png")
        Display()
        Engine.object_pools["gallery"] = [self]
        self.display = Engine.static_object["fish_display"][1]
    
    def start(self):
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
                    lambda current_record = record: self.display.show_record(current_record),
                    Engine.static_object["Cursor"][1]
                )
            button.enabled = is_unlocked
            Engine.spawn_entity(
                button,
                f"{star_level}star"
            )
            
            fish_counters[star_level] += 1
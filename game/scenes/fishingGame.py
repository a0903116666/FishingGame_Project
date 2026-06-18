import pygame
import math
import random
import system.BaseClass as BaseClass
import system.UI as UI
import system.Engine as Engine
import system.Math as Math
from config import WINDOW_WIDTH, WINDOW_HEIGHT, TITLE_FONT, DESC_FONT
import config
from fish_data import FISH_MASTER_DATA, get_fish_data

class FishAnimation(BaseClass.GameObject):
    def __init__(self):
        super().__init__(WINDOW_WIDTH / 2, 0, 400, 400)
        self.texture = Engine.get_image("game/assets/pixel_fish.png")
        self.angleStack = 0
        self.jumpingStack = 0
        self.jumpMag = 0
        self.angleMag = 0
        self.progress = 0
    
    def start(self):
        self.angleStack = 0
        self.jumpingStack = 0
        self.angleMag = 0
        self.jumpMag = 0
        self.progress = 0
    
    def update_value(self, progress):
        self.progress = progress
        self.angleStack += (progress * 5) * 15 * Engine.delta_time * random.uniform(0.8, 1)
        self.jumpingStack += (progress + 1) * 20 * Engine.delta_time * random.uniform(0.8, 1)
        self.jumpMag = (1 - progress) * 50
        self.angleMag = (1 - progress) * 10 + 5
    
    def render(self, screen):
        angle = math.sin(self.angleStack) * self.angleMag
        jump = math.sin(self.jumpingStack) * self.jumpMag
        rotated = pygame.transform.rotate(self.texture, angle)
        arc_rect = rotated.get_rect(center=(200 + math.sin(math.radians(angle)) * 180, 200 - abs(math.cos(math.radians(angle))) * 180))
        arc_rect.y += (1 - self.progress) * (WINDOW_HEIGHT + 50) - jump
        arc_rect.x += WINDOW_WIDTH / 4
        screen.blit(rotated, arc_rect)

class SettleMenu(BaseClass.GameObject):
    def __init__(self, fish_id, weight, is_new_record, is_new_species):
        super().__init__(WINDOW_WIDTH / 2, -WINDOW_HEIGHT / 2, 650, 440)
        
        self.texture = Engine.get_image("game/assets/settle_column2.png")
        
        self.fish_id = fish_id
        self.weight = weight
        self.is_new_record = is_new_record
        self.is_new_species = is_new_species
        
        self.continue_button = UI.Button(
            WINDOW_WIDTH / 2 + 125, self.y,
            250, 100,
            "game/assets/continue_button.png",
            lambda: Engine.static_object["CutScene"][1].swap_scene(["main"]),
            Engine.static_object["Cursor"][1]
        )
        self.gallery_button = UI.Button(
            WINDOW_WIDTH / 2 - 125, self.y,
            250, 100,
            "game/assets/gotoguide_button.png",
            lambda: Engine.static_object["CutScene"][1].swap_scene(["gallery", "1star"], True),
            Engine.static_object["Cursor"][1]
        )
        self.new_species_img = UI.StaticImage(
            WINDOW_WIDTH // 2 + 170, self.y - 70,
            300, 150,
            "game/assets/new_species.png",
        )
        self.new_record_img = UI.StaticImage(
            WINDOW_WIDTH // 2 + 170, self.y - 70, 
            300, 150,
            "game/assets/new_record.png",
        )
        self.fish_img = UI.StaticImage(
            250, self.y,
            128, 128,
            f"fish_img/fish_{self.fish_id}.png",
        )
        
        Engine.object_pools["settle"] = [
            self,
            self.continue_button,
            self.gallery_button,
            self.fish_img,
            self.new_species_img,
            self.new_record_img,
        ]
        Engine.add_pools(["settle"])
        
        if not is_new_species: Engine.destroy_entity(self.new_species_img, "settle")
        if not is_new_record or is_new_species: Engine.destroy_entity(self.new_record_img, "settle")
        
        self.master_data = get_fish_data(self.fish_id)
    
    def update(self):
        self.y = Math.clamp(Math.lerp(self.y, WINDOW_HEIGHT / 2 + 20, Engine.delta_time * 5), -WINDOW_HEIGHT, WINDOW_HEIGHT / 2)
        self.continue_button.y = self.y + 145
        self.gallery_button.y = self.y + 145
        self.new_record_img.y = self.y - 150
        self.new_species_img.y = self.y - 150
        self.fish_img.y = self.y - 36

    def render(self, screen):
        if not self.enabled: return
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150 * Math.clamp(self.y / WINDOW_HEIGHT + 0.5, 0, 1)))
        screen.blit(overlay, (0, 0))
        super().render(screen)
        title_color = (60, 40, 20)
        desc_color = (100, 80, 60)
    
        title_surface = TITLE_FONT.render("釣魚結算", True, title_color)
        title_x = WINDOW_WIDTH // 2 - (title_surface.get_width() // 2)
        title_y = (WINDOW_HEIGHT // 2) - 200  + self.y - WINDOW_HEIGHT / 2
        screen.blit(title_surface, (title_x, title_y))

        text_start_x = (WINDOW_WIDTH // 2) + 20
        base_y = (WINDOW_HEIGHT // 2) - 80 + self.y - WINDOW_HEIGHT / 2
        line_spacing = 40
        fish = get_fish_data(int(self.fish_id))

        name_surface = DESC_FONT.render(f"魚名：{fish['name']}", True, desc_color)
        screen.blit(name_surface, (text_start_x, base_y))

        weight_surface = DESC_FONT.render(f"重量：{self.weight} kg", True, desc_color)
        screen.blit(weight_surface, (text_start_x, base_y + line_spacing * 1))

        rarity_surface = DESC_FONT.render(f"稀有度：{fish['level']}", True, desc_color)
        screen.blit(rarity_surface, (text_start_x, base_y + line_spacing * 2))

class FishingGame(BaseClass.GameObject):
    def __init__(self):
        super().__init__(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.texture = Engine.get_image("game/assets/undersea_background.png")
        self.hook = UI.StaticImage(
                65, 0, 80, 45,
                "game/assets/hook.png"
            )
        self.animation = FishAnimation()
        Engine.object_pools["fishing"] = [
            self,
            self.hook,
            self.animation
            ]
        self.star = 1
        self.progress = 0
        self.box_y = 300
        self.box_size = 100
        self.progress_color = 0
        self.progress = 0.2
        self.min_speed = 20
        self.max_speed = 50
        self.min_cooldown = 5
        self.max_cooldown = 7
        self.box_speed = 0
        self.cooldown = self.max_cooldown
        self.progress_gain = 0.3
        self.progress_loss = 0.2
        self.cursor_pixel = 300
    
    def update(self):
        self.cursor_pixel = Math.clamp(Engine.static_object["Cursor"][1].y, 50, WINDOW_HEIGHT - 50)
        self.animation.update_value(self.progress)
        self.hook.y = self.cursor_pixel

        if abs(self.cursor_pixel - self.box_y) < self.box_size // 2:
            self.progress += self.progress_gain * Engine.delta_time
            self.progress_color = (0, 255, 0)
        else:
            self.progress -= self.progress_loss * Engine.delta_time
            self.progress_color = (255, 0, 0)
                
        self.progress = Math.clamp(self.progress, 0, 1)
        
        if self.progress == 1:
            self.success()
        elif self.progress == 0:
            self.failed()

        if self.cooldown > 0:
            self.cooldown -= Engine.delta_time
        if self.box_y >= WINDOW_HEIGHT - 50 - self.box_size // 2:
            self.box_y = WINDOW_HEIGHT - 49 - self.box_size // 2
            self.box_speed = -random.uniform(self.min_speed, self.max_speed)
            self.cooldown = random.uniform(self.min_cooldown, self.max_cooldown)
        elif self.box_y <= 50 + self.box_size // 2:
            self.box_y = 51 + self.box_size // 2
            self.box_speed = random.uniform(self.min_speed, self.max_speed)
            self.cooldown = random.uniform(self.min_cooldown, self.max_cooldown)
        else:
            if self.cooldown <= 0:
                self.box_speed = random.uniform(self.min_speed, self.max_speed) * random.choice([-1, 1])
                self.cooldown = random.uniform(self.min_cooldown, self.max_cooldown)
        self.box_y += self.box_speed * Engine.delta_time

        if self.cooldown > 0:
                self.cooldown -= Engine.delta_time
    
    def start(self):
        self.enabled = True
        stars = [1, 2, 3, 4, 5]
        weights = [0.2, 0.3, 0.25, 0.2, 0.05]
        self.star = random.choices(stars, weights=weights)[0]
        self.difficulty()
    
    def success(self):
        if self.star == 1: 
            fish_id = random.randint(1, 7)
        elif self.star == 2: 
            fish_id = random.randint(101, 115)
        elif self.star == 3: 
            fish_id = random.randint(201, 215)
        elif self.star == 4: 
            fish_id = random.randint(301, 315)
        elif self.star == 5: 
            fish_id = random.randint(401, 405)
        for fish in FISH_MASTER_DATA["fish_list"]:
            if fish["id"] == fish_id:
                min_weight = fish["min_weight_kg"]
                max_weight = fish["max_weight_kg"]
                break
        captured_weight = round(random.uniform(min_weight, max_weight), 2)
        data = config.game_save.get_fish_save_data(fish_id)
        is_new_record = False
        is_new_species = False
        if captured_weight > data["max_weight"]:
            is_new_record = True
        if not data["is_unlocked"]:
            is_new_species = True
        config.game_save.on_fish_caught(fish_id, captured_weight)
        print("caught", fish_id)
        SettleMenu(
            fish_id,
            captured_weight,
            is_new_record,
            is_new_species
        )
        self.enabled = False
    
    def failed(self):
        self.enabled = False
        Engine.static_object["CutScene"][1].swap_scene(["main"])
    
    def difficulty(self):
        if self.star == 1:
            self.progress = 0.2
            self.box_size = 200
            self.min_speed = 20
            self.max_speed = 50
            self.min_cooldown = 5
            self.max_cooldown = 7
            self.progress_gain = 0.3
            self.progress_loss = 0.2
            
        if self.star == 2:
            self.progress = 0.5
            self.box_size = 130
            self.min_speed = 80
            self.max_speed = 150
            self.min_cooldown = 2
            self.max_cooldown = 4
            self.progress_gain = 0.3
            self.progress_loss = 0.4
            
        if self.star == 3:
            self.progress = 0.5
            self.box_size = 100
            self.min_speed = 100
            self.max_speed = 200
            self.min_cooldown = 1
            self.max_cooldown = 3
            self.progress_gain = 0.3
            self.progress_loss = 0.4
            
        if self.star == 4:
            self.progress = 0.5
            self.box_size = 100
            self.min_speed = 150
            self.max_speed = 250
            self.min_cooldown = 0.2
            self.max_cooldown = 1.5
            self.progress_gain = 0.3
            self.progress_loss = 0.5
            
        if self.star == 5:
            self.progress = 0.7
            self.box_size = 100
            self.min_speed = 150
            self.max_speed = 300
            self.min_cooldown = 0.2
            self.max_cooldown = 1
            self.progress_gain = 0.3
            self.progress_loss = 0.6
        
        self.cooldown = self.max_cooldown
        self.box_speed = random.uniform(self.min_speed, self.max_speed) * random.choice([-1, 1])
    
    def render(self, screen):
        super().render(screen)
        pygame.draw.rect(
            surface=screen,
            color=(150, 0, 150),
            rect=(50, self.box_y - self.box_size//2, 30, self.box_size),
            width=0
        )
        pygame.draw.rect(
            surface=screen, 
            color=(255, 165, 0), 
            rect=(50, 50, 30, WINDOW_HEIGHT - 100),
            width=2
        )
        # pygame.draw.circle(
        #     surface=screen, 
        #     color=(255, 0, 0), 
        #     center=(65, int(self.cursor_pixel)),
        #     radius=10
        # )
        pygame.draw.rect(
            surface=screen,
            color=self.progress_color,
            rect=(WINDOW_WIDTH - 80, WINDOW_HEIGHT - (WINDOW_HEIGHT - 100) * self.progress - 50, 30, (WINDOW_HEIGHT - 100) * self.progress),
            width=0
        )
        pygame.draw.rect(
            surface=screen, 
            color=(255, 165, 0), 
            rect=(WINDOW_WIDTH - 80, 50, 30, WINDOW_HEIGHT - 100),
            width=2
        )
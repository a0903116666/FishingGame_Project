import pygame
import random
import system.BaseClass as BaseClass
import system.UI as UI
import system.Engine as Engine
import system.Math as Math
import entities.fishBox as fishBox
import entities.particles as particles
from config import WINDOW_WIDTH, WINDOW_HEIGHT
import config
from fish_data import FISH_MASTER_DATA

class FishingGame(BaseClass.GameObject):
    def __init__(self):
        super().__init__(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, WINDOW_WIDTH, WINDOW_HEIGHT)
        Engine.object_pools["fishing"] = [
            self,
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
        stars = [1, 2, 3, 4, 5]
        weights = [1, 0, 0, 0, 0]
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
        config.game_save.on_fish_caught(fish_id, captured_weight)
        print("caught", fish_id)
        Engine.static_object["CutScene"][1].swap_scene(["main"])
    
    def failed(self):
        print("魚跑走了...")
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
        screen.fill((0, 105, 255))
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
        pygame.draw.circle(
            surface=screen, 
            color=(255, 0, 0), 
            center=(65, int(self.cursor_pixel)),
            radius=10
        )
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
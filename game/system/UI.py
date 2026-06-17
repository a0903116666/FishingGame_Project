import pygame
import time
from config import *
import system.Engine as Engine
import system.Math as Math
from system.BaseClass import *

class AnimationObject(GameObject):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.startTime = 0
        
    def start(self):
        self.startTime = time.time()

class Cursor(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, CURSOR_SIZE, CURSOR_SIZE)
        self.hover: Button = None
        self.last_hover: Button = None
        self.clicked: Button = None
        self.hover_ratio: float = 0
        self.hover_start: float = 0
        self.texture: pygame.Surface = Engine.get_image("game/assets/HandCursor.png")
        self.cursor_hint_image: pygame.Surface = Engine.get_image("game/assets/ProgressArc.png")
    
    def update(self):
        if not USE_BODY_TRACKING:
            self.x, self.y = pygame.mouse.get_pos()
        
        if self.hover and self.last_hover == self.hover:
            self.hover_ratio = (time.time() - self.hover_start) / HOVER_TIME
        else:
            self.hover_ratio = 0
            self.hover_start = time.time()
        if self.hover_ratio >= 1:
            self.hover.click()
            self.clicked = self.hover
            self.hover = None
            
        self.last_hover = self.hover
 
    def render(self, screen):
        if self.hover_ratio > 0.0:
            for i in range(int(self.hover_ratio * 8 + 0.5)):
                rotated_arc = pygame.transform.rotate(self.cursor_hint_image, -45 * i)
                arc_rect = rotated_arc.get_rect(center=(self.x, self.y))
                screen.blit(rotated_arc, arc_rect)

        super().render(screen)

class Button(GameObject):
    def __init__(self, x, y, w, h, image_path: str, func, cursor: Cursor):
        super().__init__(x, y, w, h)
        self.w = w
        self.h = h
        self.origin_w = w
        self.origin_h = h
        self.smoothing = 1
        self.texture = Engine.get_image(image_path) if image_path else None
        self.onClick = func
        self.cursor = cursor
        self.enabled = True
    
    def start(self):
        self.w = self.origin_w
        self.h = self.origin_h
        self.smoothing = 1
    
    def update(self):
        if self.enabled and self.cursor.clicked != self and abs(self.cursor.x - self.x) < self.w / 2 and abs(self.cursor.y - self.y) < self.h / 2:
            self.cursor.hover = self
            self.smoothing = Math.lerp(self.smoothing, 1.2, Engine.delta_time * 20)
        else:
            self.smoothing = Math.lerp(self.smoothing, 1, Engine.delta_time * 20)
            if self.cursor.hover == self:
                self.cursor.hover = None
        self.w = int(self.origin_w * self.smoothing)
        self.h = int(self.origin_h * self.smoothing)
    
    def click(self):
        self.onClick()
    
class StaticImage(GameObject):
    def __init__(self, x, y, w, h, image_path):
        super().__init__(x, y, w, h)
        self.texture = Engine.get_image(image_path)

class CutScene(GameObject):
    def __init__(self):
        super().__init__(0, -WINDOW_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.start_time = 0
        self.enabled = False
        self.swapped = False
        self.to_pools = []
        self.initialize = False
    
    def swap_scene(self, to_pools: list[str], initialize = True):
        self.y = -WINDOW_HEIGHT
        self.swapped = False
        self.initialize = initialize
        self.enabled = True
        self.start_time = time.time()
        self.to_pools = to_pools
        Engine.pause = True
    
    def update(self):
        ratio = (time.time() - self.start_time) / CUTSCENE_DURATION
        self.y = ratio * WINDOW_HEIGHT - WINDOW_HEIGHT
        if not self.swapped and ratio >= 1:
            self.swapped = True
            if self.initialize:
                Engine.init_pools(self.to_pools)
            Engine.working_pools = self.to_pools
        if ratio >= 2:
            Engine.pause = False
            self.enabled = False
    
    def render(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (0, self.y, WINDOW_WIDTH, WINDOW_HEIGHT))
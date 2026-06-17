import pygame

class GameObject:
    def __init__(self, x, y, w, h):
        self.destroy = False
        self.enabled = True
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.texture: pygame.Surface = None

    def start(self):
        pass

    def update(self):
        pass

    def end(self):
        pass
    
    def render(self, screen: pygame.Surface):
        if self.texture:
            screen.blit(
                pygame.transform.smoothscale(self.texture, (self.w, self.h)), 
                (self.x - self.w / 2, 
                self.y - self.h / 2)
                )
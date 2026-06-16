import math
import random
from config import *

class Circle:
    def __init__(self, x, y, radius, color=(255, 50, 50), speed_x=5, speed_y=5, score=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = color
        self.score = score
        self.cooldown = 0.1

    def update_particle(self, delta_time, particle_list):
        self.cooldown -= delta_time
        if self.cooldown <= 0:
            self.cooldown = 0.1
            direction = random.random() * 2 * math.pi
            offset = random.randint(10, 20)
            particle_list.append(
                Particle(
                    self.x + math.cos(direction) * offset,
                    self.y + math.sin(direction) * offset,
                    50,
                )
            )
            # if len(particle_list) >= 10 or len(particle_list) == 0:
            #     return
    def move(self, delta_time):
        self.x += self.speed_x * delta_time
        self.y += self.speed_y * delta_time
        if self.x < 0 or self.x > WINDOW_WIDTH:
            self.speed_x *= -1
            self.x = max(1, min(self.x, WINDOW_WIDTH - 1))
        if self.y < 0 or self.y > WINDOW_HEIGHT:
            self.speed_y *= -1
            self.y = max(1, min(self.y, WINDOW_HEIGHT - 1))

class Particle:
    def __init__(self, x, y, init_size):
        self.x = x
        self.y = y
        self.init_size = init_size
        self.size = init_size
        self.init_lifetime = 0.5
        self.lifetime = 0.5
    
    def update(self, delta_time):
        self.lifetime -= delta_time
        if self.lifetime <= 0:
            return
        self.size = self.init_size * (self.lifetime / self.init_lifetime)
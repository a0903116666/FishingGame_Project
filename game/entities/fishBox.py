import random
import math
import system.BaseClass as BaseClass
import entities.particles as particle
import system.Engine as Engine
from config import WINDOW_WIDTH, WINDOW_HEIGHT

class FishBox(BaseClass.GameObject):
    def __init__(self,
        radius,
        particle_system: particle.Particles, 
        target: BaseClass.GameObject
        ):
        super().__init__(0, 0, 40, 40)
        self.enabled = True
        self.radius = radius
        self.cooldown = 0.1
        self.particle_system = particle_system
        self.target = target
    
    def start(self):
        self.reset()
    
    def update(self):
        self.move()
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = (dx**2 + dy**2) ** 0.5
        
        if distance < self.radius:
            self.reset()
            Engine.static_object["CutScene"][1].swap_scene(["fishing"], True)
        
        self.cooldown -= Engine.delta_time
        if self.cooldown <= 0:
            self.cooldown = 0.1
            direction = random.random() * 2 * math.pi
            offset = random.randint(10, 20)
            self.particle_system.spawn_particle(
                self.x + math.cos(direction) * offset,
                self.y + math.sin(direction) * offset
            )
    
    def reset(self):
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = random.randint(0, WINDOW_HEIGHT)
        self.radius = random.randint(5, 15)
        self.speed_x = random.choice([-1, 1]) * random.randint(20, 100)
        self.speed_y = random.choice([-1, 1]) * random.randint(20, 100)
            
    def move(self):
        self.x += self.speed_x * Engine.delta_time
        self.y += self.speed_y * Engine.delta_time
        if self.x < 0 or self.x > WINDOW_WIDTH:
            self.speed_x *= -1
            self.x = max(1, min(self.x, WINDOW_WIDTH - 1))
        if self.y < 0 or self.y > WINDOW_HEIGHT:
            self.speed_y *= -1
            self.y = max(1, min(self.y, WINDOW_HEIGHT - 1))
import system.BaseClass as BaseClass
import system.UI as UI
import system.Engine as Engine
from config import WINDOW_WIDTH, WINDOW_HEIGHT

class Bubble(BaseClass.GameObject):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        self.texture = Engine.get_image("game/assets/bubble.png")
        self.init_size = size
        self.init_lifetime = 0.5
        self.lifetime = 0.5
    
    def update(self):
        self.lifetime -= Engine.delta_time
        if self.lifetime <= 0:
            self.enabled = False
        else:
            self.w = self.h = self.init_size * (self.lifetime / self.init_lifetime)

class Particles(BaseClass.GameObject):
    def __init__(self, pool: str):
        super().__init__(0, 0, 0, 0)
        self.particle_pool: list[Bubble] = []
        self.pool = pool
    
    def update(self):
        to_delete = []
        for particle in self.particle_pool:
            if particle.lifetime <= 0:
                to_delete.append(particle)
        for delete in to_delete:
            self.particle_pool.remove(delete)
            Engine.destroy_entity(delete, self.pool)
    
    def spawn_particle(self, x, y):
        if len(self.particle_pool) <= 10:
            bubble = Bubble(x, y, 50)
            self.particle_pool.append(
                bubble
            )
            Engine.spawn_entity(bubble, self.pool)
    
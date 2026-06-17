import system.BaseClass as BaseClass
import system.Math as Math
import system.Engine as Engine
import entities.fishBox as fishBox
import entities.particles as particles
from config import WINDOW_WIDTH, WINDOW_HEIGHT

class Bobber(BaseClass.GameObject):
    def __init__(self, target: BaseClass.GameObject):
        super().__init__(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 64, 64)
        self.target = target
        self.texture = Engine.get_image("game/assets/bobber.png")
    
    def update(self):
        self.x += (self.target.x / WINDOW_WIDTH - 0.5) * 300 * Engine.delta_time
        self.y += (self.target.y / WINDOW_HEIGHT - 0.5) * 300 * Engine.delta_time
        self.x = Math.clamp(self.x, 0, WINDOW_WIDTH)
        self.y = Math.clamp(self.y, 0, WINDOW_HEIGHT)

class MainGame(BaseClass.GameObject):
    def __init__(self):
        super().__init__(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.texture = Engine.get_image("game/assets/warter_surface.png")
        particle_system = particles.Particles("main")
        bobber = Bobber(Engine.static_object["Cursor"][1])
        Engine.object_pools["main"] = [
            self,
            particle_system,
            bobber
        ]
        
        for i in range(5):
            Engine.spawn_entity(
                fishBox.FishBox(
                    20,
                    particle_system,
                    bobber
                ),
                "main"
            )
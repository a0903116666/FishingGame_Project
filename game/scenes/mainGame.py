import system.BaseClass as BaseClass
import system.UI as UI
import system.Engine as Engine
import entities.fishBox as fishBox
import entities.particles as particles
from config import WINDOW_WIDTH, WINDOW_HEIGHT

class MainGame(BaseClass.GameObject):
    def __init__(self):
        super().__init__(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.texture = Engine.get_image("game/assets/warter_surface.png")
        particle_system = particles.Particles("main")
        Engine.object_pools["main"] = [
            self,
            particle_system,
            ]
        
        for i in range(5):
            Engine.spawn_entity(
                fishBox.FishBox(
                    20,
                    particle_system,
                    Engine.static_object["Cursor"][1]
                ),
                "main"
            )
    
    # def render(self, screen):
    #     screen.fill((0, 255, 0))
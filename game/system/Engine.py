import pygame
from config import *
from system.BaseClass import *

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()

# 全域資料
global_data = {}

# 物件池
# key: 池名稱, value: 運作物件
object_pools: dict[str, list[GameObject]] = {}

# 常駐物件，在任何場景中運作，不受暫停影響
# key: 名稱, value: 物件
static_object: dict[str, tuple[int, GameObject]] = {}

# 運作中的物件池
working_pools: list[str] = []

pause = False
running = True
delta_time = 0

def get_image(filename: str):
    try:
        img = pygame.image.load(filename).convert_alpha()
        return img
    except FileNotFoundError:
        print(f"⚠️ 警告：找不到 {filename}，請確認有對應檔案。")        
        img = pygame.Surface((64, 64))
        img.fill((150, 0, 150))
        return img

def spawn_entity(gameObject: GameObject, pool: str):
    gameObject.start()
    object_pools[pool].append(gameObject)
    
def destroy_entity(gameObject: GameObject, pool: str):
    gameObject.end()
    object_pools[pool].remove(gameObject)

def update():
    for pool in working_pools:
        for obj in object_pools[pool]:
            if obj.enabled and not pause:
                obj.update()
    objs = []
    for t in static_object.values():
        if t[1].enabled:
            objs.append(t)
    objs.sort(key=lambda x:x[0], reverse=True)
    for obj in objs:
        obj[1].update()

def render():
    for pool in working_pools:
        for obj in object_pools[pool]:
                obj.render(SCREEN)
    objs = []
    for t in static_object.values():
        objs.append(t)
    objs.sort(key=lambda x:x[0], reverse=True)
    for obj in objs:
        obj[1].render(SCREEN)

def full():
    global delta_time
    SCREEN.fill((0, 0, 0))
    update()
    render()
    pygame.display.flip()
    delta_time = CLOCK.tick(FPS) / 1000

def add_pools(pools: list[str], initialize = False):
    working_pools.extend(pools)
    if initialize:
        for pool in pools:
            init_pools([pool])

def init_pools(pools: list[str]):
    for pool in pools:
        for obj in object_pools[pool]:
            obj.start()

def change_pool(index: int, name: str, initialize = False):
    working_pools[index] = name
    if initialize:
        init_pools([name])
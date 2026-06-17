import pygame
import system.Engine as Engine
from system.UI import Cursor, CutScene
from config import *
from scenes.homepage import HomePage
from scenes.mainGame import MainGame
from scenes.gallery import Gallery
from scenes.fishingGame import FishingGame
from scenes.pauseMenu import PauseMenu


pygame.init()
pygame.display.set_caption("2D 體感釣魚大師 - 全螢幕模式")

main_cursor = Cursor(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
Engine.static_object["Cursor"] = (0, main_cursor)
Engine.static_object["CutScene"] = (1, CutScene())

HomePage()
MainGame()
FishingGame()
Gallery()
PauseMenu()

Engine.working_pools = ["homepage"]
Engine.init_pools(["homepage"])

Engine.running = True
while Engine.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Engine.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Engine.pauseMenu = not Engine.pauseMenu
    Engine.full()
    # print(Engine.working_pools)
    
pygame.quit()
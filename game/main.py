import pygame
import sys
from entity import Circle
from main_game_system import main_game_init, main_game_update, main_game_render
from fishing_stage_system import fishing_stage_render, fishing_stage_update
from cutscene_system import fade_out_cutscene, fade_in_cutscene
import config
from config import *

pygame.init()

pygame.display.set_caption("2D 體感釣魚大師 - 全螢幕模式")

star_image = pygame.image.load(str("game/assets/1star.png")).convert_alpha()

running = True

main_circle = Circle(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 15, color=(255, 0, 0))

total_score = 0
font = pygame.font.SysFont(None, 36)

config.CLOCK.tick(FPS)
main_game_init()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    if config.GAME_STATE == MAIN_GAME:
        main_game_update()
        main_game_render()

    elif config.GAME_STATE == MINI_GAME:
        fishing_stage_render()
        fishing_stage_update()
    
    elif config.GAME_STATE == CUTSCENE_OUT:
        if config.CUTSCENE_STATE == CUTSCENE_FROM_MAIN_TO_FISHING:
            main_game_render()
        else:
            fishing_stage_render()
        fade_out_cutscene()
    elif config.GAME_STATE == CUTSCENE_IN:
        if config.CUTSCENE_STATE == CUTSCENE_FROM_MAIN_TO_FISHING:
            fishing_stage_render()
        else:
            main_game_render()
        fade_in_cutscene()
    else:
        print('Unhandled GAME_STATE:', config.GAME_STATE, end='\r')
    
    pygame.display.flip()
    config.DELTA_TIME = config.CLOCK.tick(FPS) / 1000

print('Exited main loop, quitting game.')
pygame.quit()
sys.exit()
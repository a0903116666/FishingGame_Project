import pygame
import config
from config import *
from fishing_stage_system import fishing_stage_init

is_initialized = False

PHASE_BLACK_DOWN = 1  
PHASE_WAIT = 2              

current_phase = PHASE_BLACK_DOWN
black_rect_h = 0   
rect_speed = 1000

start_wait_time = 0

def fade_out_cutscene():
    
    global CUTSCENE_STATE, is_initialized, current_phase, black_rect_h, start_wait_time

    if not is_initialized:
        config.GAME_STATE = CUTSCENE_OUT
        is_initialized = True
        current_phase = PHASE_BLACK_DOWN
        black_rect_h = 0   

    if current_phase == PHASE_BLACK_DOWN:
        black_rect_h += rect_speed * config.DELTA_TIME
        if black_rect_h >= WINDOW_HEIGHT:
            black_rect_h = WINDOW_HEIGHT
            current_phase = PHASE_WAIT
            start_wait_time = pygame.time.get_ticks()
    elif current_phase == PHASE_WAIT:
        if pygame.time.get_ticks() - start_wait_time >= 200:
            if config.CUTSCENE_STATE == CUTSCENE_FROM_MAIN_TO_FISHING:
                fishing_stage_init()
            config.GAME_STATE = CUTSCENE_IN
            is_initialized = False

    pygame.draw.rect(SCREEN, (0, 0, 0), (0, 0, WINDOW_WIDTH, black_rect_h))

def fade_in_cutscene():
    global is_initialized, black_rect_h, rect_speed

    if not is_initialized:
        black_rect_h = 0 
        is_initialized = True

    pygame.draw.rect(SCREEN, (0, 0, 0), (0, black_rect_h, WINDOW_WIDTH, WINDOW_HEIGHT))
        
    black_rect_h += rect_speed * config.DELTA_TIME
    if black_rect_h >= WINDOW_HEIGHT:
        black_rect_h = WINDOW_HEIGHT
        if config.CUTSCENE_STATE == CUTSCENE_FROM_MAIN_TO_FISHING:
            config.GAME_STATE = MINI_GAME
            config.CUTSCENE_STATE = CUTSCENE_FROM_FISHING_TO_MAIN
        else:
            config.GAME_STATE = MAIN_GAME
            config.CUTSCENE_STATE = CUTSCENE_FROM_MAIN_TO_FISHING
        is_initialized = False


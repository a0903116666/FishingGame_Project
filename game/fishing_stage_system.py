from body_control import body_cursor
import random
import pygame
import config
from config import *
from fish_data import FISH_MASTER_DATA


progress = 0.7
box_y = 300
box_speed = 100
box_size = 100
cooldown = 2
progress_corlor = (255, 0, 0)
cursor_pixel = 0

# 難度控制參數
min_speed = 150
max_speed = 300
min_cooldown = 0.2
max_cooldown = 2
progress_gain = 0.2
progress_loss = 0.2
choice = 0

def fishing_stage_init():
    global progress, box_y, box_speed, box_size, cooldown, progress_corlor, cursor_pixel, choice, background_image, resized_background_image, resized_hook_image

    stars = [1, 2, 3, 4, 5]
    weights = [1, 0, 0, 0, 0]
    choice = random.choices(stars, weights=weights)[0]

    if choice == 1: fish_one_star()
    elif choice == 2: fish_two_star()
    elif choice == 3: fish_three_star()
    elif choice == 4: fish_four_star()
    elif choice == 5: fish_five_star()

    progress_corlor = (255, 0, 0)
    _, cursor_y = body_cursor()
    cursor_pixel = max(min((cursor_y + 0.5) * WINDOW_HEIGHT, WINDOW_HEIGHT - 50), 50)
    background_image = pygame.image.load("game/assets/undersea_background.png").convert_alpha()
    resized_background_image = pygame.transform.smoothscale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    hook_image = pygame.image.load("game/assets/hook.png").convert_alpha()
    resized_hook_image = pygame.transform.smoothscale(hook_image, (50, 50))


def fishing_stage_render():
    global progress, box_y, box_size, progress_corlor, cursor_pixel, resized_background_image, resized_hook_image
    SCREEN.blit(resized_background_image, (0, 0))
    pygame.draw.rect(
            surface=SCREEN,
            color=(150, 0, 150),
            rect=(50, box_y - box_size//2, 30, box_size),
            width=0
        )
    pygame.draw.rect(
        surface=SCREEN, 
        color=(255, 165, 0), 
        rect=(50, 50, 30, WINDOW_HEIGHT - 100),
        width=2
    )
    # draw cursor with circle
    #pygame.draw.circle(
    #    surface=SCREEN, 
    #    color=(255, 0, 0), 
    #    center=(65, int(cursor_pixel)),
    #   radius=10
    #)
    SCREEN.blit(resized_hook_image, (40, int(cursor_pixel) - resized_hook_image.get_height() // 2))
    # progress bar render
    pygame.draw.rect(
        surface=SCREEN,
        color=progress_corlor,
        rect=(WINDOW_WIDTH - 80, WINDOW_HEIGHT - (WINDOW_HEIGHT - 100) * progress - 50, 30, (WINDOW_HEIGHT - 100) * progress),
        width=0
    )
    pygame.draw.rect(
        surface=SCREEN, 
        color=(255, 165, 0), 
        rect=(WINDOW_WIDTH - 80, 50, 30, WINDOW_HEIGHT - 100),
        width=2
    )
    
def fishing_stage_update():
    global progress, box_y, box_size, progress_corlor, box_speed, cooldown, cursor_pixel, choice

    _, cursor_y = body_cursor()
    cursor_pixel = max(min((cursor_y + 0.5) * WINDOW_HEIGHT, WINDOW_HEIGHT - 50), 50)

    if abs(cursor_pixel - box_y) < box_size // 2:
            progress += progress_gain * config.DELTA_TIME
            progress_corlor = (0, 255, 0)
    else:
        progress -= progress_loss * config.DELTA_TIME
        progress_corlor = (255, 0, 0)
            
    progress = max(0, min(1, progress))

    if cooldown > 0:
        cooldown -= config.DELTA_TIME
    if box_y >= WINDOW_HEIGHT - 50 - box_size // 2:
        box_y = WINDOW_HEIGHT - 49 - box_size // 2
        box_speed = -random.uniform(min_speed, max_speed)
        cooldown = random.uniform(min_cooldown, max_cooldown)
    elif box_y <= 50 + box_size // 2:
        box_y = 51 + box_size // 2
        box_speed = random.uniform(min_speed, max_speed)
        cooldown = random.uniform(min_cooldown, max_cooldown)
    else:
        if cooldown <= 0:
            box_speed = random.uniform(min_speed, max_speed) * random.choice([-1, 1])
            cooldown = random.uniform(min_cooldown, max_cooldown)
    box_y += box_speed * config.DELTA_TIME

    if cooldown > 0:
            cooldown -= config.DELTA_TIME

    if progress == 1:
        print("釣到魚了！")
        if choice == 1: 
            fish_id = random.randint(1, 7)
            for fish in FISH_MASTER_DATA["fish_list"]:
                if fish["id"] == fish_id:
                    min_weight = fish["min_weight_kg"]
                    max_weight = fish["max_weight_kg"]
                    break
            captured_weight = round(random.uniform(min_weight, max_weight), 2)
            config.game_save.on_fish_caught(fish_id, captured_weight)
        elif choice == 2: 
            fish_id = random.randint(101, 115)
            for fish in FISH_MASTER_DATA["fish_list"]:
                if fish["id"] == fish_id:
                    min_weight = fish["min_weight_kg"]
                    max_weight = fish["max_weight_kg"]
                    break
            captured_weight = round(random.uniform(min_weight, max_weight), 2)
            config.game_save.on_fish_caught(fish_id, captured_weight)
        elif choice == 3: 
            fish_id = random.randint(201, 215)
            for fish in FISH_MASTER_DATA["fish_list"]:
                if fish["id"] == fish_id:
                    min_weight = fish["min_weight_kg"]
                    max_weight = fish["max_weight_kg"]
                    break
            captured_weight = round(random.uniform(min_weight, max_weight), 2)
            config.game_save.on_fish_caught(fish_id, captured_weight)
        elif choice == 4: 
            fish_id = random.randint(301, 315)
            for fish in FISH_MASTER_DATA["fish_list"]:
                if fish["id"] == fish_id:
                    min_weight = fish["min_weight_kg"]
                    max_weight = fish["max_weight_kg"]
                    break
            captured_weight = round(random.uniform(min_weight, max_weight), 2)
            config.game_save.on_fish_caught(fish_id, captured_weight)
        elif choice == 5: 
            fish_id = random.randint(401, 405)
            for fish in FISH_MASTER_DATA["fish_list"]:
                if fish["id"] == fish_id:
                    min_weight = fish["min_weight_kg"]
                    max_weight = fish["max_weight_kg"]
                    break
            captured_weight = round(random.uniform(min_weight, max_weight), 2)
            config.game_save.on_fish_caught(fish_id, captured_weight)
        config.GAME_STATE = CUTSCENE_OUT
        config.CUTSCENE_STATE = CUTSCENE_FROM_FISHING_TO_MAIN
    if progress == 0:
        print("魚跑走了...")
        config.GAME_STATE = CUTSCENE_OUT
        config.CUTSCENE_STATE = CUTSCENE_FROM_FISHING_TO_MAIN

def fish_one_star():
    global progress, box_y, box_speed, box_size, cooldown, min_speed, max_speed, min_cooldown, max_cooldown, progress_gain, progress_loss
    print("發動一星魚！")
    progress = 0.2
    box_y = 300
    box_size = 200
    min_speed = 20
    max_speed = 50
    min_cooldown = 5
    max_cooldown = 7
    box_speed = random.uniform(min_speed, max_speed) * random.choice([-1, 1])
    cooldown = max_cooldown
    progress_gain = 0.3
    progress_loss = 0.2
def fish_two_star():
    global progress, box_y, box_speed, box_size, cooldown, min_speed, max_speed, min_cooldown, max_cooldown, progress_gain, progress_loss
    print("發動二星魚！")
    progress = 0.5
    box_y = 300
    box_size = 130
    min_speed = 80
    max_speed = 150
    min_cooldown = 2
    max_cooldown = 4
    box_speed = random.uniform(min_speed, max_speed) * random.choice([-1, 1])
    cooldown = max_cooldown
    progress_gain = 0.3
    progress_loss = 0.4
def fish_three_star():
    global progress, box_y, box_speed, box_size, cooldown, min_speed, max_speed, min_cooldown, max_cooldown, progress_gain, progress_loss
    print("發動三星魚！")
    progress = 0.5
    box_y = 300
    box_size = 100
    min_speed = 100
    max_speed = 200
    min_cooldown = 1
    max_cooldown = 3
    box_speed = random.uniform(min_speed, max_speed) * random.choice([-1, 1])
    cooldown = max_cooldown
    progress_gain = 0.3
    progress_loss = 0.4
def fish_four_star():
    global progress, box_y, box_speed, box_size, cooldown, min_speed, max_speed, min_cooldown, max_cooldown, progress_gain, progress_loss
    print("發動四星魚！")
    progress = 0.5
    box_y = 300
    box_size = 100
    min_speed = 150
    max_speed = 250
    min_cooldown = 0.2
    max_cooldown = 1.5
    box_speed = random.uniform(min_speed, max_speed) * random.choice([-1, 1])
    cooldown = max_cooldown
    progress_gain = 0.3
    progress_loss = 0.5
def fish_five_star():
    global progress, box_y, box_speed, box_size, cooldown, min_speed, max_speed, min_cooldown, max_cooldown, progress_gain, progress_loss
    print("發動五星魚！")
    progress = 0.7
    box_y = 300
    box_size = 100
    min_speed = 150
    max_speed = 300
    min_cooldown = 0.2
    max_cooldown = 1
    box_speed = random.uniform(min_speed, max_speed) * random.choice([-1, 1])
    cooldown = max_cooldown
    progress_gain = 0.3
    progress_loss = 0.6
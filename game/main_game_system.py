import random
import config
from config import *
from entity import Circle
from body_control import body_cursor, gesture_detection

def main_game_init():
    global bubble_image, main_circle, COLLECTABLES
    config.GAME_STATE = MAIN_GAME
    config.CUTSCENE_STATE = CUTSCENE_FROM_MAIN_TO_FISHING
    fish_amount = 5
    for i in range(fish_amount):
        x = random.randint(0, WINDOW_WIDTH)
        y = random.randint(0, WINDOW_HEIGHT)
        speed_x = random.choice([-1, 1]) * random.randint(50, 150)
        speed_y = random.choice([-1, 1]) * random.randint(50, 150)
        score = random.randint(1, 10)
        color = (random.randint(25*score, 255), random.randint(25*(10-score), 255), 0)
        circle = Circle(x, y, 20, color, speed_x=speed_x, speed_y=speed_y, score=score)
        COLLECTABLES.append(circle)
    bubble_image = pygame.image.load(str("game/assets/bubble.png")).convert_alpha()
    main_circle = Circle(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 15, color=(255, 0, 0))

def main_game_render():
    global PARTICLES ,bubble_image, main_circle
    SCREEN.fill((0, 105, 255))
    for particle in PARTICLES:
        particle_size = int(particle.size)
        particle_image = pygame.transform.smoothscale(bubble_image, (particle_size, particle_size))
        particle_position = (
            int(particle.x - particle_size / 2),
            int(particle.y - particle_size / 2),
        )
        SCREEN.blit(particle_image, particle_position)
    pygame.draw.circle(
            surface=SCREEN, 
            color=main_circle.color, 
            center=(int(main_circle.x), int(main_circle.y)), 
            radius=main_circle.radius
    )

def main_game_update():
    for collectable in COLLECTABLES:
        collectable.update_particle(config.DELTA_TIME, PARTICLES)

    for particle in PARTICLES:
        particle.update(config.DELTA_TIME)
        
    while len(PARTICLES) > 0:
        if PARTICLES[0].lifetime <= 0:
            PARTICLES.pop(0)
        else:
            break

    cursor_x, cursor_y = body_cursor()
    main_circle.speed_x = cursor_x * 1500
    main_circle.speed_y = cursor_y * 1500

    main_circle.move(config.DELTA_TIME)

    if main_circle.x < 0:
        main_circle.x = 0
        main_circle.speed_x = 0
    if main_circle.x > WINDOW_WIDTH:
        main_circle.x = WINDOW_WIDTH
        main_circle.speed_x = 0
    if main_circle.y < 0:
        main_circle.y = 0
        main_circle.speed_y = 0
    if main_circle.y > WINDOW_HEIGHT:
        main_circle.y = WINDOW_HEIGHT
        main_circle.speed_y = 0
        
    for collectable in COLLECTABLES:
        dx = main_circle.x - collectable.x
        dy = main_circle.y - collectable.y
        distance = (dx**2 + dy**2) ** 0.5
        
        if distance < main_circle.radius + collectable.radius:
            COLLECTABLES.remove(collectable)
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, WINDOW_HEIGHT)
            radius = random.randint(5, 15)
            speed_x = random.choice([-1, 1]) * random.randint(20, 100)
            speed_y = random.choice([-1, 1]) * random.randint(20, 100)
            score = random.randint(1, 10)
            color = (random.randint(25*score, 255), random.randint(25*(10-score), 255), 0)
            COLLECTABLES.append(Circle(x, y, radius, color, speed_x=speed_x, speed_y=speed_y, score=score))
            config.GAME_STATE = CUTSCENE_OUT
            config.CUTSCENE_STATE = CUTSCENE_FROM_MAIN_TO_FISHING

        collectable.move(config.DELTA_TIME)
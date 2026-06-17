import pygame
from save_system import FishingSaveSystem

game_save = FishingSaveSystem()

FPS = 60
SMOOTHING_FACTOR = 0.2  
WINDOW_WIDTH, WINDOW_HEIGHT = 720, 480

COLLECTABLES = []
PARTICLES = []

pygame.init()

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("2D 體感釣魚大師 - 全螢幕模式")

CLOCK = pygame.time.Clock()

DELTA_TIME = 0

GAME_STATE = 0
CUTSCENE_STATE = 0

HOME_MENU = 0
GAME_MENU = 5
MINI_GAME_MENU = 6
MAIN_GAME = 1
MINI_GAME = 2
CUTSCENE_OUT = 3
CUTSCENE_IN = 4

CUTSCENE_FROM_MAIN_TO_FISHING = 0
CUTSCENE_FROM_FISHING_TO_MAIN = 1
CUTSCENE_DURATION = 0.25

CURSOR_SIZE = 50
HOVER_TIME = 0.5
USE_BODY_TRACKING = False
pygame.mouse.set_visible(False)

TITLE_FONT = pygame.font.Font("game/assets/pixel_font.ttf", 32)
DESC_FONT = pygame.font.Font("game/assets/pixel_font.ttf", 20)
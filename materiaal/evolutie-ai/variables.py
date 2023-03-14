########################################
FPS = 200 # hoe hoger hoe sneller het spel gaat, mits je computer dat aankan

FITNESS_PENALTY = 2 # dit bepaalt hoe snel ze af gaan als ze te lang blijven hangen (omhoog is sneller afgaan)

LEVEL = 'level0_data.csv' # hier kun je het level veranderen
########################################

# CONSTANT VARIABLES
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
MAX_LEVELS = 3

BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)

# GLOBAL VARIABLES
generation = 0
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = True
start_intro = True
see_field_of_vision = True # to see the blue outline of what a bot sees
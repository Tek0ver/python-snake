FPS = 0
WINDOW_SIZE = 500 # Window size
GAME_GRID = 5 # Number of square for the grid
GAME_RESOLUTION = WINDOW_SIZE // GAME_GRID

# AI rewards (fitness)
REWARD_ALIVE_ONE_MORE_FRAME = 1
REWARD_EAT_FOOD = 10

# AI penelties (fitness)
PENALTY_HARD_STUCK = -1000 # not a indentation (when stuck in left/right/left/right/... or up/down/up/down/...)
PENALTY_HUNGER_DEATH = -1000 # not a indentation
PENALTY_WALL_TAIL_DEATH = -100

# debug mode (prints informations)
DEBUG = False
NO_FOOD = False
NO_GROW = True

FPS = 0
WINDOW_SIZE = 500 # Window size
GAME_GRID = 10 # Number of square for the grid
GAME_RESOLUTION = WINDOW_SIZE // GAME_GRID

# AI rewards (fitness)
REWARD_ALIVE_ONE_MORE_FRAME = 1
REWARD_EAT_FOOD = 100

# AI penelties (fitness)
PENALTY_HARD_STUCK = 20
PENALTY_HUNGER_DEATH = 10
PENALTY_WALL_TAIL_DEATH = 10

# debug mode (prints informations)
DEBUG = False
NO_FOOD = False
NO_GROW = False

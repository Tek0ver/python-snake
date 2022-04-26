import pygame
from random import randint
from sys import exit

pygame.init()

# SETTINGS
FPS = 1
WINDOW_SIZE = 500 # Window size
GAME_GRID = 10 # Number of square for the grid

GAME_RESOLUTION = WINDOW_SIZE // GAME_GRID

screen = pygame.display.set_mode((WINDOW_SIZE,WINDOW_SIZE))
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 24)
text_color = (0,0,0)

def setup_game():
    global snake, food, score

    snake = Snake()
    food = Food()
    score = Score()

    print("game setup")

def gameover():

    text_1 = font.render(f"GAMEOVER", True, text_color)
    text_2 = font.render(f"score : {str(score.score)}", True, text_color)
    text_3 = font.render(f"replay : R", True, text_color)
    text_4 = font.render(f"quit : Q", True, text_color)

    snake.draw()
    food.draw()

    screen.blit(text_1, (0,60))
    screen.blit(text_2, (0,80))
    screen.blit(text_3, (0,140))
    screen.blit(text_4, (0,160))

    pygame.display.flip()

    pause = True

    while pause:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_r:
                    pause = False

                    # Reset game
                    setup_game()


class Score:
    def __init__(self):
        self.score = 0
        self.image = font.render(f"score : {str(self.score)}", True, text_color)

    def add(self, points):
        self.score += points
        self.image = font.render(f"score : {str(self.score)}", True, text_color)
    
    def draw(self):
        screen.blit(self.image, (0,0))


class SnakeBody:
    def __init__(self, center):

        self.image = pygame.Surface((GAME_RESOLUTION,GAME_RESOLUTION))
        self.image.fill((93,175,29))
        self.rect = self.image.get_rect(center=center)

    def draw(self):

        screen.blit(self.image, self.rect)


class Snake:
    def __init__(self):

        self.sprite_head = pygame.Surface((GAME_RESOLUTION,GAME_RESOLUTION))
        self.sprite_head.fill((55,87,30))

        self.rect_head = self.sprite_head.get_rect(bottomright=(GAME_GRID//4 * GAME_RESOLUTION,GAME_GRID//4 * GAME_RESOLUTION)) # Spawn at center
        self.body = []

        self.directions = [(0,-1), (1,0), (0,1), (-1,0)] # [ top, right, bottom, left]
        self.direction_index = 2
        self.direction = self.directions[self.direction_index] # Spawn heading to bottom

        self.max_limit = screen.get_width() # Store to check collision with walls

    def move(self):

        # store head position before moving to use position when moving body
        head_pos = self.rect_head.center

        self.check_collisons() # check colisions at the coming position before moving

        # move head
        self.rect_head.move_ip(self.direction[0] * GAME_RESOLUTION,
                               self.direction[1] * GAME_RESOLUTION)
        

        # move body
        if self.body:
            # delete "last"
            del self.body[0]
            # "move" first
            self.body.append(SnakeBody(head_pos))

    def check_collisons(self):

        next_head_position = self.rect_head.move(self.direction[0] * GAME_RESOLUTION,
                                                    self.direction[1] * GAME_RESOLUTION)

        # check for food
        if next_head_position.colliderect(food.rect):
            score.add(1)
            food.spawn()
            self.grow()

        # check for "out of screen"
        elif next_head_position.bottom > self.max_limit or next_head_position.top < 0 or next_head_position.left < 0 or next_head_position.right > self.max_limit:
            gameover()

        # check for tail
        elif next_head_position.collidelist(self.body) not in [-1, 0]:
            gameover()

    def draw(self):

        screen.blit(self.sprite_head, self.rect_head)
        for body in self.body:
            body.draw()

    def turn(self, direction):

        if type(direction) is int: # for human input
            # avoid death by going back (top to bottom, left to right, etc)
            if (direction == 0 and self.direction_index != 2)\
            or (direction == 2 and self.direction_index != 0)\
            or (direction == 3 and self.direction_index != 1)\
            or (direction == 1 and self.direction_index != 3):
                self.direction_index = direction
                self.direction = self.directions[self.direction_index]

        elif type(direction) is str: # for ai input
            if direction == 'left':
                if self.direction_index == 0:
                    self.direction_index = 3
                else:
                    self.direction_index -= 1
            if direction == 'right':
                if self.direction_index == 3:
                    self.direction_index = 0
                else:
                    self.direction_index += 1
                    
            # then make the turn
            self.direction = self.directions[self.direction_index]

        # self.directions = [(0,-1), (1,0), (0,1), (-1,0)] # [ top, right, bottom, left]
        # self.direction_index = 2
        # self.direction = self.directions[self.direction_index] # Spawn heading to bottom        

    def grow(self):

        if len(self.body) == 0:
            self.body.append(SnakeBody(self.rect_head.center))
        else:
            self.body.insert(0, SnakeBody(self.body[-1].rect.center))


class Food:
    def __init__(self):

        self.image = pygame.Surface((GAME_RESOLUTION,GAME_RESOLUTION))
        self.image.fill((194,46,46))
        self.rect = self.image.get_rect()

        self.spawn()

    def spawn(self):

        self.rect.topleft = (randint(0,GAME_GRID - 1) * GAME_RESOLUTION,
                             randint(0,GAME_GRID - 1) * GAME_RESOLUTION)
    
    def draw(self):

        screen.blit(self.image, self.rect)


running = True
input_ready = True

setup_game()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif input_ready:
                if event.key == pygame.K_UP:
                    snake.turn(0)
                    input_ready = False
                elif event.key == pygame.K_DOWN:
                    snake.turn(2)
                    input_ready = False
                elif event.key == pygame.K_LEFT:
                    snake.turn(3)
                    input_ready = False
                elif event.key == pygame.K_RIGHT:
                    snake.turn(1)
                    input_ready = False
                elif event.key == pygame.K_j:
                    snake.turn('left')
                    input_ready = False
                elif event.key == pygame.K_k:
                    snake.turn('right')
                    input_ready = False

    screen.fill((200,200,200))

    snake.move()
    snake.draw()

    food.draw()

    score.draw()

    pygame.display.flip()

    clock.tick(FPS)
    input_ready = True

pygame.quit()

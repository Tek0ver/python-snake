import pygame, os, neat, pickle
from random import randint
from sys import exit

pygame.init()

# SETTINGS
FPS = 100
WINDOW_SIZE = 500 # Window size
GAME_GRID = 10 # Number of square for the grid

GAME_RESOLUTION = WINDOW_SIZE // GAME_GRID

screen = pygame.display.set_mode((WINDOW_SIZE,WINDOW_SIZE))
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 24)
text_color = (0,0,0)

print(globals())


def setup_game(ai):
    global snake, food, score

    snake = Snake(ai)
    food = Food()
    score = Score()


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
                    setup_game(ai=False)


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
    def __init__(self, ai):

        self.sprite_head = pygame.Surface((GAME_RESOLUTION,GAME_RESOLUTION))
        self.sprite_head.fill((55,87,30))

        self.alive = True
        if ai is False:
            self.mode = 'human'
        else:
            self.mode = 'ai'

        self.rect_head = self.sprite_head.get_rect(bottomright=(GAME_GRID//2 * GAME_RESOLUTION,GAME_GRID//2 * GAME_RESOLUTION)) # Spawn at center
        self.body = []

        self.directions = [(0,-1), (1,0), (0,1), (-1,0)] # [ top, right, bottom, left]
        self.direction_index = 2
        self.direction = self.directions[self.direction_index] # Spawn heading to bottom

        self.max_limit = screen.get_width() # Store to check collision with walls

    def move(self):

        # store head position before moving to use position when moving body
        head_pos = self.rect_head.center

        self.check_collisons() # check colisions at the coming position before moving

        if self.alive is False and self.mode == 'ai':
            return False
        elif self.alive is False and self.mode == 'human':
            gameover()

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
            self.alive = False

        # check for tail
        elif next_head_position.collidelist(self.body) not in [-1, 0]:
            self.alive = False

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

    def grow(self):

        if len(self.body) == 0:
            self.body.append(SnakeBody(self.rect_head.center))
        else:
            self.body.insert(0, SnakeBody(self.body[-1].rect.center))
    
    def sensor(self, rect):

        # 0 : nothing
        # 1 : wall or tail
        # 2 : food

        # walls
        if rect.bottom > self.max_limit or rect.top < 0 or rect.left < 0 or rect.right > self.max_limit:
            return 1
        # tail
        elif rect.collidelist(self.body) != -1:
            return 1
        # food
        elif rect.colliderect(food.rect):
            return 2
        # nothing
        else:
            return 0

    def make_inputs(self, type): # type is a list

        response = []

        if 1 in type: # only see 1 unit ahead
            rect = self.rect_head.move(self.direction[0] * GAME_RESOLUTION,
                                         self.direction[1] * GAME_RESOLUTION)
            response.append(self.sensor(rect))

        if 2 in type: # see food
            if food.rect.x - snake.rect_head.x > 0:
                x = 1
            elif food.rect.x - snake.rect_head.x < 0:
                x = -1
            else:
                x = 0
            response.append(x)

            if food.rect.y - snake.rect_head.y > 0:
                y = 1
            elif food.rect.y - snake.rect_head.y < 0:
                y = -1
            else:
                y = 0
            response.append(y)

        if 3 in type: # see 1 unit on left and right
            # left
            direction_index = self.direction_index

            if self.direction_index == 0:
                direction_index = 3
            else:
                direction_index -= 1

            direction = self.directions[direction_index]

            rect = self.rect_head.move(direction[0] * GAME_RESOLUTION,
                                       direction[1] * GAME_RESOLUTION)
            response.append(self.sensor(rect))

            # right
            direction_index = self.direction_index

            if self.direction_index == 3:
                direction_index = 0
            else:
                direction_index += 1

            direction = self.directions[direction_index]

            rect = self.rect_head.move(direction[0] * GAME_RESOLUTION,
                                       direction[1] * GAME_RESOLUTION)
            response.append(self.sensor(rect))
        
        return response


class Food:
    def __init__(self):

        self.image = pygame.Surface((GAME_RESOLUTION,GAME_RESOLUTION))
        self.image.fill((194,46,46))
        self.rect = self.image.get_rect()

        self.spawn()

    def spawn(self):

        self.rect.topleft = (randint(0,GAME_GRID - 1) * GAME_RESOLUTION,
                             randint(0,GAME_GRID - 1) * GAME_RESOLUTION)
        
        if self.rect.collidelist(snake.body) != -1 or self.rect.colliderect(snake.rect_head) is True:
            self.spawn()
    
    def draw(self):

        screen.blit(self.image, self.rect)


# with AI
def eval_genomes(genomes, config):

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        running = True

        setup_game(ai=True) # makes snake, food and score

        last_move = 0 # 0 : straight, 1 : left, 2 : right
        last_count = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        genome.fitness = 0
                        running = False

            # run game
            screen.fill((200,200,200))
            if snake.move() is False:
                genome.fitness -= 10
                running = False
            snake.draw()
            food.draw()
            score.draw()
            pygame.display.flip()
            clock.tick(FPS)

            # send inputs from game to network
            output = net.activate(snake.make_inputs([1, 2, 3]))
            decision = output.index(max(output))

            # avoid stuck in circle
            if last_move != decision:
                last_move = decision
                last_count = 0
            else:
                last_count += 1
                if last_move in [1, 2] and last_count >= 10:
                    genome.fitness -= 100
                    running = False

            # send outputs from network to game
            if decision == 0: # doing nothing, going straight
                pass
            elif decision == 1:
                snake.turn('left')
            elif decision == 2:
                snake.turn('right')

            genome.fitness += 1

        # fitness
        genome.fitness += score.score * 100
        print(genome.fitness)
            

# without AI
def main():    

    running = True
    input_ready = True

    setup_game(ai=False)

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
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
    exit()


# see neat-python documentations about the run function
# (https://neat-python.readthedocs.io/en/latest/xor_example.html#example-source)
def run(config_path):

    # load configuration
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    # create the population, which is the top-level object for a NEAT run
    p = neat.Population(config)

    # to load from checkpoint
    # p = neat.Checkpointer.restore_checkpoint('checkpoint-name')

    # add a stdout reporter to show progress in the terminal
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # run for up to 100 generations
    winner = p.run(eval_genomes, 100)
    # save the best AI
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-neat-00.txt")
    # run(config_path)
    # main()

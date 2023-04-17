from settings import *
import pygame, neat
from snake import Snake
from food import Food


class Game:
    
    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_SIZE,WINDOW_SIZE))
        self.clock = pygame.time.Clock()

        font = pygame.font.SysFont(None, 24)
        text_color = (0,0,0)

        self.fps = FPS

    def draw_game(self, snake, food):
        self.screen.fill((200,200,200))
        snake.draw(self.screen)
        food.draw(self.screen)
        pygame.display.flip()

    def run(self, genomes, config):
        global DEBUG

        for genome_id, genome in genomes:

            if DEBUG:
                print('new snake')

            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)

            snake = Snake()
            food = Food(snake)

            # draw first frame
            self.draw_game(snake, food)
            self.clock.tick(self.fps)

            last_decision = -1

            hunger = GAME_GRID ** 3

            running = True
            input_ready = True

            while running:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()
                        if event.key == pygame.K_s: # slow time
                            if self.fps == FPS:
                                self.fps = 2
                            else:
                                self.fps = FPS
                        if event.key == pygame.K_d: # debug
                            if DEBUG is True:
                                DEBUG = False
                            else:
                                DEBUG = True
                        
                        # for human inputs
                        elif input_ready:
                            if event.key == pygame.K_UP:
                                snake.turn('up')
                                input_ready = False
                            elif event.key == pygame.K_DOWN:
                                snake.turn('down')
                                input_ready = False
                            elif event.key == pygame.K_LEFT:
                                snake.turn('left')
                                input_ready = False
                            elif event.key == pygame.K_RIGHT:
                                snake.turn('right')
                                input_ready = False

                # AI works here
                # send inputs from game to network
                output = net.activate(snake.make_inputs(food))
                decision = output.index(max(output))
                # send outputs from network to game
                if decision == 0:
                    snake.turn('up')
                elif decision == 1:
                    snake.turn('down')
                elif decision == 2:
                    snake.turn('left')
                elif decision == 3:
                    snake.turn('right')

                if DEBUG:
                    print(snake.make_inputs(food))
                    pause = input()

                # avoid stuck in left/right/left/right/... or up/down/up/down/...
                backwards_directions = {
                    0: 1, 1: 0, 2: 3, 3: 2
                }
                if last_decision == backwards_directions[decision]:
                    genome.fitness -= PENALTY_HARD_STUCK
                    break
                    
                last_decision = decision

                # avoir stuck in loop
                hunger -= 1
                if hunger <= 0:
                    genome.fitness -= PENALTY_HUNGER_DEATH
                    break

                if snake.update(food) == 'eat food':
                    # AI reward if alive
                    genome.fitness += REWARD_EAT_FOOD
                    hunger = GAME_GRID ** 2
                
                self.draw_game(snake, food)

                self.clock.tick(self.fps)
                input_ready = True

                # break if snake is dead
                if snake.alive is False:
                    # AI penalty if dead
                    genome.fitness -= PENALTY_WALL_TAIL_DEATH
                    break

                # AI reward if alive
                genome.fitness += REWARD_ALIVE_ONE_MORE_FRAME

                if DEBUG:
                    print(genome.fitness)
        
            if DEBUG:
                print(f"end, fitness : {genome.fitness}")

from settings import *
import pygame


class Snake:

    def __init__(self):

        # head
        self.image = pygame.Surface((GAME_RESOLUTION,GAME_RESOLUTION))
        self.image.fill((55,87,30))
        self.rect = self.image.get_rect(bottomright=(GAME_GRID//2 * GAME_RESOLUTION,GAME_GRID//2 * GAME_RESOLUTION))

        # tail
        self.tail = []

        self.alive = True

        self.rect = self.image.get_rect(bottomright=(
            (GAME_GRID//2 + 1) * GAME_RESOLUTION,
            (GAME_GRID//2 + 1) * GAME_RESOLUTION)) # Spawn at center
        self.direction = (0,1) # spawn heading to bottom

    def update(self, food):

        eat = False

        # store head position before moving to use position when moving body
        head_pos = self.rect.center

        # check colisions at the coming position before moving
        if self.check_collisions(food) == 'food':
            eat = True

        # if snake is dead, stop here
        if self.alive is False:
            return False

        # move head
        self.rect.move_ip(self.direction[0] * GAME_RESOLUTION,
                          self.direction[1] * GAME_RESOLUTION)

        # move tail
        if self.tail:
            # delete "last"
            del self.tail[0]
            # "move" first
            self.tail.append(Tail(head_pos))
        
        if eat is True:
            return 'eat food'

    def draw(self, screen):

        screen.blit(self.image, self.rect)
        for tail in self.tail:
            tail.draw(screen)

    def check_collisions(self, food):

        next_head_position = self.rect.move(self.direction[0] * GAME_RESOLUTION,
                                            self.direction[1] * GAME_RESOLUTION)

        next_position = self.sensor(food, next_head_position)

        # check for food
        if next_position == 2:
            food.spawn(self)
            self.grow()
            return 'food'

        # check for "out of screen"
        elif next_position == 1:
            self.alive = False

    def turn(self, direction):
        
        if DEBUG:
            print(direction)

        if direction == 'up':
            self.direction = (0,-1)
        elif direction == 'down':
            self.direction = (0,1)
        elif direction == 'left':
            self.direction = (-1,0)
        elif direction == 'right':
            self.direction = (1,0)

    def grow(self):

        if NO_GROW:
            return None

        # tail grows of 1 unit
        if self.tail:
            self.tail.insert(0, Tail(self.tail[-1].rect.center))
        else:
            self.tail.append(Tail(self.rect.center))

    def sensor(self, food, rect):
        
        # 0 : nothing
        # 1 : wall or tail
        # 2 : food

        # walls
        if rect.centerx < 0\
        or rect.centerx > WINDOW_SIZE\
        or rect.centery < 0\
        or rect.centery > WINDOW_SIZE:
            return 1
        # tail
        elif rect.collidelist(self.tail) != -1:
            return 1
        # food
        elif rect.colliderect(food.rect):
            return 2
        # nothing
        else:
            return 0
    
    def make_inputs(self, food): # make inputs for AI
        
        inputs = [] # inputs for AI

        for direction in [(0,-1), (1,0), (0,1), (-1,0)]:
            rect = self.rect.move(direction[0] * GAME_RESOLUTION,
                                  direction[1] * GAME_RESOLUTION)
            inputs.append(self.sensor(food, rect))

        if NO_FOOD is False:
            food_direction_y = food.rect.y - self.rect.y
            food_direction_x = food.rect.x - self.rect.x
            # food above snake head
            if food_direction_y < 0:
                inputs.append(1)
            else:
                inputs.append(0)
            # food under snake head
            if food_direction_y > 0:
                inputs.append(1)
            else:
                inputs.append(0)
            # food on left of snake head
            if food_direction_x < 0:
                inputs.append(1)
            else:
                inputs.append(0)
            # food on right of snake head
            if food_direction_x > 0:
                inputs.append(1)
            else:
                inputs.append(0)

        return inputs


class Tail:

    def __init__(self, center):

        self.image = pygame.Surface((GAME_RESOLUTION,GAME_RESOLUTION))
        self.image.fill((93,175,29))
        self.rect = self.image.get_rect(center=center)

    def draw(self, screen):

        screen.blit(self.image, self.rect)

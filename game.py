import pygame
from random import randint
from sys import exit

pygame.init()

screen = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()
FPS = 15


def gameover():
    print(f"Gameover, score : {score.score}")
    pygame.quit()
    exit()


class Score:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont(None, 24)
        self.color = (0,0,0)
        self.image = self.font.render(f"score : {str(self.score)}", True, self.color)

    def add(self, points):
        self.score += points
        self.image = self.font.render(f"score : {str(self.score)}", True, self.color)
    
    def draw(self):
        screen.blit(self.image, (0,0))


class SnakeBody:
    def __init__(self, center):

        self.image = pygame.Surface((10,10))
        self.image.fill((93,175,29))
        self.rect = self.image.get_rect(center=center)

    def draw(self):

        screen.blit(self.image, self.rect)


class Snake:
    def __init__(self):

        self.sprite_head = pygame.Surface((10,10))
        self.sprite_head.fill((55,87,30))

        self.rect_head = self.sprite_head.get_rect(topleft=(250,250))
        self.body = []
        self.direction = (0,1)

    def move(self):

        # store head position before moving to use position when moving body
        head_pos = self.rect_head.center

        # move head
        self.rect_head.move_ip(self.direction[0] * 10,
                               self.direction[1] * 10)
        
        self.check_collisons()

        # move body
        if self.body:
            # delete "last"
            del self.body[0]
            # "move" first
            self.body.append(SnakeBody(head_pos))

    def check_collisons(self):

        # check for food
        if self.rect_head.colliderect(food.rect):
            score.add(1)
            food.spawn()
            self.grow()

        # check for "out of screen"
        elif self.rect_head.bottom > 500 or self.rect_head.top < 0 or self.rect_head.left < 0 or self.rect_head.right > 500:
            gameover()

        # check for tail
        elif self.rect_head.collidelist(self.body) != -1:
            gameover()

    def draw(self):

        screen.blit(self.sprite_head, self.rect_head)
        for body in self.body:
            body.draw()

    def turn(self, direction):

        self.direction = direction

    def grow(self):

        if len(self.body) == 0:
            self.body.append(SnakeBody(self.rect_head.center))
        else:
            self.body.insert(0, SnakeBody(self.body[-1].rect.center))


class Food:
    def __init__(self):

        self.image = pygame.Surface((10,10))
        self.image.fill((194,46,46))
        self.rect = self.image.get_rect()

        self.spawn()

    def spawn(self):

        self.rect.topleft = (randint(0,49) * 10,
                             randint(0,49) * 10)
    
    def draw(self):

        screen.blit(self.image, self.rect)


running = True

snake = Snake()
food = Food()
score = Score()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                snake.turn((0,-1))
            elif event.key == pygame.K_DOWN:
                snake.turn((0,1))
            elif event.key == pygame.K_LEFT:
                snake.turn((-1,0))
            elif event.key == pygame.K_RIGHT:
                snake.turn((1,0))

    screen.fill((200,200,200))

    snake.move()
    snake.draw()

    food.draw()

    score.draw()

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()

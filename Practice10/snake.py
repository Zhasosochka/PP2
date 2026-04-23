import pygame
import random
from pygame.locals import *

pygame.init()

#colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

window_size = (700, 700)
s = pygame.display.set_mode(window_size)
pygame.display.set_caption("Snake Game")
c = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 34)
snake = [(100, 100), (80, 100), (60, 100)]
block = 20
direct = "RIGHT"
score = 0
level = 1
speed = 10

# Generation of apples
def food_generator():
    while True:
        x = random.randrange(0, window_size[0], block)
        y = random.randrange(0, window_size[1], block)
        new_food = (x, y)
        if new_food not in snake:
            return new_food
food = food_generator()


while True:
    # event processing
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        #movement
        if event.type == KEYDOWN:
            if event.key == K_LEFT and direct != "RIGHT":
                direct = "LEFT"
            elif event.key == K_RIGHT and direct != "LEFT":
                direct = "RIGHT"
            elif event.key == K_UP and direct != "DOWN":
                direct = "UP"
            elif event.key == K_DOWN and direct != "UP":
                direct = "DOWN"

    head_x, head_y = snake[0]
    if direct == "RIGHT":
        new_head = (head_x + block, head_y)
    elif direct == "LEFT":
        new_head = (head_x - block, head_y)
    elif direct == "UP":
        new_head = (head_x, head_y - block)
    elif direct == "DOWN":
        new_head = (head_x, head_y + block)

    # checking collision with border and snakes
    if new_head[0] < 0 or new_head[0] >= window_size[0] or new_head[1] < 0 or new_head[1] >= window_size[1]:
        break
    if new_head in snake:
        break

    # adding new head
    snake.insert(0, new_head)
    # deleting tail
    if new_head != food:
        snake.pop()
    else:
        score += 1
        food = food_generator()
        level = score // 5 + 1
        speed = 10 + (level - 1) * 2

    s.fill(GREEN) #background

    #food drawing
    pygame.draw.rect(s, (255, 0, 0), (food[0], food[1], block, block))

    #snake drawing
    for segment in snake:
        pygame.draw.rect(s, BLUE, (segment[0], segment[1], block, block))

    # score, level and speed displaying
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    speed_text = font.render(f"Speed: {speed}", True, WHITE)
    s.blit(score_text, (10, 10))
    s.blit(level_text, (10, 40))
    s.blit(speed_text, (10, 70))


    pygame.display.update()
    c.tick(speed)
pygame.quit()
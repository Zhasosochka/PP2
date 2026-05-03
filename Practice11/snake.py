import pygame
import random
import time
from pygame.locals import *

# Initialize Pygame engine
pygame.init()

# Color Definitions (RGB)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BLUE  = (0, 0, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (40, 40, 40)

# Food Configurations: point value, color, and expiration time in seconds
FOOD_TYPES = [
    {"value": 1, "color": (255, 50, 50),  "lifetime": 8},  # Red: common
    {"value": 2, "color": (255, 165, 0),  "lifetime": 5},  # Orange: rare
    {"value": 3, "color": (255, 255, 0),  "lifetime": 3},  # Yellow: legendary
]

# Game Window and Clock Settings
window_size = (700, 700)
s = pygame.display.set_mode(window_size)
pygame.display.set_caption("Snake Game - Weighted Food & Timers")
c = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 24)

# Snake Initial State: list of coordinates (head is index 0)
snake = [(100, 100), (80, 100), (60, 100)]
block = 20 # Size of one segment/grid cell
direct = "RIGHT"
score = 0
level = 1
speed = 10

def food_generator():
    """Generates a random food item aligned to the grid."""
    while True:
        # Calculate random position within window boundaries
        x = random.randrange(0, window_size[0], block)
        y = random.randrange(0, window_size[1], block)
        pos = (x, y)

        # Ensure food doesn't spawn on top of the snake
        if pos not in snake:
            # Pick a random food category and store its spawn timestamp
            f_type = random.choice(FOOD_TYPES).copy()
            f_type["pos"] = pos
            f_type["spawn_time"] = pygame.time.get_ticks() # Time since init in ms
            return f_type

# Create the first food item
food = food_generator()

# Main Game Loop
running = True
while running:
    # 1. Input Event Processing
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # Handle Directional Input (Prevents 180-degree self-collision)
        if event.type == KEYDOWN:
            if event.key == K_LEFT and direct != "RIGHT":
                direct = "LEFT"
            elif event.key == K_RIGHT and direct != "LEFT":
                direct = "RIGHT"
            elif event.key == K_UP and direct != "DOWN":
                direct = "UP"
            elif event.key == K_DOWN and direct != "UP":
                direct = "DOWN"

    # 2. Movement Logic: Predict the next head position
    head_x, head_y = snake[0]
    if direct == "RIGHT":
        new_head = (head_x + block, head_y)
    elif direct == "LEFT":
        new_head = (head_x - block, head_y)
    elif direct == "UP":
        new_head = (head_x, head_y - block)
    elif direct == "DOWN":
        new_head = (head_x, head_y + block)

    # 3. Collision Detection (Walls and Self-bite)
    if (new_head[0] < 0 or new_head[0] >= window_size[0] or
        new_head[1] < 0 or new_head[1] >= window_size[1] or
        new_head in snake):
        print(f"Game Over! Final Score: {score}")
        break

    # Advance the snake by adding the new head
    snake.insert(0, new_head)

    # 4. Food Lifetime Logic: Check if food has expired
    current_time = pygame.time.get_ticks()
    # If elapsed time exceeds lifetime (converted to ms), respawn food
    if current_time - food["spawn_time"] > food["lifetime"] * 1000:
        food = food_generator()

    # 5. Eating Logic
    if new_head == food["pos"]:
        score += food["value"] # Apply point weight
        food = food_generator()

        # Progression: Increase level/speed every 5 points
        level = score // 5 + 1
        speed = 10 + (level - 1) * 2
    else:
        # Remove the tail if no food eaten (maintains length)
        snake.pop()

    # 6. Rendering / Drawing
    s.fill(DARK_GRAY)

    # Draw the active food item
    pygame.draw.rect(s, food["color"], (food["pos"][0], food["pos"][1], block, block))

    # Draw all snake segments with a visual border
    for segment in snake:
        pygame.draw.rect(s, BLUE, (segment[0], segment[1], block, block))
        pygame.draw.rect(s, WHITE, (segment[0], segment[1], block, block), 1)

    # 7. UI Overlay Rendering
    # Calculate countdown timer in seconds
    time_left = max(0, food["lifetime"] - (current_time - food["spawn_time"]) // 1000)

    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    timer_text = font.render(f"Food Timer: {time_left}s", True, food["color"])

    # Draw text to screen at specified coordinates
    s.blit(score_text, (10, 10))
    s.blit(level_text, (10, 40))
    s.blit(timer_text, (10, 70))

    # Update the physical display
    pygame.display.update()

    # Maintain consistent game speed
    c.tick(speed)

# Clean exit
pygame.quit()
import pygame
import random
import json
import os
from config import *

class GameEngine:
    def __init__(self, username, db):
        """ Initialize the game engine with database connection and player info """
        self.db = db
        self.username = username

        # Database operations to fetch or create player and get their record
        self.player_id = db.get_or_create_player(username)
        self.personal_best = db.get_personal_best(self.player_id)

        # Flags to trigger sound effects or animations in the main loop
        self.just_ate_food = False
        self.just_ate_powerup = False

        # Load user preferences and start the game state
        self.load_settings()
        self.reset_game()

    # --- Setup and Settings ---

    def load_settings(self):
        """ Load player settings from a JSON file or use defaults """
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                self.settings = json.load(f)
        else:
            # Fallback to default constants from config.py
            self.settings = {"snake_color": BLUE, "grid": True, "sound": True}

    def reset_game(self):
        """ Set all game variables to their starting values """
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "RIGHT"
        self.score = 0
        self.level = 1
        self.base_speed = 10
        self.current_speed = 10
        self.obstacles = []
        self.shield_active = False
        self.powerup = None
        self.food = self.spawn_item("food")
        self.game_over = False

    # --- Item Generation ---

    def spawn_item(self, item_type):
        """ Find a random empty position and spawn food or power-up """
        while True:
            x = random.randrange(0, WINDOW_SIZE[0], BLOCK_SIZE)
            y = random.randrange(0, WINDOW_SIZE[1], BLOCK_SIZE)
            pos = (x, y)

            # Prevent spawning items inside the snake or obstacles
            if pos not in self.snake and pos not in self.obstacles:
                if item_type == "food":
                    f = random.choice(FOOD_TYPES).copy()
                    f["pos"] = pos
                    f["spawn_time"] = pygame.time.get_ticks()
                    return f
                else: # Powerup type
                    p = random.choice(POWER_UPS).copy()
                    p["pos"] = pos
                    p["spawn_time"] = pygame.time.get_ticks()
                    return p

    def generate_obstacles(self):
        """ Randomly place wall blocks starting from level 3 """
        self.obstacles = []
        if self.level >= 3:
            for _ in range(self.level * 2):
                x = random.randrange(0, WINDOW_SIZE[0], BLOCK_SIZE)
                y = random.randrange(0, WINDOW_SIZE[1], BLOCK_SIZE)
                # Ensure walls don't spawn on top of the snake
                if (x, y) not in self.snake:
                    self.obstacles.append((x, y))

    # --- Core Logic ---

    def update(self):
        """ Main logic loop: movement, collisions, and item interactions """
        curr_ticks = pygame.time.get_ticks() # Get current time once for all checks

        # 1. Calculate new head position based on current direction
        head_x, head_y = self.snake[0]
        if self.direction == "RIGHT": head_x += BLOCK_SIZE
        elif self.direction == "LEFT": head_x -= BLOCK_SIZE
        elif self.direction == "UP": head_y -= BLOCK_SIZE
        elif self.direction == "DOWN": head_y += BLOCK_SIZE
        new_head = (head_x, head_y)

        # 2. Collision Logic (Walls, Self, or Obstacles)
        if (new_head[0] < 0 or new_head[0] >= WINDOW_SIZE[0] or
            new_head[1] < 0 or new_head[1] >= WINDOW_SIZE[1] or
            new_head in self.snake or new_head in self.obstacles):

            if self.shield_active:
                self.shield_active = False # Shield protects the player once
            else:
                self.game_over = True
                # Save results to the database upon death
                self.db.save_session(self.player_id, self.score, self.level)
                return

        # 2.5 Food Expiration Logic
        # Check if the current food item has exceeded its lifetime
        if curr_ticks - self.food["spawn_time"] > self.food["lifetime"] * 1000:
            self.food = self.spawn_item("food") # Spawn a new one if expired

        # Move the snake by inserting a new head
        self.snake.insert(0, new_head)

        # 3. Eating Logic
        if new_head == self.food["pos"]:
            self.just_ate_food = True

            if self.food["type"] == "poison":
                # Poison reduces snake size
                for _ in range(2):
                    if len(self.snake) > 1: self.snake.pop()
                # Game over if the snake becomes too small
                if len(self.snake) <= 1: self.game_over = True
            else:
                # Normal food increases score
                self.score += self.food["value"]

            self.food = self.spawn_item("food")

            # Handle leveling up every 5 points
            new_level = self.score // 5 + 1
            if new_level > self.level:
                self.level = new_level
                self.base_speed = 10 + (self.level - 1) * 2
                self.generate_obstacles()
        else:
            # Remove tail segment if no food was eaten to maintain length
            self.snake.pop()

        # 4. Power-up Logic: Spawning and Expiry
        if not self.powerup and random.random() < 0.01: # 1% chance per frame to spawn
            self.powerup = self.spawn_item("powerup")

        # Remove power-up if not collected within 8 seconds
        if self.powerup and curr_ticks - self.powerup["spawn_time"] > 8000:
            self.powerup = None

        # Check for power-up collection
        if self.powerup and new_head == self.powerup["pos"]:
            self.just_ate_powerup = True
            self.apply_powerup(self.powerup)
            self.powerup = None

    def apply_powerup(self, p):
        """ Apply the specific effect of the collected power-up """
        if p["effect"] == "speed_up":
            self.current_speed = self.base_speed + 10
        elif p["effect"] == "speed_down":
            self.current_speed = max(5, self.base_speed - 5)
        elif p["effect"] == "shield":
            self.shield_active = True

        # Store when the temporary effect should expire
        self.powerup_expiry = pygame.time.get_ticks() + p["duration"]
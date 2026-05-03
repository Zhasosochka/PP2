import pygame
import random

# screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self, color_path="images/Player.png"):
        super().__init__()
        # load and resize player image
        self.image = pygame.image.load(color_path)
        self.image = pygame.transform.scale(self.image, (50, 100))
        # set starting position
        self.rect = self.image.get_rect()
        self.rect.center = (200, 500)

        # player stats and statuses
        self.lives = 3
        self.max_lives = 3
        self.shield_active = False
        self.nitro_timer = 0

    def move(self):
        # check pressed keys
        keys = pygame.key.get_pressed()
        # use higher speed if nitro is active
        speed = 10 if self.nitro_timer > 0 else 5

        # move left/right within screen bounds
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-speed, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(speed, 0)

        # decrease nitro duration over time
        if self.nitro_timer > 0:
            self.nitro_timer -= 1

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # define different coin types and their points
        self.coin_types = [
            (pygame.image.load("images/bronze_coin.png"), 1),
            (pygame.image.load("images/silver_coin.png"), 3),
            (pygame.image.load("images/gold_coin.png"), 5)
        ]
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        # pick a random coin type
        chosen_coin = random.choice(self.coin_types)
        self.image = pygame.transform.scale(chosen_coin[0], (40, 40))
        self.weight = chosen_coin[1]
        # move to random position above screen
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, 360), -50)

    def move(self, speed):
        # move downward
        self.rect.move_ip(0, speed)
        # reset if it falls off screen
        if self.rect.top > 600:
            self.reset()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        # setup enemy car image
        self.image = pygame.image.load("images/Enemy.png")
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.reset()

    def reset(self, player_rect=None):
        # spawn at random x-position above screen
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -100)
        # make sure it doesn't spawn right on top of player
        if player_rect and self.rect.colliderect(player_rect.inflate(0, 200)):
            self.reset(player_rect)

    def move(self, speed_mod):
        # move downward
        self.rect.move_ip(0, speed_mod)
        # return true if it passed the player for scoring
        if self.rect.top > SCREEN_HEIGHT:
            return True
        return False

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type # Nitro, Shield, or Repair

        # load specific image based on powerup type
        if self.type == "Nitro":
            self.image = pygame.image.load("images/nitro.png")
        elif self.type == "Shield":
            self.image = pygame.image.load("images/shield.png")
        elif self.type == "Repair":
            self.image = pygame.image.load("images/heart.png")

        # set size and random start position
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -100)
        # record spawn time to track expiration
        self.spawn_time = pygame.time.get_ticks()

    def move(self, speed):
        # move downward
        self.rect.move_ip(0, speed)
        # delete if not picked up within 5 seconds
        if pygame.time.get_ticks() - self.spawn_time > 5000:
            self.kill()
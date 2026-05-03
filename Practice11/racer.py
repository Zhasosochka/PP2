#Imports
import pygame, sys
from pygame.locals import *
import random, time

#Initialzing Pygame engine
pygame.init()

#Setting up FPS (Frames Per Second) controller
FPS = 60
FramePerSec = pygame.time.Clock()

#Color definitions (R, G, B)
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Game constants and global variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 4        # Movement speed of enemies and coins
SCORE = 0        # Enemies passed
COIN_SCORE = 0   # Total value of coins collected
N = 10           # Threshold for speed increase

#Setting up Fonts for UI
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

#Loading assets: Background image and scaling it to fit screen
background = pygame.image.load("images/AnimatedStreet.png")
background = pygame.transform.scale(background, (400,600))

#Loading and configuring sound effects
coin_sound = pygame.mixer.Sound('sounds/coin.mp3')
coin_sound.set_volume(0.2)

#Creating the main display window
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # List of tuples containing (Surface image, score value)
        self.coin_types = [
            (pygame.image.load("images/bronze_coin.png"), 1),
            (pygame.image.load("images/silver_coin.png"), 3),
            (pygame.image.load("images/gold_coin.png"), 5)
        ]
        self.reset()

    def move(self):
        # Move coin downwards; reset if it goes off-screen
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            self.reset()

    def reset(self):
        # Randomly choose a coin type and weight
        chosen_coin = random.choice(self.coin_types)
        self.image = pygame.transform.scale(chosen_coin[0], (40, 40))
        self.weight = chosen_coin[1]
        self.rect = self.image.get_rect()
        # Random horizontal spawn point
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/Enemy.png")
        self.image = pygame.transform.scale(self.image, (50,120))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        # If enemy passes the player, increase score and respawn at top
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/Player.png")
        self.image = pygame.transform.scale(self.image, (50,120))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        # Handle keyboard input for horizontal movement
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

#Setting up Sprite instances
P1 = Player()
E1 = Enemy()
C1 = Coin()

#Grouping Sprites for collision detection and batch rendering
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

#Custom event to increase difficulty over time
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

#--- Main Game Loop ---
while True:

    #Event handling
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.2 # Gradual speed increase every second
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #Rendering background and score
    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))

    #Update position and draw all sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    #UI: Displaying collected coin value
    coin_text = font_small.render("Coins: " + str(COIN_SCORE), True, BLACK)
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 100, 10))

    #Collision Detection: Player vs Coins
    collided_coins = pygame.sprite.spritecollide(P1, coins, False)
    for coin in collided_coins:
        # Check if the coin score crosses the threshold 'N' to increase speed
        old_threshold = COIN_SCORE // N
        COIN_SCORE += coin.weight
        coin_sound.play()

        if COIN_SCORE // N > old_threshold:
            SPEED += 1
            print(f"Speed increased! Current speed: {SPEED}")

        coin.reset() # Put the coin back at the top

    #Collision Detection: Player vs Enemy (Game Over)
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('sounds/crash.mp3').play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30,250))

        pygame.display.update()
        for entity in all_sprites:
                entity.kill() # Remove all sprites before exiting
        time.sleep(2)
        pygame.quit()
        sys.exit()

    #Final screen update
    pygame.display.update()
    FramePerSec.tick(FPS)
import pygame, sys, time, random
from persistence import *
from ui import *
from racer import *

# basic setup
pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Pro 2026")
CLOCK = pygame.time.Clock()

# load user settings
DEFAULT_SETTINGS = {"sound": True, "color": "images/Player.png", "difficulty": 1}
settings = load_json("settings.json", DEFAULT_SETTINGS)

# images and sounds
HEART_IMG = pygame.image.load("images/heart.png")
HEART_IMG = pygame.transform.scale(HEART_IMG, (30, 30))
BACKGROUND = pygame.image.load("images/AnimatedStreet.png")
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

try:
    coin_sound = pygame.mixer.Sound('sounds/coin.mp3')
    crash_sound = pygame.mixer.Sound('sounds/crash.mp3')
    coin_sound.set_volume(0.5)
    crash_sound.set_volume(1.0)
except:
    print("missing audio files")
    coin_sound = crash_sound = None

# states and name
USER_NAME = "Player_1"
STATE_MENU = "MENU"
STATE_GAME = "GAME"
STATE_SETTINGS = "SETTINGS"
STATE_LEADERBOARD = "LEADERBOARD"
STATE_GAMEOVER = "GAMEOVER"

def game_loop():
    global settings

    # init sprites and groups
    player = Player(settings["color"])
    enemies = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    coins_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    all_sprites.add(player)

    C1 = Coin()
    coins_group.add(C1)
    all_sprites.add(C1)

    # score and speed variables
    score = 0
    distance = 0
    base_speed = 4 + settings.get("difficulty", 1)

    running = True
    while running:
        SCREEN.blit(BACKGROUND, (0, 0))
        distance += base_speed / 20

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        # spawn enemies based on distance
        if len(enemies) < (1 + int(distance // 1000)):
            new_enemy = Enemy(base_speed)
            new_enemy.reset(player.rect)
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # random powerup spawn
        if random.randint(1, 150) == 1:
            p_type = random.choice(["Nitro", "Shield", "Repair"])
            p = PowerUp(p_type)
            powerups.add(p)
            all_sprites.add(p)

        # move everything
        C1.move(base_speed)
        player.move()

        for e in enemies:
            if e.move(base_speed):
                score += 1
                e.reset(player.rect)

        for p in powerups:
            p.move(base_speed)

        # check coin collection
        collided_coins = pygame.sprite.spritecollide(player, coins_group, False)
        for coin in collided_coins:
            score += coin.weight
            if settings["sound"] and coin_sound:
                coin_sound.play()

            # increase difficulty
            if score % 10 == 0:
                base_speed += 0.5
            coin.reset()

        # check enemy collisions
        if pygame.sprite.spritecollideany(player, enemies):
            if player.shield_active:
                player.shield_active = False
                for e in pygame.sprite.spritecollide(player, enemies, True): pass
            else:
                if settings["sound"] and crash_sound:
                    crash_sound.play()

                player.lives -= 1
                for e in pygame.sprite.spritecollide(player, enemies, True): pass

                if player.lives <= 0:
                    add_score(USER_NAME, score, distance)
                    return STATE_GAMEOVER, score, int(distance)

        # check powerup collection
        collected_powerups = pygame.sprite.spritecollide(player, powerups, True)
        for p in collected_powerups:
            if p.type == "Nitro":
                player.nitro_timer = 180
            elif p.type == "Shield":
                player.shield_active = True
            elif p.type == "Repair":
                if player.lives < player.max_lives:
                    player.lives += 1

        # draw everything to screen
        all_sprites.draw(SCREEN)
        draw_text(SCREEN, f"Score: {score}", 20, 10, 10, (0,255,0))
        draw_text(SCREEN, f"Dist: {int(distance)}m", 20, 10, 40, (50,150,255))

        # render life icons
        for i in range(player.lives):
            SCREEN.blit(HEART_IMG, (10 + (i * 35), 70))

        # show powerup status
        if player.nitro_timer > 0:
            nitro_icon = pygame.transform.scale(pygame.image.load("images/nitro.png"), (25, 25))
            SCREEN.blit(nitro_icon, (SCREEN_WIDTH - 150, 45))
            seconds_left = round(player.nitro_timer / 60, 1)
            draw_text(SCREEN, f"BOOST: {seconds_left}s", 18, SCREEN_WIDTH - 120, 47, (255, 140, 0))

        if player.shield_active:
            shield_icon = pygame.transform.scale(pygame.image.load("images/shield.png"), (25, 25))
            SCREEN.blit(shield_icon, (SCREEN_WIDTH - 150, 75))
            draw_text(SCREEN, "SHIELD ACTIVE", 18, SCREEN_WIDTH - 120, 77, (0, 100, 255))

        pygame.display.update()
        CLOCK.tick(60)

def main():
    global current_state, settings
    current_state = STATE_MENU

    # init buttons
    btn_play = Button("PLAY", 100, 200, 200, 50, (50, 200, 50), (100, 255, 100))
    btn_leader = Button("LEADERBOARD", 100, 270, 200, 50, (50, 50, 200), (100, 100, 255))
    btn_sett = Button("SETTINGS", 100, 340, 200, 50, (200, 200, 50), (255, 255, 100))
    btn_quit = Button("QUIT", 100, 410, 200, 50, (200, 50, 50), (255, 100, 100))

    last_game_results = (0, 0)

    # main app loop
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        if current_state == STATE_MENU:
            SCREEN.fill((230, 230, 230))
            draw_text(SCREEN, "STREET RACER", 40, 50, 100, (0, 0, 0))
            btn_play.draw(SCREEN)
            btn_leader.draw(SCREEN)
            btn_sett.draw(SCREEN)
            btn_quit.draw(SCREEN)

            for event in events:
                if btn_play.is_clicked(event): current_state = STATE_GAME
                if btn_leader.is_clicked(event): current_state = STATE_LEADERBOARD
                if btn_sett.is_clicked(event): current_state = STATE_SETTINGS
                if btn_quit.is_clicked(event): pygame.quit(); sys.exit()

        elif current_state == STATE_GAME:
            current_state, s, d = game_loop()
            last_game_results = (s, d)

        elif current_state == STATE_GAMEOVER:
            SCREEN.fill((200, 0, 0))
            draw_text(SCREEN, "GAME OVER", 50, 60, 150, (255, 255, 255))
            btn_back = Button("TO MENU", 100, 400, 200, 50, (0,0,0), (50,50,50))
            btn_back.draw(SCREEN)
            for event in events:
                if btn_back.is_clicked(event): current_state = STATE_MENU

        elif current_state == STATE_SETTINGS:
            SCREEN.fill((240, 240, 240))
            draw_text(SCREEN, "SETTINGS", 35, 110, 50)
            btn_diff = Button(f"Difficulty: {settings['difficulty']}", 100, 200, 200, 50, (100, 100, 100), (150, 150, 150))
            btn_diff.draw(SCREEN)
            btn_back = Button("SAVE & BACK", 100, 500, 200, 50, (0, 150, 0), (0, 200, 0))
            btn_back.draw(SCREEN)

            for event in events:
                if btn_diff.is_clicked(event):
                    settings["difficulty"] = (settings["difficulty"] % 3) + 1
                if btn_back.is_clicked(event):
                    save_json("settings.json", settings)
                    current_state = STATE_MENU

        elif current_state == STATE_LEADERBOARD:
            SCREEN.fill((255, 255, 255))
            draw_text(SCREEN, "TOP 10", 35, 130, 30)
            data = load_json("leaderboard.json", [])
            for i, entry in enumerate(data):
                txt = f"{i+1}. {entry['name']} - {entry['score']} pts"
                draw_text(SCREEN, txt, 18, 50, 100 + (i * 35))
            btn_back = Button("BACK", 100, 520, 200, 40, (100, 100, 100), (150, 150, 150))
            btn_back.draw(SCREEN)
            for event in events:
                if btn_back.is_clicked(event): current_state = STATE_MENU

        pygame.display.update()
        CLOCK.tick(60)

if __name__ == "__main__":
    main()
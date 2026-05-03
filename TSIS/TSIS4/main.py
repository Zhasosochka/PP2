import pygame
import json
from pygame.locals import *
from config import *
from db import Database
from game import GameEngine

class SnakeApp:
    def __init__(self):
        """
        Initialize the application: setup Pygame, audio mixer,
        database connection, and load assets.
        """
        pygame.init()
        pygame.mixer.init()

        # Screen and Clock setup
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 24)

        # Data and State setup
        self.db = Database()
        self.state = "MENU"
        self.username = "Player1"
        self.engine = None

        # Audio Asset Loading
        self.eat_sfx = pygame.mixer.Sound("assets/eat.mp3")
        self.powerup_sfx = pygame.mixer.Sound("assets/powerup.mp3")
        self.death_sfx = pygame.mixer.Sound("assets/gameover.mp3")
        pygame.mixer.music.load("assets/bg_music.mp3")

    # --- AUDIO HELPER ---

    def play_bg_music(self):
        """
        Manage background music playback based on user settings.
        Plays infinitely (-1) if sounds are enabled.
        """
        if self.engine and self.engine.settings["sound"]:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

    # --- UI RENDERING HELPERS ---

    def draw_text(self, text, pos, color=WHITE):
        """ Render standard text to the screen at a given position """
        img = self.font.render(text, True, color)
        self.screen.blit(img, pos)

    def draw_legend(self):
        """
        Draw a 2-column legend guide in the top right corner:
        Column 1: Food items and weights.
        Column 2: Power-up types.
        """
        y_start = 15
        padding = 22
        icon_size = 14
        small_font = pygame.font.SysFont("Verdana", 14)

        col1_x = WINDOW_SIZE[0] - 360  # Left column (Food)
        col2_x = WINDOW_SIZE[0] - 180  # Right column (Boosts)

        # Draw Column 1: Food Types
        curr_y = y_start
        for item in FOOD_TYPES:
            label = "Poison" if item["type"] == "poison" else f"+{item['value']} Pts"
            pygame.draw.rect(self.screen, item["color"], (col1_x, curr_y, icon_size, icon_size))
            txt_img = small_font.render(label, True, WHITE)
            self.screen.blit(txt_img, (col1_x + 20, curr_y - 2))
            curr_y += padding

        # Draw Column 2: Power-ups
        curr_y = y_start
        for p_up in POWER_UPS:
            pygame.draw.ellipse(self.screen, p_up["color"], (col2_x, curr_y, icon_size, icon_size))
            txt_img = small_font.render(p_up["name"], True, WHITE)
            self.screen.blit(txt_img, (col2_x + 20, curr_y - 2))
            curr_y += padding

    # --- SCREENS AND SCENES ---

    def menu_screen(self):
        """ Main Menu: Navigate to Play, Leaderboard, or Settings """
        self.screen.fill(BLACK)
        self.draw_text("SNAKE PRO 2026", (250, 100), GREEN)
        self.draw_text(f"User: {self.username} (Press TAB to change)", (150, 200))
        self.draw_text("1. Play [Enter]", (250, 300))
        self.draw_text("2. Leaderboard [L]", (250, 350))
        self.draw_text("3. Settings [S]", (250, 400))
        self.draw_text("4. Quit [Q]", (250, 450))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT: return False
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.engine = GameEngine(self.username, self.db)
                    self.state = "PLAYING"
                if event.key == K_l:
                    self.current_scores = self.db.get_leaderboard()
                    self.state = "LEADERBOARD"
                if event.key == K_s: self.state = "SETTINGS"
                if event.key == K_q: return False
        return True

    def game_loop(self):
        """ Active Gameplay: Updates logic, plays sounds, and renders the map """
        self.engine.update()

        # Check Game Over
        if self.engine.game_over:
            pygame.mixer.music.stop()
            if self.engine.settings["sound"] and self.death_sfx:
                self.death_sfx.play()
            self.state = "GAMEOVER"
            return True

        self.play_bg_music()
        self.screen.fill(DARK_GRAY)

        # Trigger Eating Sound Effects
        if self.engine.just_ate_food and self.engine.settings["sound"]:
            if self.eat_sfx: self.eat_sfx.play()
            self.engine.just_ate_food = False

        if self.engine.just_ate_powerup and self.engine.settings["sound"]:
            if self.powerup_sfx: self.powerup_sfx.play()
            self.engine.just_ate_powerup = False

        # Render Grid Lines
        if self.engine.settings["grid"]:
            for x in range(0, WINDOW_SIZE[0], BLOCK_SIZE):
                pygame.draw.line(self.screen, (60, 60, 60), (x, 0), (x, WINDOW_SIZE[1]))
            for y in range(0, WINDOW_SIZE[1], BLOCK_SIZE):
                pygame.draw.line(self.screen, (60, 60, 60), (0, y), (WINDOW_SIZE[0], y))

        # Render Game Objects
        for obs in self.engine.obstacles:
            pygame.draw.rect(self.screen, WHITE, (obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE))

        f = self.engine.food
        pygame.draw.rect(self.screen, f["color"], (f["pos"][0], f["pos"][1], BLOCK_SIZE, BLOCK_SIZE))

        if self.engine.powerup:
            p = self.engine.powerup
            pygame.draw.ellipse(self.screen, p["color"], (p["pos"][0], p["pos"][1], BLOCK_SIZE, BLOCK_SIZE))

        for seg in self.engine.snake:
            color = self.engine.settings["snake_color"] if not self.engine.shield_active else GREEN
            pygame.draw.rect(self.screen, color, (seg[0], seg[1], BLOCK_SIZE, BLOCK_SIZE))

        # UI Overlay
        self.draw_text(f"Score: {self.engine.score}  Level: {self.engine.level}", (10, 10))
        self.draw_text(f"Best: {self.engine.personal_best}", (10, 40), ORANGE)
        self.draw_legend()

        pygame.display.flip()
        self.clock.tick(self.engine.current_speed)

        # Movement Input Handling
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP and self.engine.direction != "DOWN": self.engine.direction = "UP"
                if event.key == K_DOWN and self.engine.direction != "UP": self.engine.direction = "DOWN"
                if event.key == K_LEFT and self.engine.direction != "RIGHT": self.engine.direction = "LEFT"
                if event.key == K_RIGHT and self.engine.direction != "LEFT": self.engine.direction = "RIGHT"
        return True

    def game_over_screen(self):
        """ Display results and offer to Retry or go to Menu """
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", (240, 150), RED)

        score = self.engine.score
        level = self.engine.level
        pb = self.engine.personal_best

        self.draw_text(f"Final Score: {score}", (250, 250), WHITE)
        self.draw_text(f"Level Reached: {level}", (250, 290), WHITE)
        self.draw_text(f"Personal Best: {pb}", (250, 330), ORANGE)

        self.draw_text("Press [R] to Retry", (240, 450), GREEN)
        self.draw_text("Press [M] for Main Menu", (240, 500), WHITE)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT: return False
            if event.type == KEYDOWN:
                if event.key == K_r:
                    self.engine = GameEngine(self.username, self.db)
                    self.state = "PLAYING"
                if event.key == K_m:
                    self.state = "MENU"
        return True

    def leaderboard_screen(self):
        """ Fetch and display the top 10 scores from the Database """
        self.screen.fill(BLACK)
        self.draw_text("LEADERBOARD", (250, 50), CYAN)

        y_offset = 120
        for i, (user, score, lvl, date) in enumerate(self.current_scores):
            txt = f"{i+1}. {user} - {score} (Lvl {lvl})"
            self.draw_text(txt, (150, y_offset))
            y_offset += 30

        self.draw_text("Press M for Menu", (230, 600), GREEN)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT: return False
            if event.type == KEYDOWN:
                if event.key == K_m: self.state = "MENU"
        return True

    def settings_screen(self):
        """ Modify and save user preferences (grid, sound, color) to JSON """
        if not hasattr(self, 'temp_settings'):
            with open("settings.json", "r") as f:
                self.temp_settings = json.load(f)

        self.screen.fill(BLACK)
        self.draw_text("SETTINGS", (280, 50), YELLOW)

        grid_status = "ON" if self.temp_settings["grid"] else "OFF"
        sound_status = "ON" if self.temp_settings["sound"] else "OFF"
        color = self.temp_settings["snake_color"]

        self.draw_text(f"1. Grid: {grid_status} [Press G]", (150, 200))
        self.draw_text(f"2. Sound: {sound_status} [Press S]", (150, 250))
        self.draw_text(f"3. Snake Color: {color} [Press C]", (150, 300), color)
        self.draw_text("Press ENTER to Save & Back", (180, 500), GREEN)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT: return False
            if event.type == KEYDOWN:
                if event.key == K_g:
                    self.temp_settings["grid"] = not self.temp_settings["grid"]
                if event.key == K_s:
                    self.temp_settings["sound"] = not self.temp_settings["sound"]
                if event.key == K_c:
                    # Cycle through basic colors
                    colors = [[0, 255, 0], [255, 0, 0], [0, 0, 255], [255, 255, 0]]
                    curr_idx = colors.index(self.temp_settings["snake_color"])
                    self.temp_settings["snake_color"] = colors[(curr_idx + 1) % len(colors)]

                if event.key == K_RETURN:
                    with open("settings.json", "w") as f:
                        json.dump(self.temp_settings, f)
                    if self.engine:
                        self.engine.settings = self.temp_settings.copy()
                    delattr(self, 'temp_settings')
                    self.state = "MENU"
        return True

    # --- MAIN EXECUTION ---

    def run(self):
        """ Main state controller for the application """
        running = True
        while running:
            if self.state == "MENU":
                running = self.menu_screen()
            elif self.state == "PLAYING":
                running = self.game_loop()
            elif self.state == "GAMEOVER":
                running = self.game_over_screen()
            elif self.state == "LEADERBOARD":
                running = self.leaderboard_screen()
            elif self.state == "SETTINGS":
                running = self.settings_screen()

            self.clock.tick(30)
        pygame.quit()

if __name__ == "__main__":
    app = SnakeApp()
    app.run()
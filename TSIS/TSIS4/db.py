import psycopg2
from datetime import datetime

class Database:
    def __init__(self):
        """
        Initialize the database connection.
        Includes a timeout to prevent the game from freezing if the DB is offline.
        """
        try:
            self.conn = psycopg2.connect(
                dbname="snake_db",
                user="postgres",
                password="hpbmphpbmp", # Check your actual PostgreSQL password here!
                host="localhost",
                connect_timeout=3      # Connection attempt will stop after 3 seconds
            )
            self.cursor = self.conn.cursor()
            self._create_tables()      # Automatically set up schema on startup
            print("Database connected successfully!")
        except Exception as e:
            print(f"DATABASE ERROR: {e}")
            self.conn = None           # Fallback so the game doesn't crash without DB

    # --- Schema Setup ---

    def _create_tables(self):
        """
        Create the required tables if they do not already exist.
        Includes players for identity and game_sessions for history.
        """
        # Task 3.1: Implement suggested schema
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            );
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            );
        """)
        self.conn.commit()

    # --- Player Management ---

    def get_or_create_player(self, username):
        """
        Handles Task 3.1.1: Username entry.
        Inserts a new user if they don't exist, otherwise fetches the existing ID.
        """
        # ON CONFLICT prevents errors if the username is already taken
        self.cursor.execute(
            "INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING",
            (username,)
        )
        self.cursor.execute("SELECT id FROM players WHERE username = %s", (username,))
        self.conn.commit()
        return self.cursor.fetchone()[0]

    # --- Statistics and Saving ---

    def save_session(self, player_id, score, level):
        """
        Handles Task 3.1.2: Automatically save results after Game Over.
        Saves the score, level, and current timestamp.
        """
        self.cursor.execute(
            "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
            (player_id, score, level)
        )
        self.conn.commit()

    def get_leaderboard(self):
        """
        Handles Task 3.1.3: Fetch the top 10 all-time scores.
        Joins players and sessions to display usernames instead of IDs.
        """
        self.cursor.execute("""
            SELECT p.username, g.score, g.level_reached, g.played_at
            FROM game_sessions g
            JOIN players p ON g.player_id = p.id
            ORDER BY g.score DESC LIMIT 10
        """)
        return self.cursor.fetchall()

    def get_personal_best(self, player_id):
        """
        Handles Task 3.1.4: Fetch the player's best score.
        Used to display the PB during gameplay and on the Game Over screen.
        """
        self.cursor.execute(
            "SELECT MAX(score) FROM game_sessions WHERE player_id = %s",
            (player_id,)
        )
        res = self.cursor.fetchone()[0]
        return res if res else 0 # Returns 0 if the player has no previous sessions
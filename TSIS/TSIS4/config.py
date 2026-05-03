import pygame

# Screen Settings
WINDOW_SIZE = (700, 700)
BLOCK_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (40, 40, 40)
BLUE = (0, 0, 255)
GREEN = (34, 139, 34)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (160, 32, 240)
CYAN = (0, 255, 255)

# Food Types
FOOD_TYPES = [
    {"value": 1, "color": RED, "lifetime": 8, "type": "normal"},
    {"value": 2, "color": ORANGE, "lifetime": 5, "type": "normal"},
    {"value": 3, "color": YELLOW, "lifetime": 3, "type": "normal"},
    {"value": 0, "color": DARK_RED, "lifetime": 10, "type": "poison"}
]

# Power-up Types
POWER_UPS = [
    {"name": "Speed Boost", "color": CYAN, "duration": 5000, "effect": "speed_up"},
    {"name": "Slow Motion", "color": PURPLE, "duration": 5000, "effect": "speed_down"},
    {"name": "Shield", "color": GREEN, "duration": 0, "effect": "shield"}
]
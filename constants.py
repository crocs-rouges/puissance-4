import pygame

# Dimensions
CELL_SIZE = 80
ROWS = 6
COLS = 7
WIDTH = COLS * CELL_SIZE
HEIGHT = (ROWS + 1) * CELL_SIZE  # Added extra space for status text

# Colors
BLUE = (0, 123, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Animation
ANIMATION_SPEED = 20

# Victory Animation
VICTORY_FONT_SIZE = 72
VICTORY_TEXT_COLOR = WHITE
VICTORY_OVERLAY_COLOR = (0, 0, 0, 180)  # Semi-transparent black
VICTORY_ANIMATION_SPEED = 2
PARTICLE_COUNT = 50
PARTICLE_SPEED = 3
PARTICLE_SIZE = 8
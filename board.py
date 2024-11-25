import pygame
from constants import *

class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    def is_valid_move(self, col):
        return 0 <= col < COLS and self.grid[0][col] == 0

    def get_next_row(self, col):
        for row in range(ROWS-1, -1, -1):
            if self.grid[row][col] == 0:
                return row
        return -1

    def make_move(self, row, col, player):
        self.grid[row][col] = player

    def check_win(self, row, col, player):
        # Horizontal
        for c in range(max(0, col-3), min(col+1, COLS-3)):
            if all(self.grid[row][c+i] == player for i in range(4)):
                return True

        # Vertical
        for r in range(max(0, row-3), min(row+1, ROWS-3)):
            if all(self.grid[r+i][col] == player for i in range(4)):
                return True

        # Diagonal /
        for i in range(-3, 1):
            r, c = row+i, col-i
            if (0 <= r <= ROWS-4 and 0 <= c <= COLS-4 and
                all(self.grid[r+j][c+j] == player for j in range(4))):
                return True

        # Diagonal \
        for i in range(-3, 1):
            r, c = row+i, col+i
            if (0 <= r <= ROWS-4 and 0 <= c <= COLS-4 and
                all(self.grid[r+j][c-j] == player for j in range(4))):
                return True

        return False

    def draw(self, screen):
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(screen, BLUE, 
                               (col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                color = WHITE
                if self.grid[row][col] == 1:
                    color = RED
                elif self.grid[row][col] == 2:
                    color = YELLOW
                pygame.draw.circle(screen, color,
                                 (col*CELL_SIZE + CELL_SIZE//2,
                                  row*CELL_SIZE + CELL_SIZE//2),
                                 CELL_SIZE//2 - 5)
import random

class ComputerPlayer:
    def __init__(self):
        self.difficulty = "medium"

    def get_move(self, board):
        if self.difficulty == "easy":
            return self.random_move(board)
        else:
            return self.smart_move(board)

    def random_move(self, board):
        valid_moves = [col for col in range(7) if board.is_valid_move(col)]
        return random.choice(valid_moves) if valid_moves else 0

    def smart_move(self, board):
        # Check for winning move
        for col in range(7):
            if board.is_valid_move(col):
                row = board.get_next_row(col)
                board.grid[row][col] = 2
                if board.check_win(row, col, 2):
                    board.grid[row][col] = 0
                    return col
                board.grid[row][col] = 0

        # Block opponent's winning move
        for col in range(7):
            if board.is_valid_move(col):
                row = board.get_next_row(col)
                board.grid[row][col] = 1
                if board.check_win(row, col, 1):
                    board.grid[row][col] = 0
                    return col
                board.grid[row][col] = 0

        # Default to random move
        return self.random_move(board)
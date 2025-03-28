from algorithms import Base
import random

class UniformRandom(Base):
    # Select a valid move from the game (Check top row of every column, if '0' valid move)
    def get_valid_move(self, board):

        valid_moves = []

        for col in range(7):
            if board[0][col] == 'O':
                valid_moves.append(col)  # assuming 0-based columns
        return valid_moves


    # Select random move from a valid move in board, return column
    def select_uniform_random(self, board):
        valid_move = self.get_valid_move(board)

        if not valid_move:
            return None

        return random.choice(valid_move)

    # Place player move in the board and return updated board
    def make_move(self, board, column, player):
        #Create new board to manipulate

        new_board = [row[:] for row in board]

        #Iterate thorugh row in reverse order
        for row in range(5, -1, -1):
            if new_board[row][column] == 'O':
                new_board[row][column] = player #place piece in lowest available slot
                break
        return new_board

import logging
from common.globals import Globals
from common.utils import Utils
from common.game_interface import GameInterface

class Connect4(GameInterface):
    """Implements the Connect Four game logic."""

    def __init__(self, board):
        """Initializes the Connect Four game with the given board."""
        self.logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
        self.board = [list(row) for row in board] 
    
    def is_valid_move(self, col):
        """Checks if a move is valid (column not full)."""
        return 0 <= col < 7 and self.board[0][col] == Globals.Players.O
    
    def get_next_board(self, col, player):
        """Returns the next board state after a move."""
        new_board = [row[:] for row in self.board]
        for row in range(5, -1, -1):
            if new_board[row][col] == Globals.Players.O:
                new_board[row][col] = player
                break
        return ["".join(row) for row in new_board]

    def check_win(self, player, verbosity):
        """Checks if the given player has won the game."""
        # Logic based on KeithGalli connect4 logic available at https://github.com/KeithGalli/Connect4-Python/blob/master/connect4.py
        for row_index, row in enumerate(self.board):
            for col in range(4):
                #Iterates in windows of 4 columns
                #Check horizontal locations for win
                if "".join(row[col:col + 4]) == player * 4:
                    Utils.log_message(self.logger, f"Horizontal win [{row_index},{col}] to [{row_index},{col + 4}]", verbosity, Globals.VerbosityLevels.VERBOSE)
                    return True
        for col in range(7):
            for row in range(3):
                #Iterates in windows of 3 rows
                #Check vertical locations for win
                if "".join([self.board[row + i][col] for i in range(4)]) == player * 4:
                    Utils.log_message(self.logger, f"Vertical win [{row},{col}] to [{row + 4},{col}]", verbosity, Globals.VerbosityLevels.VERBOSE)
                    return True
        for row in range(3):
            for col in range(4):
                #Iterates in windows of 4 rows x 4 columns
                #Check positively sloped diagonals
                if "".join([self.board[row + i][col + i] for i in range(4)]) == player * 4:
                    Utils.log_message(self.logger, f"Positively Sloped Diagonal win [{row},{col}] to [{row + 3},{col + 3}]", verbosity, Globals.VerbosityLevels.VERBOSE)
                    return True
        for row in range(3, 6):
            for col in range(4):
                #Iterates in windows of 4 rows x 4 columns
                #Check negatively sloped diagonals
                if "".join([self.board[row - i][col + i] for i in range(4)]) == player * 4:
                    Utils.log_message(self.logger, f"Positively Sloped Diagonal win [{row},{col}] to [{row - 3},{col + 3}]", verbosity, Globals.VerbosityLevels.VERBOSE)
                    return True
        return False

    def check_draw(self):
        """Checks if the game has ended in a draw."""
        for row in self.board:
            if Globals.Players.O in row:
                return False
        return True

    def evaluate_board(self, verbosity):
        """Evaluates the current board state (win, loss, draw, or None)."""
        if self.check_win(Globals.Players.Y, verbosity):
            return 1
        elif self.check_win(Globals.Players.R, verbosity):
            return -1
        elif self.check_draw():
            return 0
        else:
            return None
        
    def get_board(self):
        """Returns the current game board state."""
        return ["".join(row) for row in self.board]

    def get_num_cols(self):
        """Returns the number of columns in the game board."""
        if not self.board:  
            return 0  
        return len(self.board[0])
    
    def get_opponent(self, player):
        """Returns the opponent player ('R' or 'Y')."""
        return Globals.Players.R if player == Globals.Players.Y else Globals.Players.Y
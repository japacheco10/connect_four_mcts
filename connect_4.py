from common import Globals, Utils, GameInterface

class Connect4(GameInterface):
    """Implements the Connect Four game logic."""

    def __init__(self, board=None):
        """Initializes the Connect Four game with the given board."""
        self.logger_source = __name__ + "." + self.__class__.__name__
        if board is None:
            # Create an empty 6x7 board (6 rows, 7 columns)
            self.board = [[Globals.Players.O for _ in range(7)] for _ in range(6)]
        else:
            self.board = [list(row) for row in board]
        self.print_result = True
    
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

    def check_win(self, player):
        """Checks if the given player has won the game."""
        # Logic based on KeithGalli connect4 logic available at https://github.com/KeithGalli/Connect4-Python/blob/master/connect4.py
        for row_index, row in enumerate(self.board):
            for col in range(4):
                #Iterates in windows of 4 columns
                #Check horizontal locations for win
                if "".join(row[col:col + 4]) == player * 4:
                    if self.print_result:
                        Utils.log_message(f"Horizontal win [{row_index},{col}] to [{row_index},{col + 4}]", Globals.VerbosityLevels.VERBOSE, self.logger_source)
                    return True
        for col in range(7):
            for row in range(3):
                #Iterates in windows of 3 rows
                #Check vertical locations for win
                if "".join([self.board[row + i][col] for i in range(4)]) == player * 4:
                    if self.print_result:
                        Utils.log_message(f"Vertical win [{row},{col}] to [{row + 4},{col}]", Globals.VerbosityLevels.VERBOSE, self.logger_source)
                    return True
        for row in range(3):
            for col in range(4):
                #Iterates in windows of 4 rows x 4 columns
                #Check positively sloped diagonals
                if "".join([self.board[row + i][col + i] for i in range(4)]) == player * 4:
                    if self.print_result:
                        Utils.log_message(f"Positively Sloped Diagonal win [{row},{col}] to [{row + 3},{col + 3}]", Globals.VerbosityLevels.VERBOSE, self.logger_source)
                    return True
        for row in range(3, 6):
            for col in range(4):
                #Iterates in windows of 4 rows x 4 columns
                #Check negatively sloped diagonals
                if "".join([self.board[row - i][col + i] for i in range(4)]) == player * 4:
                    if self.print_result:
                        Utils.log_message(f"Positively Sloped Diagonal win [{row},{col}] to [{row - 3},{col + 3}]", Globals.VerbosityLevels.VERBOSE, self.logger_source)
                    return True
        return False

    def check_draw(self):
        """Checks if the game has ended in a draw."""
        for row in self.board:
            if Globals.Players.O in row:
                return False
        return True

    def evaluate_board(self, print_result:bool=True):
        self.print_result = print_result
        """Evaluates the current board state (win, loss, draw, or None)."""
        if self.check_win(Globals.Players.Y):
            return 1
        elif self.check_win(Globals.Players.R):
            return -1
        elif self.check_draw():
            return 0
        else:
            return None
    
    def set_board(self, new_board):
        """Sets the board state of the Connect4 object."""
        self.board = [list(row) for row in new_board]

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
    
    def copy_game(self):
        """Clones game."""
        return Connect4(self.get_board())
    
    def do_move(self, col, player):
        """Executes a move on the board."""
        if not self.is_valid_move(col):
            raise ValueError(f"Invalid move: Column {col + 1} is full.")
        for row in range(5, -1, -1):
            if self.board[row][col] == Globals.Players.O:
                self.board[row][col] = player
                self.last_move = (row, col)  #   Track the move
                return
        raise Exception("Should not reach here")
    
    def undo_move(self):
        """Undoes the last move on the board."""
        if self.last_move:
            row, col = self.last_move
            self.board[row][col] = Globals.Players.O
            self.last_move = None
        else:
            raise ValueError("Cannot undo: No move has been made.")
        
    def print_board(self):
        """Prints current board"""
        for row in self.get_board():
            Utils.log_message(row, Globals.VerbosityLevels.BRIEF, self.logger_source)
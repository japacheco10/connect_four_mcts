from abc import ABC, abstractmethod

class GameInterface(ABC):
    """
    Defines an interface for game-related operations that algorithms can use.
    This allows algorithms to be "game-agnostic"
    """
    @abstractmethod
    def is_valid_move(self, col):
        """Checks if a move is valid."""
        pass

    @abstractmethod
    def get_next_board(self, col, player):
        """Returns the next game board state after a move."""
        pass

    @abstractmethod
    def check_win(self, player):
        """Checks if the given player has won the game."""
        pass

    @abstractmethod
    def check_draw(self):
        """Checks if the game has ended in a draw."""
        pass

    @abstractmethod
    def evaluate_board(self):
        """Evaluates the current game board state (win, loss, draw, or None)."""
        pass
    
    @abstractmethod
    def set_board(self, new_board):
        """Sets the board state of the Connect4 object."""
        pass
    
    @abstractmethod
    def get_board(self):
        """Returns the current game board state."""
        pass

    @abstractmethod
    def get_num_cols(self):
        """Returns the number of columns in the game board."""
        pass

    @abstractmethod
    def get_opponent(self, player):
        """Returns the opponent player."""
        pass
    
    @abstractmethod
    def copy_game(self):
        """Creates and returns a copy of the game."""
        pass

    @abstractmethod
    def do_move(self):
        """Executes a move on the board."""
        pass

    @abstractmethod
    def undo_move(self):
        """Undoes the last move on the board."""
        pass
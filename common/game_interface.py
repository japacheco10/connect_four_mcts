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
    def get_board(self):
        """Returns the current game board state."""
        pass

    @abstractmethod
    def get_num_cols(self):
        """Returns the number of columns in the game board."""
        pass
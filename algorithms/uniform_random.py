import random
from algorithms import Base
from common import GameInterface, Globals

class UniformRandom(Base):
    """Implements the Uniform Random algorithm, which chooses moves randomly."""
    
    def __init__(self, simulations:int=0):
        super().__init__(simulations, __name__ + "." + self.__class__.__name__)
    def choose_move(self, game: GameInterface, player):
        """
        Chooses a random legal move.

        Args:
            game (GameInterface): An object representing the game.
            player (str): The current player ('R' or 'Y').
            
        Returns:
            int: The chosen move (column index), or None if no move is possible.
        """
        num_cols = game.get_num_cols()
        legal_moves = [col for col in range(num_cols) if game.is_valid_move(col)]
        if not legal_moves:
            return None
        move = random.choice(legal_moves)
        return move

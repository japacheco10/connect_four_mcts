import random, logging
from algorithms import Base
from common.utils import Utils
from common.globals import Globals
from common.game_interface import GameInterface

logger = logging.getLogger(__name__)

class UniformRandom(Base):
    """Implements the Uniform Random algorithm, which chooses moves randomly."""
    
    def choose_move(self, game: GameInterface, player, verbosity="None", simulations=0):
        """
        Chooses a random legal move.

        Args:
            game (GameInterface): An object representing the game.
            player (str): The current player ('R' or 'Y').
            verbosity (str, optional): The verbosity level ("None", "Brief", or "Verbose"). Defaults to "None".
            simulations (int, optional): The number of simulations to run. Defaults to 0.

        Returns:
            int: The chosen move (column index), or None if no move is possible.
        """
        num_cols = game.get_num_cols()
        legal_moves = [col for col in range(num_cols) if game.is_valid_move(col)]
        if not legal_moves:
            return None
        move = random.choice(legal_moves)
        Utils.log_message(logger, f"FINAL Move selected: {move}", verbosity, Globals.VerbosityLevels.BRIEF)
        return move

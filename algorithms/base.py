from abc import ABC, abstractmethod
from common.game_interface import GameInterface
from common.globals import Globals

class Base(ABC):
    """Abstract base class for all game-playing algorithms."""
    @abstractmethod
    def choose_move(self, game: GameInterface, player,  verbosity=Globals.VerbosityLevels.NONE, simulations=0):
        """
        Chooses a move for the given game state.

        Args:
            game (GameInterface): An object representing the game.
            player (str): The current player ('R' or 'Y').
            verbosity (str, optional): The verbosity level ("None", "Brief", or "Verbose"). Defaults to "None".
            simulations (int, optional): The number of simulations to run. Defaults to 0.

        Returns:
            int: The chosen move (column index), or None if no move is possible.
        """
        pass
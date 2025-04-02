from abc import ABC, abstractmethod
from common import GameInterface, Globals

class Base(ABC):
    def __init__(self, simulations:int=0, logger_source:str=None):
        """
        Initialize Algorithm
        Args:
            simulations (int, optional): The number of simulations to run. Defaults to 0.
            logger_source (str, optional): Name to set to the logger
        """
        self.simulations = simulations
        self.logger_source = logger_source

    """Abstract base class for all game-playing algorithms."""
    @abstractmethod
    def choose_move(self, game: GameInterface, player):
        """
        Chooses a move for the given game state.

        Args:
            game (GameInterface): An object representing the game.
            player (str): The current player ('R' or 'Y').

        Returns:
            int: The chosen move (column index), or None if no move is possible.
        """
        pass
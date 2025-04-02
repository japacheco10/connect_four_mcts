from abc import abstractmethod
from algorithms import Base, Node
from common import GameInterface

class MCTS(Base):
    """Abstract base class for Monte Carlo Tree Search algorithms."""
    def __init__(self, simulations:int=0):
        super().__init__(simulations, __name__ + "." + self.__class__.__name__)

    def choose_move(self, game: GameInterface, player):
        """
        Chooses a move for the given game state.
        """
        pass

    def selection(self, node, total_visits, is_max, current_game, path):
        """Performs the selection phase of MCTS."""
        pass

    def expansion(self, node, legal_moves, current_player, current_game, path):
        """Performs the expansion phase of MCTS."""
        pass

    def best_move(self, root, game):
        pass

    def backpropagation(self, path, result):
        """Performs the backpropagation phase of MCTS."""
        pass

    @abstractmethod
    def select_child(self, node, total_visits, is_max):
        """Selects the best child node."""
        pass

    @abstractmethod
    def rollout(self, game: GameInterface, player):
        """Performs a rollout of the game."""
        pass

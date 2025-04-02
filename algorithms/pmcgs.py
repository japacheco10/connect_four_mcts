from algorithms import MCTS
from common import GameInterface, Globals

class PMCGS(MCTS):
    """Implements the Pure Monte Carlo Game Search (PMCGS) algorithm."""
    def __init__(self, simulations:int=0):
        super().__init__(simulations, __name__ + "." + self.__class__.__name__)

    def choose_move(self, game: GameInterface, player):
        super().choose_move(game, player)
    
    def selection(self, node, total_visits, is_max, current_game, path):
        super().selection(node, total_visits, is_max, current_game, path)

    def expansion(self, node, legal_moves, current_player, current_game, path):
        super().expansion(self, node, legal_moves, current_player, current_game, path)

    def best_move(self, root, game):
        super().best_move(root, game)

    def backpropagation(self, path, result):
        super().backpropagation( path, result)
    
    def select_child(self, node, total_visits, is_max):
        pass

    def rollout(self, game: GameInterface, player):
        pass
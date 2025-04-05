from algorithms import MCTS, Node
from common import GameInterface, Globals, Utils
import random

class UCT(MCTS):
    def __init__(self, simulations:int=0):
        super().__init__(simulations, __name__ + "." + self.__class__.__name__)

    def choose_move(self, game: GameInterface, player):
        return super().choose_move(game, player)
    
    def search(self):
        super().search()

    def backpropagation(self, node: Node, outcome: int) -> None:
        super().backpropagation(node, outcome)

    def expansion(self, parent: Node, state: GameInterface) -> bool:
        return super().expansion(parent, state)

    def best_move(self, root=None):
        return super().best_move(root)
    
    def select_child(self, current_player:str) -> tuple:
        pass

    def rollout(self, state: GameInterface, current_player:str) -> int:
        pass
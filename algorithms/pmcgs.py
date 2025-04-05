from algorithms import MCTS, Node
from common import GameInterface, Globals, Utils
import random

class PMCGS(MCTS):
    """Implements the Pure Monte Carlo Game Search (PMCGS) algorithm."""
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
        """Selects a node to expand (randomly)."""
        node:Node = self.root
        state:GameInterface = self.game.copy_game()  # Use copy_game
        
        Utils.log_message(f"select_child: Starting at node ID {id(node)}",Globals.VerbosityLevels.NONE, self.logger_source)
        
        while node.children:
            children = list(node.children.values())
            node = random.choice(children)  # Random selection
            Utils.log_message(f"select_child: Selected child node ID {id(node)}, move: {node.move}, visits: {node.visits}, wins: {node.wins}",Globals.VerbosityLevels.NONE, self.logger_source)
            Utils.log_message(f"wi: {node.wins}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
            Utils.log_message(f"ni: {node.visits}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
            Utils.log_message(f"Move selected: {node.move + 1}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
            try:
                state.do_move(node.move, current_player)
            except ValueError:
                Utils.log_message(f"select_child: ValueError, returning node ID {id(node)}",Globals.VerbosityLevels.NONE, self.logger_source)
                return node, state

            current_player = self.game.get_opponent(current_player)  # Update player
            
        if self.expansion(node, state):
            node = random.choice(list(node.children.values()))
            Utils.log_message(f"select_child: Expanded, selected random child ID {id(node)}, move: {node.move}",Globals.VerbosityLevels.NONE, self.logger_source)
            
            try:
                state.do_move(node.move, current_player)
            except ValueError:
                Utils.log_message(f"select_child: ValueError after expansion, returning node ID {id(node)}",Globals.VerbosityLevels.NONE, self.logger_source)
                return node, state
        Utils.log_message(f"select_child: Returning node ID {id(node)}",Globals.VerbosityLevels.NONE, self.logger_source)
        return node, state

    def rollout(self, state: GameInterface, current_player:str) -> int:
        """Performs a rollout from the given state (randomly)."""
        Utils.log_message(f"rollout: Starting rollout from state",Globals.VerbosityLevels.NONE, self.logger_source)
        
        while state.evaluate_board(False) is None:
            legal_moves = [move for move in range(state.get_num_cols()) if state.is_valid_move(move)]
            if not legal_moves:
                Utils.log_message(f"rollout: Draw",Globals.VerbosityLevels.NONE, self.logger_source)
                return 0  # Draw
            move = random.choice(legal_moves)

            Utils.log_message(f"Move selected: {move + 1}", Globals.VerbosityLevels.VERBOSE, self.logger_source)

            Utils.log_message(f"rollout: Selected random move: {move}, player: {current_player}",Globals.VerbosityLevels.NONE, self.logger_source)
            try:
                state.do_move(move, current_player)
            except ValueError:
                Utils.log_message("rollout: Invalid move in rollout",Globals.VerbosityLevels.NONE, self.logger_source)
                return 0  # Invalid move
            current_player = state.get_opponent(current_player)  # Update player

        result = state.evaluate_board(False)
        Utils.log_message(f"TERMINAL NODE VALUE: {result}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
        Utils.log_message(f"rollout: Rollout ended with result: {result}",Globals.VerbosityLevels.NONE, self.logger_source)
        return result
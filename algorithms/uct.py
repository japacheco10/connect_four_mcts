from algorithms import MCTS, Node
from common import GameInterface, Globals, Utils
import random
import math

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
    
    def select_child(self, current_player: str, path: list) -> tuple:
        """Selects a node to expand (using UCT)."""
        node: Node = self.root
        state: GameInterface = self.game
        
        while node.children:
            children = list(node.children.values())
            best_value = float('-inf')
            best_child = None
            child_counter = 1
            
            for child in children:
                if child.visits == 0:
                    uct_value = float('inf')
                else:
                    c = math.sqrt(2)   
                    uct_value = (child.wins / child.visits) + c * (math.sqrt(math.log(node.visits) / child.visits))
                
                Utils.log_message(f"V{child_counter}: {uct_value:.2f} (wins={child.wins}, visits={child.visits})", Globals.VerbosityLevels.VERBOSE, self.logger_source)
                child_counter += 1  # Increment the counter

                if uct_value > best_value:
                    best_value = uct_value
                    best_child = child
            
            Utils.log_message(f"Best V#: {best_value:.2f}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
            node = best_child
            Utils.log_message(f"wi: {node.wins}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
            Utils.log_message(f"ni: {node.visits}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
            Utils.log_message(f"Move selected: {node.move + 1}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
            try:
                state.do_move(node.move, current_player)
                path.append((node.move, current_player))
            except ValueError:
                return node, state
            
            current_player = self.game.get_opponent(current_player)  # Update player
        
        if self.expansion(node, state):
            node = random.choice(list(node.children.values()))
            
            try:
                state.do_move(node.move, current_player)
                path.append((node.move, current_player))
            except ValueError:
                return node, state
        
        return node, state


    def rollout(self, state: GameInterface, current_player:str, path: list) -> int:
        """Performs a rollout from the given state (randomly)."""
        
        while state.evaluate_board(False) is None:
            legal_moves = [move for move in range(state.get_num_cols()) if state.is_valid_move(move)]
            if not legal_moves:
                return 0  # Draw
            move = random.choice(legal_moves)

            Utils.log_message(f"Move selected: {move + 1}", Globals.VerbosityLevels.VERBOSE, self.logger_source)

            try:
                state.do_move(move, current_player)
                path.append((move, current_player))
            except ValueError:
                return 0  # Invalid move
            current_player = state.get_opponent(current_player)  # Update player

        result = state.evaluate_board(False)
        Utils.log_message(f"TERMINAL NODE VALUE: {result}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
        return result
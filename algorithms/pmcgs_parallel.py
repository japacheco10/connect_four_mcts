def rollout_with_node(args):
    state, player, algorithm_class, simulations, node = args
    algo = algorithm_class(simulations=simulations)
    outcome = algo.rollout(state, player)
    return node, outcome

from algorithms import MCTS, Node
from common import GameInterface, Globals, Utils
import random

class PMCGSParallel(MCTS):
    """Implements the Pure Monte Carlo Game Search (PMCGS) algorithm."""
    def __init__(self, simulations:int=0):
        super().__init__(simulations, __name__ + "." + self.__class__.__name__)

    def choose_move(self, game: GameInterface, player):
        self.game = game
        self.root = Node()
        self.node_count = 0
        self.current_player = player

        self.search()  # calls the parallel version defined in this class

        return self.best_move()
    
    def search(self):
        from concurrent.futures import ProcessPoolExecutor

        root = self.root
        rollout_inputs = []

        # Selection in main thread
        for _ in range(self.simulations):
            node, state = self.select_child(self.current_player)

            rollout_inputs.append((
                state.copy_game(),
                self.current_player,
                self.__class__,
                self.simulations,
                node
            ))

        # Parallel rollout using top-level function
        with ProcessPoolExecutor() as executor:
           outcomes = list(executor.map(rollout_with_node, rollout_inputs))
        
        # Backpropagation in main thread
        for node, outcome in outcomes:
            self.backpropagation(node, outcome)
            self.node_count += 1

    def select_child(self, current_player:str, path: list = None) -> tuple:
        """Selects a node to expand (randomly)."""
        node:Node = self.root
        state:GameInterface = self.game
        
        while node.children:
            children = list(node.children.values())
            node = random.choice(children)  # Random selection
            Utils.log_message(f"wi: {node.wins}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
            Utils.log_message(f"ni: {node.visits}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
            Utils.log_message(f"Move selected: {node.move + 1}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
            try:
                state.do_move(node.move, current_player)
            except ValueError:
                return node, state

            current_player = self.game.get_opponent(current_player)  # Update player
            
        if self.expansion(node, state):
            node = random.choice(list(node.children.values()))
            
            try:
                state.do_move(node.move, current_player)
            except ValueError:
                return node, state
        return node, state

    def rollout(self, state: GameInterface, current_player: str, path=None) -> int:
        """Performs a rollout from the given state (randomly)."""
        
        while state.evaluate_board(False) is None:
            legal_moves = [move for move in range(state.get_num_cols()) if state.is_valid_move(move)]
            if not legal_moves:
                return 0  # Draw

            move = random.choice(legal_moves)

            Utils.log_message(f"Move selected: {move + 1}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
        
            try:
                state.do_move(move, current_player)
            except ValueError:
                return 0  # Invalid move

            current_player = state.get_opponent(current_player)  # Update player

        result = state.evaluate_board(False)
        Utils.log_message(f"TERMINAL NODE VALUE: {result}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
        return result

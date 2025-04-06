def rollout_with_node(args):
    state, player, algorithm_class, simulations, node = args
    algo = algorithm_class(simulations=simulations)
    outcome = algo.rollout(state, player)
    return node, outcome

from algorithms import MCTS, Node
from common import GameInterface, Globals, Utils
import random, math

class UCTImpParallel(MCTS):
    def __init__(self, simulations: int = 0):
        super().__init__(simulations, __name__ + "." + self.__class__.__name__)

    def choose_move(self, game: GameInterface, player):
        self.game = game
        self.root = Node()
        self.node_count = 0
        self.current_player = player

        self.search()
        return self.best_move()

    def search(self):
        from concurrent.futures import ProcessPoolExecutor

        rollout_inputs = []

        for _ in range(self.simulations):
            path = []  # path not needed here
            node, state = self.select_child(self.current_player, path)
            rollout_inputs.append((
                state.copy_game(),  # ensure isolation
                self.current_player,
                self.__class__,
                self.simulations,
                node
            ))

        with ProcessPoolExecutor() as executor:
            outcomes = list(executor.map(rollout_with_node, rollout_inputs))

        for node, outcome in outcomes:
            self.backpropagation(node, outcome)
            self.node_count += 1

    def backpropagation(self, node: Node, outcome: int) -> None:
        super().backpropagation(node, outcome)

    def expansion(self, parent: Node, state: GameInterface) -> bool:
        return super().expansion(parent, state)

    def best_move(self, root=None):
        return super().best_move(root)
    
    def get_column_bias(self, col):
        """Gets the column bias favoring columns closer to the center """
        num_columns = 7 
        center = num_columns // 2
        return 1.0 - (abs(center - col) / center)
    
    def select_child(self, current_player: str, path: list = None) -> tuple:
        """Selects a node to expand (using UCB1)."""
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
                    c = 1
                    bias = self.get_column_bias(child.move)
                    k = 0.5  
                    uct_value = (child.wins / child.visits) + c * math.sqrt(math.log(node.visits) / child.visits) + (k * bias / (child.visits + 1))

                if uct_value > best_value:
                    best_value = uct_value
                    best_child = child
                
                Utils.log_message(f"V{child_counter}: {uct_value:.2f} (wins={child.wins}, visits={child.visits})", Globals.VerbosityLevels.VERBOSE, self.logger_source)
                child_counter += 1  # Increment the counter
            
            Utils.log_message(f"Best V#: {best_value:.2f}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
            node = best_child
            Utils.log_message(f"wi: {node.wins}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
            Utils.log_message(f"ni: {node.visits}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
            Utils.log_message(f"Move selected: {node.move + 1}", Globals.VerbosityLevels.VERBOSE, self.logger_source)

            try:
                state.do_move(node.move, current_player)
            except ValueError:
                return node, state

            current_player = self.game.get_opponent(current_player)

        if self.expansion(node, state):
            node = random.choice(list(node.children.values()))
            
            try:
                state.do_move(node.move, current_player)
            except ValueError:
                return node, state

        return node, state

    def rollout(self, state: GameInterface, current_player: str, path: list = None) -> int:
        
        while state.evaluate_board(False) is None:
            legal_moves = [move for move in range(state.get_num_cols()) if state.is_valid_move(move)]
            if not legal_moves:
                return 0

            move = random.choice(legal_moves)
            Utils.log_message(f"Move selected: {move + 1}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
            
            try:
                state.do_move(move, current_player)
            except ValueError:
                return 0

            current_player = state.get_opponent(current_player)

        result = state.evaluate_board(False)
        Utils.log_message(f"TERMINAL NODE VALUE: {result}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
        return result

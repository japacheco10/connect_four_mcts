def rollout_with_node(args):
    state, player, algorithm_class, simulations, node = args
    algo = algorithm_class(simulations=simulations)
    outcome = algo.rollout(state, player)
    return node, outcome

from algorithms import MCTS, Node
from common import GameInterface, Globals, Utils
import random, math

class UCTParallel(MCTS):
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

        Utils.log_message("search: Starting UCT search with parallel rollouts", Globals.VerbosityLevels.NONE, self.logger_source)
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

        Utils.log_message("search: Parallel UCT search complete", Globals.VerbosityLevels.NONE, self.logger_source)

    def backpropagation(self, node: Node, outcome: int) -> None:
        super().backpropagation(node, outcome)

    def expansion(self, parent: Node, state: GameInterface) -> bool:
        return super().expansion(parent, state)

    def best_move(self, root=None):
        return super().best_move(root)

    def select_child(self, current_player: str, path: list = None) -> tuple:
        """Selects a node to expand (using UCB1)."""
        node: Node = self.root
        state: GameInterface = self.game
        Utils.log_message(f"select_child: Starting at node ID {id(node)}", Globals.VerbosityLevels.NONE, self.logger_source)

        while node.children:
            best_value = float('-inf')
            best_child = None

            for child in node.children.values():
                if child.visits == 0:
                    uct_value = float('inf')
                else:
                    c = math.sqrt(2)  # exploration constant
                    uct_value = (child.wins / child.visits) + c * math.sqrt(math.log(node.visits) / child.visits)

                if uct_value > best_value:
                    best_value = uct_value
                    best_child = child

            node = best_child
            Utils.log_message(f"select_child: Selected child node ID {id(node)}, move: {node.move}, visits: {node.visits}, wins: {node.wins}", Globals.VerbosityLevels.NONE, self.logger_source)
            Utils.log_message(f"wi: {node.wins}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
            Utils.log_message(f"ni: {node.visits}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
            Utils.log_message(f"Move selected: {node.move + 1}", Globals.VerbosityLevels.VERBOSE, self.logger_source)

            try:
                state.do_move(node.move, current_player)
            except ValueError:
                Utils.log_message(f"select_child: ValueError, returning node ID {id(node)}", Globals.VerbosityLevels.NONE, self.logger_source)
                return node, state

            current_player = self.game.get_opponent(current_player)

        if self.expansion(node, state):
            node = random.choice(list(node.children.values()))
            Utils.log_message(f"select_child: Expanded, selected random child ID {id(node)}, move: {node.move}", Globals.VerbosityLevels.NONE, self.logger_source)

            try:
                state.do_move(node.move, current_player)
            except ValueError:
                Utils.log_message(f"select_child: ValueError after expansion, returning node ID {id(node)}", Globals.VerbosityLevels.NONE, self.logger_source)
                return node, state

        Utils.log_message(f"select_child: Returning node ID {id(node)}", Globals.VerbosityLevels.NONE, self.logger_source)
        return node, state

    def rollout(self, state: GameInterface, current_player: str, path: list = None) -> int:
        Utils.log_message("rollout: Starting rollout from state", Globals.VerbosityLevels.NONE, self.logger_source)

        while state.evaluate_board(False) is None:
            legal_moves = [move for move in range(state.get_num_cols()) if state.is_valid_move(move)]
            if not legal_moves:
                Utils.log_message("rollout: Draw", Globals.VerbosityLevels.NONE, self.logger_source)
                return 0

            move = random.choice(legal_moves)
            Utils.log_message(f"Move selected: {move + 1}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
            Utils.log_message(f"rollout: Selected random move: {move}, player: {current_player}", Globals.VerbosityLevels.NONE, self.logger_source)

            try:
                state.do_move(move, current_player)
            except ValueError:
                Utils.log_message("rollout: Invalid move in rollout", Globals.VerbosityLevels.NONE, self.logger_source)
                return 0

            current_player = state.get_opponent(current_player)

        result = state.evaluate_board(False)
        Utils.log_message(f"TERMINAL NODE VALUE: {result}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
        Utils.log_message(f"rollout: Rollout ended with result: {result}", Globals.VerbosityLevels.NONE, self.logger_source)
        return result

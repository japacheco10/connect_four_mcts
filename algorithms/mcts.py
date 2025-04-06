from abc import abstractmethod
from algorithms import Base, Node
from common import GameInterface, Utils, Globals
import time, random

class MCTS(Base):
    """Abstract base class for Monte Carlo Tree Search algorithms."""
    def __init__(self, simulations:int=0, logger_source:str=None):
        super().__init__(simulations, logger_source if logger_source is not None else __name__ + "." + self.__class__.__name__)
        self.game:GameInterface = None
        self.root:Node = None
        self.node_count = 0
        self.current_player = None

    def choose_move(self, game: GameInterface, player):
        """
        Chooses a move for the given game state.

        Args:
            game (GameInterface): The game interface.
            player (str): The current player.

        Returns:
            int: The chosen move (column index), or None if no move is possible.
        """
        self.game = game
        self.root = Node()
        self.node_count = 0
        self.current_player = player

        self.search()

        return self.best_move()
    
    def search(self):
        """Performs the MCTS search for the given number of iterations."""
        start_time = time.process_time()
        for _ in range(self.simulations):
            path = []  # Track moves made
            node, state = self.select_child(self.current_player, path)
            outcome = self.rollout(state, self.current_player, path)
            self.backpropagation(node, outcome)

            # Undo all moves made in this iteration
            for move, _ in reversed(path):
                state.undo_move()

            self.node_count += 1  # Increment node_count
            Utils.log_message("-----------------------------------------",Globals.VerbosityLevels.VERBOSE, self.logger_source)

        self.run_time = time.process_time() - start_time

    def backpropagation(self, node: Node, outcome: int) -> None:
        """Backpropagates the result of the rollout."""

        reward = 0
        if outcome == 1:
            reward = 1
        elif outcome == -1:
            reward = -1

        while node is not None:
            node.visits += 1

            # Apply reward based on the perspective of the player who made the move to reach this node
            if node.parent is not None: # For non-root nodes, the outcome is from the opponent's perspective in the parent
                node.parent.wins += -reward
            elif reward == 1: # For the root node, a win is a positive outcome
                node.wins += 1
            elif reward == -1: # For the root node, a loss is a negative outcome
                node.wins += -1

            Utils.log_message("Updated values:", Globals.VerbosityLevels.VERBOSE, self.logger_source)
            Utils.log_message(f"wi: {node.wins}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
            Utils.log_message(f"ni: {node.visits}", Globals.VerbosityLevels.VERBOSE, self.logger_source)

            node = node.parent

    def expansion(self, parent: Node, state: GameInterface) -> bool:
        """Expands the tree from the given node."""
        
        if state.evaluate_board(False) is not None:
            return False
        Utils.log_message("NODE ADDED", Globals.VerbosityLevels.VERBOSE, self.logger_source)
        
        legal_moves = [move for move in range(state.get_num_cols()) if state.is_valid_move(move)]
        children = [Node(move, parent) for move in legal_moves]
        parent.children = {child.move: child for child in children}
        self.node_count += len(children)  # Increment node_count

        return True
    
    def best_move(self, root=None):
        """Selects the best move after all simulations are completed."""
        if root is None:
            root = self.root

        if not root.children:
            legal_moves = [i for i in range(self.game.get_num_cols()) if self.game.is_valid_move(i)]
            if legal_moves:
                fallback = random.choice(legal_moves)
                return fallback
            else:
                return None

        best_move = -1
        best_value = float('-inf')
        move_values = [None] * self.game.get_num_cols()

        for move, child in root.children.items():
            if child.visits > 0:
                move_values[move] = child.wins / child.visits
            else:
                move_values[move] = None

        for move, value in enumerate(move_values):
            if value is not None and value > best_value:
                best_value = value
                best_move = move

        if Utils.get_verbosity_level() == Globals.VerbosityLevels.VERBOSE:
            for i in range(self.game.get_num_cols()):
                if self.game.is_valid_move(i):
                    if move_values[i] is not None:
                        Utils.log_message(f"Column {i + 1}: {move_values[i]:.2f}", Globals.VerbosityLevels.VERBOSE, self.logger_source)
                    else:
                        Utils.log_message(f"Column {i + 1}: None", Globals.VerbosityLevels.VERBOSE, self.logger_source)
                else:
                    Utils.log_message(f"Column {i + 1}: Null", Globals.VerbosityLevels.VERBOSE, self.logger_source)

        # Final fallback if no best move found from visits
        if best_move == -1:
            legal_moves = [i for i in range(self.game.get_num_cols()) if self.game.is_valid_move(i)]
            if legal_moves:
                fallback = random.choice(legal_moves)
                return fallback
            else:
                return None

        return best_move
    
    @abstractmethod
    def select_child(self, current_player: str, path: list) -> tuple:
        """Selects a node to expand."""
        pass

    @abstractmethod
    def rollout(self, state: GameInterface, current_player: str, path: list) -> int:
        """Performs a rollout from the given state."""
        pass
class Node:
    """Represents a node in the game tree."""

    def __init__(self, move=None):
        self.move = move
        self.children = {}  # {move: Node}
        self.wins = 0
        self.visits = 0
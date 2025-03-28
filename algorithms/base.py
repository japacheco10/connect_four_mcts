from abc import ABC, abstractmethod
class Base(ABC):
    @abstractmethod
    def make_move(self, board, player):
        pass
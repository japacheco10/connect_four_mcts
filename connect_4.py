import logging
from common.utils import AlgorithmFactory

class Connect4():
    def __init__(self, algorithm_name:str, player:str, board:list, verbosity:str, iterations:int):
        self.logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
        self.current_player = player
        self.board = board
        self.verbosity = verbosity
        self.iterations = iterations
        self.algorithm = AlgorithmFactory.create_algorithm(algorithm_name.lower())
        
    def run(self):
        move = self.algorithm.make_move(self.board, self.current_player)
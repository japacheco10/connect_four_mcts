from .base import Base
from .uniform_random import UniformRandom
from .pmcgs import PureMonteCarloGameSearch
from .uct import UCT
from common.globals import Globals

class AlgorithmFactory():
    """
    A factory class for creating algorithm instances.
    """

    @staticmethod
    def create_algorithm(name: str):
        """
        Creates an algorithm instance based on the provided name.

        Args:
            name: The name of the algorithm to create.

        Returns:
            An instance of the specified algorithm class.

        Raises:
            ValueError: If the algorithm name is invalid.
        """
        try:
            # Use lowercase names and import classes with correct names.
            if name == Globals.Algorithms.UR:
                from algorithms.uniform_random import UniformRandom
                return UniformRandom()
            elif name == Globals.Algorithms.PMCGS:
                from algorithms.pmcgs import PureMonteCarloGameSearch
                return PureMonteCarloGameSearch()
            elif name == Globals.Algorithms.UCT:
                from algorithms.uct import UCT
                return UCT()
            else:
                raise ValueError(f"Invalid algorithm name: {name}")
        except ImportError as e:
            raise ValueError(f"Error importing algorithm: {e}")
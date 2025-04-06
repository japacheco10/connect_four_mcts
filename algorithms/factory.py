from common import Globals

class AlgorithmFactory():
    """
    A factory class for creating algorithm instances.
    """

    @staticmethod
    def create_algorithm(name: str, simulations:int=0, parallel:int=0):
        """
        Creates an algorithm instance based on the provided name.

        Args:
            name: The name of the algorithm to create.
            simulations (int, optional): The number of simulations to run. Defaults to 0.

        Returns:
            An instance of the specified algorithm class.

        Raises:
            ValueError: If the algorithm name is invalid.
        """
        try:
            # Use lowercase names and import classes with correct names.
            if name == Globals.Algorithms.UR:
                from algorithms import UniformRandom
                return UniformRandom()
            elif name == Globals.Algorithms.PMCGS:
                if parallel == 1:
                    from algorithms import PMCGSParallel
                    return PMCGSParallel(simulations)
                else:
                    from algorithms import PMCGS
                    return PMCGS(simulations)
            elif name == Globals.Algorithms.UCT:
                if parallel == 1:
                    from algorithms import UCTParallel
                    return UCTParallel(simulations)
                else:
                    from algorithms import UCT
                    return UCT(simulations)
            elif name == Globals.Algorithms.UCTIMP:
                if parallel == 1:
                    from algorithms import UCTImpParallel
                    return UCTImpParallel(simulations)
                else:
                    from algorithms import UCTImprovement
                    return UCTImprovement(simulations)
            else:
                raise ValueError(f"Invalid algorithm name: {name}")
        except ImportError as e:
            raise ValueError(f"Error importing algorithm: {e}")
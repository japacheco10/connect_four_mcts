import argparse
import os
import logging
import logging.config

class Utils():
    @staticmethod
    def get_base_dir():
        return os.path.dirname(os.path.dirname(__file__)) # Go one directory up from common.

    @staticmethod
    def init():
        """
        Initializes program global resources.
        """
        basedir = Utils.get_base_dir()
        os.makedirs(os.path.join(basedir, "_logs"), exist_ok=True)
        logging.config.fileConfig(os.path.join(basedir, "_resources", "config", 'log.ini'), disable_existing_loggers=False)

    @staticmethod
    def file_exists(path):
        """
        Validates if a file exists, either as an absolute path or relative to the program's base directory.

        Args:
            path (str): The file path to validate.

        Returns:
            str: The absolute file path when valid.

        Raises:
            argparse.ArgumentTypeError: If the file does not exist or is not a file.
        """
        absolute_path = os.path.abspath(path)
        relative_path = os.path.join(Utils.get_base_dir(), path)

        if not os.path.exists(absolute_path) and not os.path.exists(relative_path):
            raise argparse.ArgumentTypeError(f"'{path}' does not exist.")

        if os.path.exists(absolute_path) and os.path.isfile(absolute_path):
            return absolute_path

        if os.path.exists(relative_path) and os.path.isfile(relative_path):
            return relative_path

        raise argparse.ArgumentTypeError(f"'{path}' is not a valid file.")

    @staticmethod
    def validate_arguments():
        """
        Validates command-line arguments for the game initialization.

        Parses the input file path, verbosity level, and number of iterations.

        Returns:
            tuple: A tuple containing the validated input file path (str), verbosity level (str),
                   and number of iterations (int).

        Raises:
            argparse.ArgumentTypeError: If the input file does not exist.
            SystemExit: If any of the arguments are invalid.
        """
        parser = argparse.ArgumentParser(description="Validate arguments")
        parser.add_argument(
            "input_file",
            help="Input file with game initialization settings.",
            type=Utils.file_exists
        )
        parser.add_argument(
            "verbosity",
            type=str,
            choices=['Verbose', 'Brief', 'None'],
            help="Verbosity level. Values supported: Verbose, Brief, None"
        )
        parser.add_argument(
            "iterations",
            type=int,
            help="Indicates number of simulations."
        )
        args = parser.parse_args()

        return args.input_file, args.verbosity, args.iterations

    @staticmethod
    def load_game_settings(path):
        """
        Loads game settings.

        Args:
            path (str): The file path to validate.

        Returns:
            tuple: Algorithm name, current player, board.
        """
        with open(path, 'r') as f:
            lines = f.readlines()

        algorithm_name = lines[0].strip()
        current_player = lines[1].strip()
        board = [list(line.strip()) for line in lines[2:]]

        return algorithm_name, current_player, board

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
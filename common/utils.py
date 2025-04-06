import argparse
import os
import logging
import logging.config
from common import Globals

class Utils():
    VERBOSITY = Globals.VerbosityLevels.NONE

    @staticmethod
    def get_verbosity_level():
        """Gets verbosity level"""
        return Utils.VERBOSITY
    
    @staticmethod
    def set_verbosity_level(verbosity:str):
        """
        Sets verbosity level
        Args:
            verbosity (str): The current verbosity level ("None", "Brief", or "Verbose").
        """
        Utils.VERBOSITY = verbosity.upper()

    @staticmethod
    def get_base_dir():
        """
        Gets base python application directory
        """
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
    def log_message(message: str, message_verbosity: str, source: str = None):
        """
        Logs a message based on the current and message verbosity levels.

        Args:
            message (str): The message to log.
            message_verbosity (str): The verbosity level required to log the message.
            source (str): logging instance from the file/class calling the log_message method
        """
        verbosity_levels = {Globals.VerbosityLevels.NONE: 0, Globals.VerbosityLevels.BRIEF: 1, Globals.VerbosityLevels.VERBOSE: 2, Globals.VerbosityLevels.ERROR: 3}
        if message_verbosity != Globals.VerbosityLevels.NONE and (verbosity_levels.get(Utils.get_verbosity_level(), 0) >=
            verbosity_levels.get(message_verbosity, 0)):
            print(message)
        
        if source is not None:
            logger = logging.getLogger(source)
            log_levels = {
                Globals.VerbosityLevels.VERBOSE: logger.debug,
                Globals.VerbosityLevels.BRIEF: logger.info,
                Globals.VerbosityLevels.ERROR: logger.error,
                Globals.VerbosityLevels.NONE: logger.debug
            }
            log_func = log_levels.get(message_verbosity, logger.error)  
            log_func(message)

    @staticmethod
    def load_game_settings(path):
        """
        Loads game settings.

        Args:
            path (str): The file path to validate.

        Returns:
            tuple: Algorithm name, player, board.
        """
        with open(path, 'r') as f:
            lines = f.readlines()

        algorithm_name = lines[0].strip()
        player = lines[1].strip()
        board = [list(line.strip()) for line in lines[2:]]

        return algorithm_name, player, board
    
    @staticmethod
    def load_tournament_config():
        """Loads the tournament configuration from a file."""
        config = []
        with open(Utils.file_exists("_resources/config/tournament_config.txt"), 'r') as file:
            lines = file.readlines()
            max_proc = int(lines[0].strip())  # Read number of processors to run parallel games
            num_games = int(lines[1].strip())  # Read number of games from the first line
            parallel = int(lines[2].strip())  # Read if algorithm parallel processing should be enabled
            for line in lines[3:]:  # Read algorithm configurations from the rest
                algorithm, simulations = line.strip().split(',')
                config.append((algorithm, int(simulations)))
        return max_proc, num_games, parallel, config
    
    @staticmethod
    def load_single_match_config():
        """Loads the single match configuration from a file."""
        config = []
        with open(Utils.file_exists("_resources/config/single_match_config.txt"), 'r') as file:
            lines = file.readlines()
            verbosity = lines[0].strip()  # Read verbosity level
            num_games = int(lines[1].strip())  # Read number of games from the first line
            for line in lines[2:4]:  # Read algorithm configurations from the rest
                algorithm, simulations = line.strip().split(',')
                config.append((algorithm, int(simulations)))
        return verbosity, num_games, config
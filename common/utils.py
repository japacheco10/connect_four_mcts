import argparse
import os
import logging
import logging.config
from common.globals import Globals

class Utils():
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
    def log_message(logger: logging.Logger, message: str, current_verbosity: str, message_verbosity: str, message_log_level: str = Globals.LogLevels.INFO):
        """
        Logs a message based on the current and message verbosity levels.

        Args:
            logger (Logger): logging instance from the file/class calling the log_message method
            message (str): The message to log.
            current_verbosity (str): The current verbosity level ("None", "Brief", or "Verbose").
            message_verbosity (str): The verbosity level required to log the message.
            message_log_level (str): The log level required to log the message (Debug, Info, Warn, Error, Critical). Default Info
        """
        verbosity_levels = {"None": 0, "Brief": 1, "Verbose": 2}
        if current_verbosity != Globals.VerbosityLevels.NONE and (verbosity_levels.get(current_verbosity, 0) >=
            verbosity_levels.get(message_verbosity, 0)):
            print(message)

        log_levels = {
            "Debug": logger.debug,
            "Info": logger.info,
            "Warning": logger.warning,
            "Error": logger.error,
            "Critical": logger.critical
        }
        log_func = log_levels.get(message_log_level, logger.info)  
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
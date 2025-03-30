import logging, traceback, sys
from common.globals import Globals
from common.utils import Utils
from connect_4 import Connect4
from algorithms import AlgorithmFactory

logger = None

def main():
    try:
        Utils.log_message(logger, "Init Start", Globals.VerbosityLevels.NONE, Globals.VerbosityLevels.NONE, Globals.LogLevels.DEBUG)
        input_file, verbosity, simulations = Utils.validate_arguments()
        algorithm_name, player, board = Utils.load_game_settings(input_file)
        Utils.log_message(logger, "Init End", Globals.VerbosityLevels.NONE, Globals.VerbosityLevels.NONE, Globals.LogLevels.DEBUG)
        
        Utils.log_message(logger, "Starting Game", Globals.VerbosityLevels.NONE, Globals.VerbosityLevels.NONE, Globals.LogLevels.DEBUG)
        play_game(algorithm_name, player, board, verbosity, simulations)
        Utils.log_message(logger, "Ending Game", Globals.VerbosityLevels.NONE, Globals.VerbosityLevels.NONE, Globals.LogLevels.DEBUG)
    except:
        Utils.log_message(logger, f"Uncaught exception: {traceback.format_exc()}", Globals.VerbosityLevels.NONE, Globals.VerbosityLevels.NONE, Globals.LogLevels.CRITICAL)
        sys.exit(1)

def play_game(algorithm_name, initial_player, initial_board, verbosity, simulations):
    """Plays a full game of Connect Four.
    Args:
        algorithm_name (str): The name of the algorithm to use for move selection.
        initial_player (str): The player who makes the first move ('R' or 'Y').
        initial_board (list[str]): The initial state of the Connect Four board.
        verbosity (str): The verbosity level for logging ("None", "Brief", or "Verbose").
        simulations (int): The number of simulations to run (used by some algorithms).
    """
    try:
        game = Connect4(initial_board)
        algorithm = AlgorithmFactory.create_algorithm(algorithm_name)
        current_player = initial_player
        current_board = game.get_board()

        while True:
            Utils.log_message(logger, f"Current player {current_player}", verbosity, Globals.VerbosityLevels.VERBOSE)
            move = algorithm.choose_move(game, current_player, verbosity, simulations)
            if move is not None:
                current_board = Connect4(current_board).get_next_board(move, current_player)
                game.board = Connect4(current_board).board  # Update the game board
                for row in game.get_board():
                    Utils.log_message(logger, row, verbosity, Globals.VerbosityLevels.VERBOSE)
                
            game_over_state = game.evaluate_board(verbosity)  # Evaluate the *current* state

            if game_over_state is not None or move is None:  # Game over or no move
                if game_over_state == 0:
                    Utils.log_message(logger, "Draw!", verbosity, Globals.VerbosityLevels.NONE)
                elif game_over_state == 1:
                    Utils.log_message(logger, f"{Globals.Players.Y} wins!", verbosity, Globals.VerbosityLevels.NONE)
                elif game_over_state == -1:
                    Utils.log_message(logger, f"{Globals.Players.R} wins!", verbosity, Globals.VerbosityLevels.NONE)
                elif move is None:
                    Utils.log_message(logger, f"No valid moves for {current_player}. Game over.",verbosity, Globals.VerbosityLevels.NONE)
                break

            current_player = game.get_opponent(current_player)
            
        Utils.log_message(logger, "Final Board:", verbosity, Globals.VerbosityLevels.NONE)
        for row in game.get_board():
            Utils.log_message(logger, row, verbosity, Globals.VerbosityLevels.NONE)
    except:
        Utils.log_message(logger, f"Uncaught exception: {traceback.format_exc()}", Globals.VerbosityLevels.NONE, Globals.VerbosityLevels.NONE, Globals.LogLevels.CRITICAL)
        sys.exit(1)

if __name__ == "__main__":
    """Main entry point of the script."""
    Utils.init()
    logger = logging.getLogger(__name__)
    main()

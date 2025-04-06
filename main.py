import traceback, sys
from common import Globals, Utils
from connect_4 import Connect4
from algorithms import AlgorithmFactory

def main():
    try:
        input_file, verbosity, simulations = Utils.validate_arguments()
        Utils.set_verbosity_level(verbosity)
        algorithm_name, player, board = Utils.load_game_settings(input_file)
        
        play_game(algorithm_name, player, board, simulations)
    except:
        Utils.log_message(f"Uncaught exception: {traceback.format_exc()}", Globals.VerbosityLevels.ERROR, __name__)
        sys.exit(1)

def play_game(algorithm_name, initial_player, initial_board, simulations):
    """Plays a full game of Connect Four.
    Args:
        algorithm_name (str): The name of the algorithm to use for move selection.
        initial_player (str): The player who makes the first move ('R' or 'Y').
        initial_board (list[str]): The initial state of the Connect Four board.
        simulations (int): The number of simulations to run (used by some algorithms).
    """
    try:
        game = Connect4(initial_board)
        Utils.log_message("Initial Board:", Globals.VerbosityLevels.BRIEF, __name__)
        game.print_board()
        algorithm = AlgorithmFactory.create_algorithm(algorithm_name, simulations)
        current_player = initial_player

        while True:
            Utils.log_message(f"Current player {current_player}", Globals.VerbosityLevels.BRIEF, __name__)
            move = algorithm.choose_move(game, current_player)
            Utils.log_message(f"FINAL Move selected: {move}", Globals.VerbosityLevels.BRIEF, __name__)
            if move is not None:
                game.set_board(game.get_next_board(move, current_player))
                Utils.log_message("Current Board:", Globals.VerbosityLevels.BRIEF, __name__)
                game.print_board()
                
            game_state = game.evaluate_board()  # Evaluate the *current* state

            if game_state is not None or move is None:  # Game over or no move
                if game_state == 0:
                    Utils.log_message("**** Draw! ****", Globals.VerbosityLevels.BRIEF, __name__)
                elif game_state == 1:
                    Utils.log_message(f"**** {Globals.Players.Y} wins! ****", Globals.VerbosityLevels.BRIEF, __name__)
                elif game_state == -1:
                    Utils.log_message(f"**** {Globals.Players.R} wins! ****", Globals.VerbosityLevels.BRIEF, __name__)
                elif move is None:
                    Utils.log_message(f"No valid moves for {current_player}.", Globals.VerbosityLevels.BRIEF, __name__)
                break

            current_player = game.get_opponent(current_player)
            
        Utils.log_message("Final Board:", Globals.VerbosityLevels.BRIEF, __name__)
        game.print_board()
    except:
        Utils.log_message(f"Uncaught exception: {traceback.format_exc()}", Globals.VerbosityLevels.ERROR, __name__)
        sys.exit(1)

if __name__ == "__main__":
    """Main entry point of the script."""
    Utils.init()
    main()

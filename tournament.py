import traceback, sys
from common import Globals, Utils
from connect_4 import Connect4
from algorithms import AlgorithmFactory

def main():
    try:
        Utils.log_message("Init Start", Globals.VerbosityLevels.NONE, __name__)
        verbosity, num_games, algorithms = Utils.load_tournament_config()
        Utils.set_verbosity_level(verbosity)
        num_algorithms = len(algorithms)
        results = [[0] * num_algorithms for _ in range(num_algorithms)]  # 2D list to store results
        Utils.log_message("Init End", Globals.VerbosityLevels.NONE, __name__)
        
        Utils.log_message("Starting Tournament", Globals.VerbosityLevels.NONE, __name__)
        #   Tournament loop
        for i in range(num_algorithms):
            for j in range(num_algorithms):
                if i == j:
                    results[i][j] = "-"  # No game against itself
                    continue

                wins1 = 0
                wins2 = 0
                draws = 0

                for g in range(num_games):
                    print("-------------------------------------------------------------------------")
                    print(f"Game [{g+1}]")
                    print(f"[{algorithms[i][0]}] vs [{algorithms[j][0]}]")
                    print("-------------------------------------------------------------------------")
                    #   Create algorithm instances for each game
                    alg1 = AlgorithmFactory.create_algorithm(algorithms[i][0], simulations=algorithms[i][1])
                    alg2 = AlgorithmFactory.create_algorithm(algorithms[j][0], simulations=algorithms[j][1])

                    winner = play_game(alg1, alg2, Globals.Players.R)

                    if winner == -1: #Y
                        wins1 += 1
                    elif winner == 1: #R
                        wins2 += 1
                    else:
                        draws += 1

                results[i][j] = f"{wins1 / num_games * 100:.2f}%"  # Winning percentage for algorithm i

        #   Results presentation (table)
        print("Tournament Results (Winning Percentage for Row Algorithm vs. Column Algorithm)")
        print("-------------------------------------------------------------------------")
        print("      |", end="")
        for alg in algorithms:
            print(f"{alg[0]:8}|", end="")
        print()
        print("------|", end="")
        for _ in range(num_algorithms):
            print("--------|", end="")
        print()

        for i in range(num_algorithms):
            print(f"{algorithms[i][0]:8}|", end="")
            for j in range(num_algorithms):
                print(f"{results[i][j]:8}|", end="")
            print()
        print("-------------------------------------------------------------------------")
    
        Utils.log_message("Ending Tournament", Globals.VerbosityLevels.ERROR, __name__)
    except ValueError as e:
        Utils.log_message(f"Error: {e}", Globals.VerbosityLevels.ERROR, __name__)
        sys.exit(1)
    except:
        Utils.log_message(f"Uncaught exception: {traceback.format_exc()}", Globals.VerbosityLevels.ERROR, __name__)
        sys.exit(1)

def play_game(player1_alg, player2_alg, initial_player):
    """Plays a full game of Connect Four.
    Args:
        algorithm_name (str): The name of the algorithm to use for move selection.
        initial_player (str): The player who makes the first move ('R' or 'Y').
        initial_board (list[str]): The initial state of the Connect Four board.
        simulations (int): The number of simulations to run (used by some algorithms).
    """
    try:
        game = Connect4()
        Utils.log_message("Initial Board:", Globals.VerbosityLevels.BRIEF, __name__)
        game.print_board()
        current_player = initial_player
        winner = None

        while True:
            Utils.log_message(f"Current player {current_player}", Globals.VerbosityLevels.BRIEF, __name__)
            if current_player == Globals.Players.R:
                move = player1_alg.choose_move(game, current_player)
            else:
                move = player2_alg.choose_move(game, current_player)
            Utils.log_message(f"FINAL Move selected: {move}", Globals.VerbosityLevels.BRIEF, __name__)
            
            if move is not None:
                game.set_board(game.get_next_board(move, current_player))
                Utils.log_message("Current Board:", Globals.VerbosityLevels.BRIEF, __name__)
                game.print_board()
                
            game_state = game.evaluate_board()  # Evaluate the *current* state

            if game_state is not None or move is None:  # Game over or no move
                if game_state == 0:
                    winner = game_state
                    Utils.log_message("**** Draw! ****", Globals.VerbosityLevels.BRIEF, __name__)
                elif game_state == 1:
                    winner = game_state
                    Utils.log_message(f"**** {Globals.Players.Y} wins! ****", Globals.VerbosityLevels.BRIEF, __name__)
                elif game_state == -1:
                    winner = game_state
                    Utils.log_message(f"**** {Globals.Players.R} wins! ****", Globals.VerbosityLevels.BRIEF, __name__)
                elif move is None:
                    winner = 0
                    Utils.log_message(f"No valid moves for {current_player}.", Globals.VerbosityLevels.BRIEF, __name__)
                break

            current_player = game.get_opponent(current_player)
            
        Utils.log_message("Final Board:", Globals.VerbosityLevels.BRIEF, __name__)
        game.print_board()
        return winner
    except:
        Utils.log_message(f"Uncaught exception: {traceback.format_exc()}", Globals.VerbosityLevels.ERROR, __name__)
        sys.exit(1)

if __name__ == "__main__":
    """Main entry point of the script."""
    Utils.init()
    main()

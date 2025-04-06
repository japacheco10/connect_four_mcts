import traceback, sys, time
from common import Globals, Utils
from connect_4 import Connect4
from algorithms import AlgorithmFactory
from collections import defaultdict

def main():
    try:
        Utils.log_message("Init Start", Globals.VerbosityLevels.NONE, __name__)
        verbosity, num_games, algorithms = Utils.load_tournament_config()
        Utils.set_verbosity_level(verbosity)
        algorithm_names = [f"{name}({param})" if param else name for name, param in algorithms]
        num_algorithms = len(algorithms)
        # Timing data per algorithm
        total_game_time = [0.0 for _ in range(num_algorithms)]
        total_move_time = [0.0 for _ in range(num_algorithms)]
        total_moves = [0 for _ in range(num_algorithms)]
        # Initialize results dictionary
        results = defaultdict(dict)
        Utils.log_message("Init End", Globals.VerbosityLevels.NONE, __name__)
        
        Utils.log_message("Starting Tournament", Globals.VerbosityLevels.NONE, __name__)
        #   Tournament loop
        for i in range(num_algorithms):
            for j in range(num_algorithms):
                wins_i = 0
                wins_j = 0
                draws = 0

                for game in range(num_games):
                    print("-------------------------------------------------------------------------")
                    print(f"Game [{game+1}]")
                    print(f"[{algorithm_names[i]}] vs [{algorithm_names[j]}]")
                    print("-------------------------------------------------------------------------")
                    if game % 2 == 0: #ensure fairness by alternating which algorithm goes first
                        first, second = i, j
                    else:
                        first, second = j, i

                    #   Create algorithm instances for each game
                    alg1 = AlgorithmFactory.create_algorithm(algorithms[first][0], simulations=algorithms[first][1])
                    alg2 = AlgorithmFactory.create_algorithm(algorithms[second][0], simulations=algorithms[second][1])

                    winner, game_duration, move_times = play_game(alg1, alg2, Globals.Players.R, first, second)

                    # Track time
                    total_game_time[first] += game_duration
                    total_game_time[second] += game_duration
                    total_moves[first] += move_times[first]
                    total_moves[second] += move_times[second]
                    total_move_time[first] += move_times[f"{first}_time"]
                    total_move_time[second] += move_times[f"{second}_time"]

                    if winner == 1:
                        # Player 1 (alg1) wins
                        if first == i:
                            wins_i += 1
                        else:
                            wins_j += 1
                    elif winner == -1:
                        # Player 2 (alg2) wins
                        if second == i:
                            wins_i += 1
                        else:
                            wins_j += 1
                    else:
                        draws += 1

                total = wins_i + wins_j + draws
                win_rate = (wins_i / total * 100) if total > 0 else 0.0
                results[algorithm_names[i]][algorithm_names[j]] = f"{win_rate:.2f}%"

        # Print header
        print("-" * (12 + 12 * num_algorithms))
        print(f"{'':<12}|" + "".join(f"{name:<12}|" for name in algorithm_names))
        print("-" * (12 + 12 * num_algorithms))

        # Print rows
        for row_name in algorithm_names:
            row = f"{row_name:<12}|"
            for col_name in algorithm_names:
                result = results[row_name].get(col_name, "N/A")
                row += f"{result:<12}|"
            print(row)

        print("-" * (12 + 12 * num_algorithms))
        print("-------------------------------------------------------------------------")
        print("\nAverage Timing Stats per Algorithm:")
        print("-" * 60)
        print(f"{'Algorithm':<20} {'Avg Move Time (s)':<20} {'Avg Game Time (s)':<20}")
        print("-" * 60)
        for idx, name in enumerate(algorithm_names):
            avg_move_time = total_move_time[idx] / total_moves[idx] if total_moves[idx] else 0
            avg_game_time = total_game_time[idx] / (num_games * num_algorithms)  # Appears in num_algorithms matches
            print(f"{name:<20} {avg_move_time:<20.4f} {avg_game_time:<20.2f}")
        Utils.log_message("Ending Tournament", Globals.VerbosityLevels.ERROR, __name__)
    except ValueError as e:
        Utils.log_message(f"Error: {e}", Globals.VerbosityLevels.ERROR, __name__)
        sys.exit(1)
    except:
        Utils.log_message(f"Uncaught exception: {traceback.format_exc()}", Globals.VerbosityLevels.ERROR, __name__)
        sys.exit(1)

def play_game(player1_alg, player2_alg, initial_player, alg1_index, alg2_index):
    """
    Simulates a full Connect Four game between two algorithms.
    
    Args:
        player_r_alg: Algorithm instance for Red (Player 1)
        player_y_alg: Algorithm instance for Yellow (Player 2)
        initial_player: 'R' or 'Y', who starts the game
    Returns:
        1 if Yellow wins, -1 if Red wins, 0 if draw
    """
    try:
        game_start = time.time()
        move_counts = {alg1_index: 0, alg2_index: 0}
        move_times = {f"{alg1_index}_time": 0.0, f"{alg2_index}_time": 0.0}
        game = Connect4()
        Utils.log_message("Initial Board:", Globals.VerbosityLevels.BRIEF, __name__)
        game.print_board()
        current_player = initial_player
        winner = None

        while True:
            Utils.log_message(f"Current player {current_player}", Globals.VerbosityLevels.BRIEF, __name__)
            move_start = time.time()
            if current_player == Globals.Players.R:
                move = player1_alg.choose_move(game, current_player)
                duration = time.time() - move_start
                move_times[f"{alg1_index}_time"] += duration
                move_counts[alg1_index] += 1
            else:
                move = player2_alg.choose_move(game, current_player)
                duration = time.time() - move_start
                move_times[f"{alg2_index}_time"] += duration
                move_counts[alg2_index] += 1
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
        game_duration = time.time() - game_start
        move_times.update(move_counts)
        return winner, game_duration, move_times
    except:
        Utils.log_message(f"Uncaught exception: {traceback.format_exc()}", Globals.VerbosityLevels.ERROR, __name__)
        sys.exit(1)

if __name__ == "__main__":
    """Main entry point of the script."""
    Utils.init()
    main()

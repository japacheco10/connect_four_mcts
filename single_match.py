import traceback, sys, time
from common import Globals, Utils
from connect_4 import Connect4
from algorithms import AlgorithmFactory
from collections import defaultdict

def main():
    try:
        Utils.log_message("Init Start", Globals.VerbosityLevels.NONE, __name__)
        verbosity, num_games, algorithms = Utils.load_single_match_config()
        Utils.set_verbosity_level(verbosity)
        algorithm_names = [f"{name}({param})" if param else name for name, param in algorithms]
        num_algorithms = len(algorithms)

        # Timing data per algorithm
        total_game_time = [0.0 for _ in range(num_algorithms)]
        total_move_time = [0.0 for _ in range(num_algorithms)]
        total_moves = [0 for _ in range(num_algorithms)]
        games_played = [0 for _ in range(num_algorithms)]

        # Initialize results dictionaries
        win_counts = defaultdict(lambda: defaultdict(int))  # wins[row_alg][col_alg]
        draw_counts = defaultdict(lambda: defaultdict(int))  # draws[alg1][alg2]

        Utils.log_message("Init End", Globals.VerbosityLevels.NONE, __name__)
        Utils.log_message("Starting Single Match", Globals.VerbosityLevels.NONE, __name__)

        # Tournament loop
        for i in range(num_algorithms):
            for j in range(num_algorithms):
                if i == j:  # Skip self-matches for win tracking
                    continue  # Important!

                for game_index in range(num_games):
                    print("-------------------------------------------------------------------------")
                    print(f"Game [{game_index + 1}]")
                    print(f"[{algorithm_names[i]}] vs [{algorithm_names[j]}]")
                    print("-------------------------------------------------------------------------")

                    # Alternate who starts
                    first_index, second_index = (i, j) if game_index % 2 == 0 else (j, i)

                    # Create algorithm instances for each game
                    alg1 = AlgorithmFactory.create_algorithm(
                        algorithms[first_index][0], simulations=algorithms[first_index][1]
                    )
                    alg2 = AlgorithmFactory.create_algorithm(
                        algorithms[second_index][0], simulations=algorithms[second_index][1]
                    )

                    # Determine initial player for the game (consistent for 'first')
                    initial_player = Globals.Players.R if first_index == i else Globals.Players.R

                    winner, game_duration, move_times = play_game(
                        alg1, alg2, initial_player, first_index, second_index
                    )

                    # Track time
                    total_game_time[first_index] += game_duration
                    total_game_time[second_index] += game_duration
                    total_moves[first_index] += move_times.get(first_index, 0)
                    total_moves[second_index] += move_times.get(second_index, 0)
                    total_move_time[first_index] += move_times.get(f"{first_index}_time", 0.0)
                    total_move_time[second_index] += move_times.get(f"{second_index}_time", 0.0)
                    games_played[first_index] += 1
                    games_played[second_index] += 1

                    # Track win counts and draws (for row vs. column)
                    if winner == 1:  # Player 1 (alg1, which is algorithms[first_index]) won
                        win_counts[algorithm_names[i]][algorithm_names[j]] += 1
                    elif winner == -1:  # Player 2 (alg2, which is algorithms[second_index]) won
                        win_counts[algorithm_names[j]][algorithm_names[i]] += 1
                    else:
                        draw_counts[algorithm_names[i]][algorithm_names[j]] += 1
                        draw_counts[algorithm_names[j]][algorithm_names[i]] += 1

        # Compute Win Rate Matrix
        print("\nWin Rate Matrix (%):")
        print("-" * (14 + 14 * num_algorithms))
        print(f"{'':<14}|" + "".join(f"{name:<14}|" for name in algorithm_names))
        print("-" * (14 + 14 * num_algorithms))
        for i in range(num_algorithms):
            row = f"{algorithm_names[i]:<14}|"
            for j in range(num_algorithms):
                wins = win_counts[algorithm_names[i]].get(algorithm_names[j], 0)
                losses = win_counts[algorithm_names[j]].get(algorithm_names[i], 0)
                total_played = wins + losses  # Corrected: Do not include draws!
                total_games_per_matchup = num_games if i != j else num_games * 2 # Account for self-play
                
                win_rate = (wins / total_played * 100) if total_played > 0 else 50.00 if i == j else 0.00
                row += f"{win_rate:.2f}%{'':<1}|"
            print(row)
        print("-" * (14 + 14 * num_algorithms))

        # Print Raw Wins Matrix
        print("\nRaw Wins Matrix (#):")
        print("-" * (14 + 14 * num_algorithms))
        print(f"{'':<14}|" + "".join(f"{name:<14}|" for name in algorithm_names))
        print("-" * (14 + 14 * num_algorithms))
        for i in range(num_algorithms):
            row = f"{algorithm_names[i]:<14}|"
            for j in range(num_algorithms):
                wins = win_counts[algorithm_names[i]].get(algorithm_names[j], 0)
                row += f"{str(wins):<14}|"
            print(row)
        print("-" * (14 + 14 * num_algorithms))

        # Print Raw Draws Matrix
        print("\nRaw Draws Matrix (#):")
        print("-" * (14 + 14 * num_algorithms))
        print(f"{'':<14}|" + "".join(f"{name:<14}|" for name in algorithm_names))
        print("-" * (14 + 14 * num_algorithms))
        for i in range(num_algorithms):
            row = f"{algorithm_names[i]:<14}|"
            for j in range(num_algorithms):
                draws = draw_counts[algorithm_names[i]].get(algorithm_names[j], 0)
                row += f"{str(draws):<14}|"
            print(row)
        print("-" * (14 + 14 * num_algorithms))

        print("\nAverage Timing Stats per Algorithm:")
        print("-" * 80)
        print(f"{'Algorithm':<20} {'Games Played':<15} {'Avg Move Time (s)':<20} {'Avg Game Time (s)':<20}")
        print("-" * 80)
        for idx, name in enumerate(algorithm_names):
            avg_move_time = total_move_time[idx] / total_moves[idx] if total_moves[idx] else 0
            avg_game_time = 0.0 if games_played[idx] == 0 else total_game_time[idx] / games_played[idx]
            print(f"{name:<20} {games_played[idx]:<15} {avg_move_time:<20.4f} {avg_game_time:<20.2f}")
        Utils.log_message("Ending Single Match", Globals.VerbosityLevels.NONE, __name__)
    except ValueError as e:
        Utils.log_message(f"Error: {e}", Globals.VerbosityLevels.ERROR, __name__)
        sys.exit(1)
    except:
        Utils.log_message(f"Uncaught exception: {traceback.format_exc()}", Globals.VerbosityLevels.ERROR, __name__)
        sys.exit(1)

import traceback
import sys
import time
from common import Globals, Utils
from connect_4 import Connect4
from algorithms import AlgorithmFactory
from collections import defaultdict


def play_game(player1_alg, player2_alg, initial_player, alg1_index, alg2_index):
    """
    Simulates a full Connect Four game between two algorithms.

    Args:
        player1_alg: Algorithm instance for Player 1 (starts as Red)
        player2_alg: Algorithm instance for Player 2 (starts as Yellow if Player 1 is Red)
        initial_player: Globals.Players.R or Globals.Players.Y, who starts the game
        alg1_index: Index of the first algorithm in the `algorithms` list for this game
        alg2_index: Index of the second algorithm in the `algorithms` list for this game

    Returns:
        winner: 1 if Player 1 wins, -1 if Player 2 wins, 0 if draw
        game_duration: Time taken for the game in seconds
        move_times: Dictionary containing move counts and total move times for each algorithm
                      e.g., {alg1_index: num_moves_alg1, alg2_index: num_moves_alg2,
                            f"{alg1_index}_time": total_time_alg1, f"{alg2_index}_time": total_time_alg2}
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
        last_move_player = None  # Initialize last_move_player

        while True:
            Utils.log_message(f"Current player {current_player}", Globals.VerbosityLevels.BRIEF, __name__)
            move_start = time.time()
            if current_player == Globals.Players.R:
                move = player1_alg.choose_move(game, current_player)
                duration = time.time() - move_start
                move_times[f"{alg1_index}_time"] += duration
                move_counts[alg1_index] += 1
                current_alg_name = f"Alg{alg1_index}"
            else:
                move = player2_alg.choose_move(game, current_player)
                duration = time.time() - move_start
                move_times[f"{alg2_index}_time"] += duration
                move_counts[alg2_index] += 1
                current_alg_name = f"Alg{alg2_index}"

            Utils.log_message(f"FINAL Move selected: {move} by {current_alg_name}", Globals.VerbosityLevels.BRIEF, __name__)

            if move is not None:
                game.set_board(game.get_next_board(move, current_player))
                Utils.log_message("Current Board:", Globals.VerbosityLevels.BRIEF, __name__)
                game.print_board()
                last_move_player = current_player  # Track the player who made the move

            Utils.log_message(f"Before evaluate_board", Globals.VerbosityLevels.VERBOSE, __name__)
            game_state = game.evaluate_board(False)  # Evaluate the *current* state
            Utils.log_message(f"After evaluate_board: game_state = {game_state}", Globals.VerbosityLevels.VERBOSE, __name__)

            if game_state is not None or move is None:  # Game over or no move
                if game_state == 0:
                    winner = 0
                    Utils.log_message("**** Draw! ****", Globals.VerbosityLevels.BRIEF, __name__)
                elif game_state == 1:  # Yellow wins
                    winner = 1 if last_move_player == Globals.Players.Y else -1
                    Utils.log_message(f"**** {Globals.Players.Y} wins! (Winner: {winner}) ****", Globals.VerbosityLevels.BRIEF, __name__)
                elif game_state == -1:  # Red wins
                    winner = 1 if last_move_player == Globals.Players.R else -1
                    Utils.log_message(f"**** {Globals.Players.R} wins! (Winner: {winner}) ****", Globals.VerbosityLevels.BRIEF, __name__)
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
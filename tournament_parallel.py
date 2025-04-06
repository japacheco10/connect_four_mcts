import sys
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from collections import defaultdict
from common import Utils, Globals
from algorithms import AlgorithmFactory
from connect_4 import Connect4

try:
    from tqdm import tqdm  # Optional for progress bar
except ImportError:
    tqdm = None

import time

def play_game(player1_alg, player2_alg, initial_player, alg1_index, alg2_index):
    from common import Globals

    game = Connect4()
    current_player = initial_player
    winner = None
    last_move_player = None  # Initialize last_move_player

    move_times = {alg1_index: 0.0, alg2_index: 0.0}
    move_counts = {alg1_index: 0, alg2_index: 0}

    start_time = time.time()

    while True:
        move_start = time.time()

        if current_player == Globals.Players.R:
            move = player1_alg.choose_move(game, current_player)
            duration = time.time() - move_start
            move_times[alg1_index] += duration
            move_counts[alg1_index] += 1
            last_move_player = Globals.Players.R  # Track last move
        else:
            move = player2_alg.choose_move(game, current_player)
            duration = time.time() - move_start
            move_times[alg2_index] += duration
            move_counts[alg2_index] += 1
            last_move_player = Globals.Players.Y  # Track last move

        if move is not None:
            game.set_board(game.get_next_board(move, current_player))

        game_state = game.evaluate_board(False)

        if game_state is not None or move is None:
            if game_state == 0:
                winner = 0  # Draw
            elif game_state == 1:  # Yellow wins
                winner = 1 if last_move_player == Globals.Players.Y else -1
            elif game_state == -1:  # Red wins
                winner = 1 if last_move_player == Globals.Players.R else -1
            elif move is None:
                winner = 0  # No valid moves
            break

        current_player = game.get_opponent(current_player)

    total_time = time.time() - start_time

    return winner, total_time, move_times, move_counts

def run_single_match(args):
    i, j, game_index, algorithms, parallel = args

    first_index, second_index = (i, j) if game_index % 2 == 0 else (j, i)

    alg1 = AlgorithmFactory.create_algorithm(
        algorithms[first_index][0], simulations=algorithms[first_index][1], parallel=parallel
    )
    alg2 = AlgorithmFactory.create_algorithm(
        algorithms[second_index][0], simulations=algorithms[second_index][1], parallel=parallel
    )

    initial_player = Globals.Players.R  # Consistent initial player for the 'first' algorithm

    winner, game_duration, move_times, move_counts = play_game(
        alg1, alg2, initial_player, first_index, second_index
    )

    return {
        "row": i,
        "col": j,
        "winner": winner,
        "first": first_index,
        "second": second_index,
        "game_time": game_duration,
        "move_times": move_times,
        "move_counts": move_counts,
    }

def main():
    try:
        max_proc, num_games, parallel, algorithms = Utils.load_tournament_config()
        Utils.set_verbosity_level(Globals.VerbosityLevels.NONE)
        algorithm_names = [f"{name}({param})" if param else name for name, param in algorithms]
        num_algorithms = len(algorithms)
        total_game_time = [0.0] * num_algorithms
        total_move_time = [0.0] * num_algorithms
        total_moves = [0] * num_algorithms
        games_played = [0] * num_algorithms

        win_counts = defaultdict(lambda: defaultdict(int))
        draw_counts = defaultdict(lambda: defaultdict(int))
        results = defaultdict(dict)

        # Prepare all jobs
        jobs = []
        for i in range(num_algorithms):
            for j in range(num_algorithms):
                for game_index in range(num_games):
                    jobs.append((i, j, game_index, algorithms, parallel))

        game_results = []
        print(f"\nRunning {len(jobs)} games in parallel...\n")

        with ProcessPoolExecutor(max_workers=max_proc) as executor:
            futures = [executor.submit(run_single_match, job) for job in jobs]

            progress_iter = as_completed(futures)
            if tqdm:
                progress_iter = tqdm(progress_iter, total=len(futures))

            for future in progress_iter:
                result = future.result()
                game_results.append(result)

                first = result["first"]
                second = result["second"]

                total_game_time[first] += result["game_time"]
                total_game_time[second] += result["game_time"]
                games_played[first] += 1
                games_played[second] += 1
                total_move_time[first] += result["move_times"].get(first, 0)
                total_move_time[second] += result["move_times"].get(second, 0)
                total_moves[first] += result["move_counts"].get(first, 0)
                total_moves[second] += result["move_counts"].get(second, 0)

        # Aggregate results and track wins for row vs. column
        for result in game_results:
            i = result["row"]
            j = result["col"]
            winner = result["winner"]
            first = result["first"]
            second = result["second"]

            row_name = algorithm_names[i]
            col_name = algorithm_names[j]

            if i != j:  # Add this condition to skip self-matches
                if winner == 1:  # Player 1 (algorithms[first]) won
                    if first == i:
                        win_counts[row_name][col_name] += 1
                    else:
                        win_counts[col_name][row_name] += 1
                elif winner == -1:  # Player 2 (algorithms[second]) won
                    if second == i:
                        win_counts[row_name][col_name] += 1
                    else:
                        win_counts[col_name][row_name] += 1
                else:
                    draw_counts[row_name][col_name] += 1
                    draw_counts[col_name][row_name] += 1

        # Compute percentages (Win Rate)
        print("\nWin Rate Matrix (%):")
        print("-" * (14 + 14 * num_algorithms))
        print(f"{'':<14}|" + "".join(f"{name:<14}|" for name in algorithm_names))
        print("-" * (14 + 14 * num_algorithms))
        for row_name in algorithm_names:
            row = f"{row_name:<14}|"
            for col_name in algorithm_names:
                wins = win_counts[row_name].get(col_name, 0)
                losses = win_counts[col_name].get(row_name, 0)  # Wins for the opponent
                total_played = wins + losses  # Corrected: Do not include draws!
                total_games_per_matchup = num_games if i != j else num_games * 2  # Account for self-play

                win_rate = (wins / total_played * 100) if total_played > 0 else 50.00 if i == j else 0.00
                row += f"{win_rate:.2f}%{'':<1}|"
            print(row)
        print("-" * (14 + 14 * num_algorithms))

        # Print Raw Win Count Matrix
        print("\nGames Won Matrix (#):")
        print("-" * (14 + 14 * num_algorithms))
        print(f"{'':<14}|" + "".join(f"{name:<14}|" for name in algorithm_names))
        print("-" * (14 + 14 * num_algorithms))
        for row_name in algorithm_names:
            row = f"{row_name:<14}|"
            for col_name in algorithm_names:
                wins = win_counts[row_name].get(col_name, 0)
                row += f"{str(wins):<14}|"
            print(row)
        print("-" * (14 + 14 * num_algorithms))

        # Print Raw Draw Count Matrix
        print("\nGames Drawn Matrix (#):")
        print("-" * (14 + 14 * num_algorithms))
        print(f"{'':<14}|" + "".join(f"{name:<14}|" for name in algorithm_names))
        print("-" * (14 + 14 * num_algorithms))
        for row_name in algorithm_names:
            row = f"{row_name:<14}|"
            for col_name in algorithm_names:
                draws = draw_counts[row_name].get(col_name, 0)
                row += f"{str(draws):<14}|"
            print(row)
        print("-" * (14 + 14 * num_algorithms))

        print("\nAverage Timing Stats per Algorithm:")
        print("-" * 80)
        print(f"{'Algorithm':<20} {'Games Played':<15} {'Avg Move Time (s)':<20} {'Avg Game Time (s)':<20}")
        print("-" * 80)
        for idx, name in enumerate(algorithm_names):
            avg_move = total_move_time[idx] / total_moves[idx] if total_moves[idx] else 0
            avg_game = 0.0 if games_played[idx] == 0 else total_game_time[idx] / games_played[idx]
            print(f"{name:<20} {games_played[idx]:<15} {avg_move:<20.4f} {avg_game:<20.2f}")

    except Exception:
        Utils.log_message(f"Uncaught exception: {traceback.format_exc()}", Globals.VerbosityLevels.ERROR, __name__)
        sys.exit(1)

if __name__ == "__main__":
    Utils.init()
    main()
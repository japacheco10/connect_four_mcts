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

    move_times = {alg1_index: 0.0, alg2_index: 0.0}
    move_counts = {alg1_index: 0, alg2_index: 0}

    start_time = time.time()

    while True:
        move_start = time.time()

        if current_player == Globals.Players.R:
            move = player1_alg.choose_move(game, current_player)
            move_times[alg1_index] += time.time() - move_start
            move_counts[alg1_index] += 1
        else:
            move = player2_alg.choose_move(game, current_player)
            move_times[alg2_index] += time.time() - move_start
            move_counts[alg2_index] += 1

        if move is not None:
            game.set_board(game.get_next_board(move, current_player))

        game_state = game.evaluate_board(False)

        if game_state is not None or move is None:
            winner = game_state
            break

        current_player = game.get_opponent(current_player)

    total_time = time.time() - start_time

    return winner, total_time, move_times, move_counts

def run_single_match(args):
    i, j, game_index, algorithms = args

    first, second = (i, j) if game_index % 2 == 0 else (j, i)

    alg1 = AlgorithmFactory.create_algorithm(algorithms[first][0], simulations=algorithms[first][1])
    alg2 = AlgorithmFactory.create_algorithm(algorithms[second][0], simulations=algorithms[second][1])

    winner, game_duration, move_times, move_counts = play_game(alg1, alg2, Globals.Players.R, first, second)

    return {
        "row": i,
        "col": j,
        "winner": winner,
        "first": first,
        "second": second,
        "game_time": game_duration,
        "move_times": move_times,
        "move_counts": move_counts
    }



def main():
    try:
        verbosity, num_games, algorithms = Utils.load_tournament_config()
        Utils.set_verbosity_level(verbosity)
        algorithm_names = [f"{name}({param})" if param else name for name, param in algorithms]
        num_algorithms = len(algorithms)
        total_game_time = [0.0] * num_algorithms
        total_move_time = [0.0] * num_algorithms
        total_moves = [0] * num_algorithms
        games_played = [0] * num_algorithms

        results = defaultdict(dict)
        raw_wins = defaultdict(lambda: defaultdict(int))

        # Prepare all jobs
        jobs = []
        for i in range(num_algorithms):
            for j in range(num_algorithms):
                for game_index in range(num_games):
                    jobs.append((i, j, game_index, algorithms))

        game_results = []
        print(f"\nRunning {len(jobs)} games in parallel...\n")

        with ProcessPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(run_single_match, job) for job in jobs]

            progress_iter = as_completed(futures)
            if tqdm:
                progress_iter = tqdm(progress_iter, total=len(futures))

            for future in progress_iter:
                result = future.result()
                game_results.append(result)

                for idx in [result["first"], result["second"]]:
                    total_game_time[idx] += result["game_time"]
                    games_played[idx] += 1
                    total_move_time[idx] += result["move_times"].get(idx, 0)
                    total_moves[idx] += result["move_counts"].get(idx, 0)


        # Aggregate results
        for result in game_results:
            i = result["row"]
            j = result["col"]
            winner = result["winner"]
            first = result["first"]
            second = result["second"]

            if winner == 1:
                winner_idx = first
            elif winner == -1:
                winner_idx = second
            else:
                winner_idx = None  # Draw

            if winner_idx == i:
                raw_wins[algorithm_names[i]][algorithm_names[j]] += 1

        # Compute percentages
        for i in range(num_algorithms):
            for j in range(num_algorithms):
                wins = raw_wins[algorithm_names[i]][algorithm_names[j]]
                win_rate = (wins / num_games) * 100
                results[algorithm_names[i]][algorithm_names[j]] = f"{win_rate:.2f}%"

        # Print Win Rate Matrix
        print("\nWin Rate Matrix (%):")
        print("-" * (14 + 14 * num_algorithms))
        print(f"{'':<14}|" + "".join(f"{name:<14}|" for name in algorithm_names))
        print("-" * (14 + 14 * num_algorithms))
        for row_name in algorithm_names:
            row = f"{row_name:<14}|"
            for col_name in algorithm_names:
                result = results[row_name].get(col_name, "N/A")
                row += f"{result:<14}|"
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
                result = raw_wins[row_name].get(col_name, "0")
                row += f"{str(result):<14}|"
            print(row)
        print("-" * (14+ 14 * num_algorithms))

        print("\nAverage Timing Stats per Algorithm:")
        print("-" * 80)
        print(f"{'Algorithm':<20} {'Games Played':<15} {'Avg Move Time (s)':<20} {'Avg Game Time (s)':<20}")
        print("-" * 80)
        for idx, name in enumerate(algorithm_names):
            avg_move = total_move_time[idx] / total_moves[idx] if total_moves[idx] else 0
            avg_game = total_game_time[idx] / games_played[idx] if games_played[idx] else 0
            print(f"{name:<20} {games_played[idx]:<15} {avg_move:<20.4f} {avg_game:<20.2f}")


    except Exception:
        Utils.log_message(f"Uncaught exception: {traceback.format_exc()}", Globals.VerbosityLevels.ERROR, __name__)
        sys.exit(1)


if __name__ == "__main__":
    Utils.init()
    main()

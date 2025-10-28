"""
Logger Module
Functions for logging and statistics management.
"""

from pathlib import Path
from datetime import datetime


def load_stats(stats_file):
    """
    Load statistics from file.

    Args:
        stats_file: Path to statistics file

    Returns:
        Dictionary with statistics
    """
    default_stats = {
        'games_played': 0,
        'wins': 0,
        'losses': 0,
        'total_score': 0
    }

    if not stats_file.exists():
        return default_stats

    try:
        with open(stats_file, 'r', encoding='utf-8') as f:
            stats = {}
            for line in f:
                if ':' in line:
                    key, value = line.strip().split(':', 1)
                    stats[key.strip()] = int(value.strip())
            return stats if stats else default_stats
    except Exception as e:
        print(f"Warning: Could not load statistics: {e}")
        return default_stats


def save_stats(stats_file, stats):
    """
    Save statistics to file.

    Args:
        stats_file: Path to statistics file
        stats: Statistics dictionary
    """
    try:
        stats_file.parent.mkdir(parents=True, exist_ok=True)
        with open(stats_file, 'w', encoding='utf-8') as f:
            f.write(f"games_played: {stats['games_played']}\n")
            f.write(f"wins: {stats['wins']}\n")
            f.write(f"losses: {stats['losses']}\n")
            f.write(f"total_score: {stats['total_score']}\n")
    except Exception as e:
        print(f"Warning: Could not save statistics: {e}")


def save_game_log(game_number, category, state, score, stats):
    """
    Save detailed game log to file.

    Args:
        game_number: Game number
        category: Category name
        state: Game state dictionary
        score: Final score
        stats: Current statistics
    """
    game_dir = Path(f"game_log/game{game_number}")
    game_dir.mkdir(parents=True, exist_ok=True)

    log_file = game_dir / "log.txt"

    try:
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"Game {game_number} Log\n")
            f.write("=" * 60 + "\n")
            f.write(f"Category: {category}\n")
            f.write(f"Word: {state['word']}\n")
            f.write(f"Word Length: {len(state['word'])}\n\n")

            f.write("Guesses (in order):\n")
            for i, (guess, correct) in enumerate(state.get('guess_log', []), 1):
                status = "Correct" if correct else "Wrong"
                f.write(f"{i}. {guess} -> {status}\n")

            wrong_list = ', '.join(state.get('wrong_guesses', [])) or 'None'
            f.write(f"\nWrong Guesses List: {wrong_list}\n")
            f.write(f"Wrong Guesses Count: {state.get('wrong_count', 0)}\n")
            f.write(f"Remaining Attempts: {state.get('max_wrong', 6) - state.get('wrong_count', 0)}\n")
            f.write(f"Result: {'Win' if state.get('game_won', False) else 'Loss'}\n")
            f.write(f"Points Earned: {score}\n")
            f.write(f"Total Score: {stats['total_score']}\n\n")

            f.write(f"Games Played: {stats['games_played']}\n")
            f.write(f"Wins: {stats['wins']}\n")
            f.write(f"Losses: {stats['losses']}\n")

            if stats['games_played'] > 0:
                win_rate = (stats['wins'] / stats['games_played']) * 100
                f.write(f"Win Rate: {win_rate:.2f}%\n")

            f.write(f"\nDate & Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n")

        print(f"Game log saved to: {log_file}")
    except Exception as e:
        print(f"Warning: Could not save log: {e}")


def display_final_stats(stats):
    """
    Display final statistics.

    Args:
        stats: Statistics dictionary
    """
    print("\n" + "=" * 60)
    print("FINAL STATISTICS".center(60))
    print("=" * 60)
    print(f"Games played: {stats['games_played']}")
    print(f"Wins: {stats['wins']}")
    print(f"Losses: {stats['losses']}")

    if stats['games_played'] > 0:
        win_rate = (stats['wins'] / stats['games_played']) * 100
        avg_score = stats['total_score'] / stats['games_played']
        print(f"Win rate: {win_rate:.2f}%")
        print(f"Average score: {avg_score:.2f}")

    print(f"Total score: {stats['total_score']}")
    print("=" * 60)

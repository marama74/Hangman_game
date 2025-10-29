"""
Main Entry Point for Hangman Game
Handles:
- Welcome screen
- Category selection(select at least one )
- Gameplay loop
- Logging results
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent))

from game.engine import play_game, get_next_game_number
from game.wordlist import get_categories, display_categories, get_category_choice
from game.logger import load_stats, save_stats, display_final_stats
from ui.display import display_welcome

def main():
    """Main Hangman game flow."""
    base_dir = Path(__file__).resolve().parent
    words_dir = base_dir / "words"
    stats_file = base_dir / "game_stats.txt"

    stats = load_stats(stats_file)

    display_welcome()

    # Load categories
    categories = get_categories(words_dir)
    if not categories:
        print("No categories found. Add files to 'words/categories/'")
        return

    display_categories(categories)
    category_name = get_category_choice(categories)

    player_name = input("\nEnter your name: ").strip().capitalize() or "Player"

    game_number = get_next_game_number()

    
    game_result = play_game(words_dir, category_name, stats, game_number)

    
    save_stats(stats_file, stats)

    display_final_stats(stats)

    print("\nThanks for playing Hangman, {}!".format(player_name))


if __name__ == "__main__":
    main()
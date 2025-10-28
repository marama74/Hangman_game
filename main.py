"""
Main Entry Point for Hangman Game
Handles:
- Welcome screen
- Category selection
- Gameplay loop
- Logging results
"""

from pathlib import Path
import sys

# Add current directory to path for relative imports
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

    # Load player statistics
    stats = load_stats(stats_file)

    # Display welcome banner
    display_welcome()

    # Load categories
    categories = get_categories(words_dir)
    if not categories:
        print("No categories found. Add files to 'words/categories/'")
        return

    # Display categories and get selection
    display_categories(categories)
    category_name = get_category_choice(categories)

    # Ask for player name
    player_name = input("\nEnter your name: ").strip().capitalize() or "Player"

    # Get next game number
    game_number = get_next_game_number()

    # Start the game
    game_result = play_game(words_dir, category_name, stats, game_number)

    # Save updated stats
    save_stats(stats_file, stats)

    # Display final stats
    display_final_stats(stats)

    print("\nThanks for playing Hangman_game, {}!".format(player_name))


if __name__ == "__main__":
    main()

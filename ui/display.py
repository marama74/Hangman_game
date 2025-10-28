"""
Display Module
Functions for formatting and displaying game information.
"""

import os


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_welcome():
    """Display welcome banner."""
    print("=" * 60)
    print("HANGMAN GAME".center(60))
    print("=" * 60)
    print("\nGuess the word letter by letter!")
    print("You have 6 wrong guesses before losing.")
    print("\nThree ways to guess:")
    print("  1. Single letter (e.g., 'a')")
    print("  2. Multiple letters (e.g., 'thon')")
    print("  3. Complete word (e.g., 'python')")
    print("=" * 60)


def display_category_menu(categories):
    """
    Display category selection menu.
    
    Args:
        categories: List of category names
    """
    print("\n" + "=" * 60)
    print("CHOOSE A CATEGORY".center(60))
    print("=" * 60)
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")
    print(f"  {len(categories) + 1}. All categories (random)")
    print("\n  Type 'quit' to exit")
    print("=" * 60)


def get_word_progress(word, correct_letters):
    """
    Get word progress with revealed letters.
    
    Args:
        word: The secret word
        correct_letters: Set of correctly guessed letters
        
    Returns:
        Formatted string with progress
    """
    progress = []
    for letter in word:
        if letter in correct_letters:
            progress.append(letter.upper())
        else:
            progress.append('_')
    return ' '.join(progress)


def display_game_state(state):
    """
    Display current game state.
    
    Args:
        state: Game state dictionary
    """
    print("\n" + "=" * 60)
    
    # Word progress
    progress = get_word_progress(state['word'], state['correct_letters'])
    print(f"Word: {progress}")
    
    # Guessed letters
    if state['guessed_letters']:
        sorted_guesses = sorted(list(state['guessed_letters']))
        print(f"Guessed: {', '.join(sorted_guesses)}")
    else:
        print("Guessed: None")
    
    # Remaining attempts
    remaining = state['max_wrong'] - state['wrong_count']
    print(f"Remaining attempts: {remaining}/{state['max_wrong']}")
    
    print("=" * 60)


def display_result(state, score, stats):
    """
    Display game result and statistics.
    
    Args:
        state: Final game state
        score: Final score
        stats: Current statistics
    """
    print("\n" + "=" * 60)
    
    if state['game_won']:
        print("YOU WIN!".center(60))
        print(f"\nThe word was: {state['word'].upper()}")
        print(f"Points earned: {score}")
    else:
        print("YOU LOSE!".center(60))
        print(f"\nThe word was: {state['word'].upper()}")
        print(f"Points earned: 0")
    
    print("=" * 60)
    
    # Display statistics
    print("\nCurrent Statistics:")
    print(f"  Total score: {stats['total_score']}")
    print(f"  Games: {stats['games_played']} | Wins: {stats['wins']} | Losses: {stats['losses']}", end="")
    
    if stats['games_played'] > 0:
        win_rate = (stats['wins'] / stats['games_played']) * 100
        avg_score = stats['total_score'] / stats['games_played']
        print(f" | Win rate: {win_rate:.2f}% | Average score: {avg_score:.2f}")
    else:
        print()
    
    print("=" * 60)

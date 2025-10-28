"""
Game Engine Module
Core gameplay logic for Hangman using functions.
"""

from pathlib import Path
from datetime import datetime
from .logger import save_game_log
from .wordlist import get_random_word
from .ascii_art import get_hangman_art
from ui.display import display_game_state, display_result


def get_next_game_number():
    """
    Get the next game number for logging.

    Returns:
        Next game number as integer
    """
    game_log_dir = Path("game_log")
    game_log_dir.mkdir(exist_ok=True)
    existing_games = [d for d in game_log_dir.iterdir() if d.is_dir() and d.name.startswith('game')]
    
    numbers = []
    for d in existing_games:
        try:
            num = int(d.name.replace('game', ''))
            numbers.append(num)
        except ValueError:
            continue
    return max(numbers) + 1 if numbers else 1


def initialize_game_state(word):
    """
    Initialize the game state dictionary.
    """
    return {
        'word': word.lower(),
        'guessed_letters': set(),
        'correct_letters': set(),
        'wrong_guesses': [],
        'wrong_count': 0,
        'max_wrong': 6,
        'game_won': False,
        'game_lost': False,
        'guess_log': []
    }


def process_guess(state, guess):
    """
    Process a user's guess and update the game state.
    """
    if not guess.isalpha():
        print("Invalid input. Use letters only.")
        return state
    
    guess = guess.lower()
    
    if len(guess) == 1:
        state = handle_single_letter(state, guess)
    elif len(guess) == len(state['word']):
        state = handle_full_word(state, guess)
    else:
        state = handle_multiple_letters(state, guess)
    
    return state


def handle_single_letter(state, letter):
    """Handle single letter guesses."""
    if letter in state['guessed_letters']:
        print(f"'{letter}' already guessed.")
        return state

    state['guessed_letters'].add(letter)

    if letter in state['word']:
        state['correct_letters'].add(letter)
        print(f"Correct! '{letter}' is in the word.")
        state['guess_log'].append((letter, True))
        if check_win(state):
            state['game_won'] = True
    else:
        state['wrong_guesses'].append(letter)
        state['wrong_count'] += 1
        print(f"Wrong! '{letter}' is not in the word.")
        state['guess_log'].append((letter, False))
        if state['wrong_count'] >= state['max_wrong']:
            state['game_lost'] = True

    return state


def handle_multiple_letters(state, letters):
    """Handle multiple letter guesses."""
    print(f"\nChecking letters: {letters.upper()}")
    new_correct = []
    new_wrong = []
    already_guessed = []

    for letter in letters:
        if letter in state['guessed_letters']:
            already_guessed.append(letter)
            continue

        state['guessed_letters'].add(letter)
        if letter in state['word']:
            state['correct_letters'].add(letter)
            new_correct.append(letter)
        else:
            state['wrong_guesses'].append(letter)
            state['wrong_count'] += 1
            new_wrong.append(letter)

    if already_guessed:
        print(f"Already guessed: {', '.join(already_guessed)}")
    if new_correct:
        print(f"Correct letters: {', '.join(new_correct)}")
    if new_wrong:
        print(f"Wrong letters: {', '.join(new_wrong)}")

    state['guess_log'].append((f"MULTI:{letters}", len(new_correct) > 0))

    if check_win(state):
        state['game_won'] = True
    elif state['wrong_count'] >= state['max_wrong']:
        state['game_lost'] = True

    return state


def handle_full_word(state, guess):
    """Handle complete word guesses."""
    print(f"\nGuessing full word: {guess.upper()}")
    if guess.lower() == state['word']:
        state['correct_letters'] = set(state['word'])
        state['guessed_letters'] = set(state['word'])
        state['game_won'] = True
        print("Correct! You guessed the word!")
        state['guess_log'].append((f"WORD:{guess}", True))
    else:
        state['wrong_guesses'].append(f"WORD:{guess}")
        state['wrong_count'] += 1
        print(f"Wrong! '{guess}' is not the word.")
        state['guess_log'].append((f"WORD:{guess}", False))
        if state['wrong_count'] >= state['max_wrong']:
            state['game_lost'] = True

    return state


def check_win(state):
    """Check if all letters have been guessed."""
    return set(state['word']) == state['correct_letters']


def calculate_score(state):
    """Calculate score based on correct guesses and wrong attempts."""
    if not state['game_won']:
        return 0
    base = len(state['word']) * 10
    penalty = state['wrong_count'] * 5
    return max(0, base - penalty)


def play_game(word_database, category, stats, game_number):
    """
    Main game loop.
    """
    # Get random word
    word, actual_category = get_random_word(word_database, category)

    # Initialize state
    state = initialize_game_state(word)
    print(f"\nNew word from '{actual_category}' category ({len(word)} letters)")

    # Game loop
    while not state['game_won'] and not state['game_lost']:
        display_game_state(state)
        print(get_hangman_art(state['wrong_count']))
        print("\nOptions: single letter / multiple letters / full word / 'quit'")
        user_input = input("\nYour guess: ").strip().lower()
        if user_input == 'quit':
            print("\nGame terminated.")
            state['game_lost'] = True
            break
        state = process_guess(state, user_input)

    # Calculate score and update stats
    score = calculate_score(state)
    stats['games_played'] += 1
    if state['game_won']:
        stats['wins'] += 1
        stats['total_score'] += score
    else:
        stats['losses'] += 1

    display_result(state, score, stats)
    save_game_log(game_number, actual_category, state, score, stats)

    return {
        'won': state['game_won'],
        'word': state['word'],
        'score': score,
        'stats': stats
    }

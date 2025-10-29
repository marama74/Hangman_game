"""
ASCII Art Module
Contains hangman drawings for each game state (0-6 wrong guesses).

This module provides:
- ASCII art for each wrong guess count
- Visual feedback of game progress
"""

def get_hangman_art(wrong_count):
    """
    Return ASCII art for hangman based on wrong guess count.
    
    Args:
        wrong_count (int): Number of wrong guesses (0-6)
        
    Returns:
        str: ASCII art representation of hangman
        
    States:
        0: Empty gallows
        1: Head
        2: Body
        3: Left arm
        4: Right arm
        5: Left leg
        6: Right leg (game over)
    """
    stages = [
        # NO wrong guess
        """
        +---+
        |   |
            |
            |
            |
            |
      =========
        """,
        # wrong_1
        """
        +---+
        |   |
        O   |
            |
            |
            |
      =========
        """,
        # wrong_2
        """
        +---+
        |   |
        O   |
        |   |
            |
            |
      =========
        """,
        # wrong_3
        """
        +---+
        |   |
        O   |
       /|   |
            |
            |
      =========
        """,
        # wrong_4 
        """
        +---+
        |   |
        O   |
       /|\\  |
            |
            |
      =========
        """,
        # wrong_5
        """
        +---+
        |   |
        O   |
       /|\\  |
       /    |
            |
      =========
        """,
        # wrong_6
        """
        +---+
        |   |
        O   |
       /|\\  |
       / \\  |
            |
      =========
        """
    ]
    
    
    if wrong_count < 0:
        wrong_count = 0
    elif wrong_count > 6:
        wrong_count = 6
    
    return stages[wrong_count]

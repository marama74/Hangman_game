"""
Wordlist Module
Handles loading words from category files and selecting random words.

This module provides:
- Loading words from text files
- Listing available categories
- Selecting random words from chosen categories
"""

from pathlib import Path
import random


def get_categories(words_dir):
    """
    Return a list of all available word categories.

    Args:
        words_dir (Path): Path to the 'words' directory

    Returns:
        dict: Mapping of category name to its file path
    """
    categories_dir = words_dir / "categories"
    if not categories_dir.exists():
        print("Error: 'categories' folder not found.")
        return {}

    category_files = list(categories_dir.glob("*.txt"))
    categories = {file.stem.lower(): file for file in category_files}

    return categories


def load_words_from_file(file_path):
    """
    Load all words from a given file.

    Args:
        file_path (Path): Path to category file

    Returns:
        list: List of cleaned words
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            words = [line.strip().lower() for line in f if line.strip()]
        return words
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return []


def get_random_word(words_dir, category_name):
    """
    Select a random word from a given category.

    Args:
        words_dir (Path): Path to the 'words' directory
        category_name (str): Name of the category or 'all'

    Returns:
        tuple: (selected_word, category_used)
    """
    categories = get_categories(words_dir)

    # If "all" or invalid category, combine all words
    if category_name.lower() not in categories and category_name.lower() != "all":
        print("Invalid category name. Using 'all' instead.")
        category_name = "all"

    all_words = []

    if category_name.lower() == "all":
        for file_path in categories.values():
            all_words.extend(load_words_from_file(file_path))
        chosen_category = "All Categories"
    else:
        file_path = categories[category_name.lower()]
        all_words = load_words_from_file(file_path)
        chosen_category = category_name.capitalize()

    if not all_words:
        print("Error: No words found in the selected category.")
        return None, chosen_category

    selected_word = random.choice(all_words)
    return selected_word, chosen_category


def display_categories(categories):
    """
    Display all available categories in a numbered format.

    Args:
        categories (dict): Category mapping
    """
    print("\nCHOOSE A CATEGORY")
    print("=" * 60)
    for i, name in enumerate(categories.keys(), 1):
        print(f"{i}. {name.capitalize()}")
    print(f"{len(categories) + 1}. All Categories (random)")
    print("=" * 60)


def get_category_choice(categories):
    """
    Ask user to select a category by name or number.

    Args:
        categories (dict): Category mapping

    Returns:
        str: Selected category name
    """
    while True:
        user_input = input("Choose a category (number or name): ").strip().lower()

        # If user entered number
        if user_input.isdigit():
            num = int(user_input)
            if 1 <= num <= len(categories):
                return list(categories.keys())[num - 1]
            elif num == len(categories) + 1:
                return "all"
            else:
                print("Invalid number. Try again.")
        else:
            # If user entered category name
            if user_input in categories or user_input == "all":
                return user_input
            print("Invalid input. Please try again.")

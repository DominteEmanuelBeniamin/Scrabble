import sys
import os
from typing import Set, Optional
from tile import TileSystem

def load_dictionary(dict_file: str) -> Optional[Set[str]]:
    """
    Load a dictionary file into a set of words.
    
    Args:
        dict_file: Path to the dictionary file
        
    Returns:
        Set of words if successful, None if there was an error
        
    The dictionary file should contain one word per line.
    Words are converted to lowercase before being added to the set.
    Empty lines and whitespace are stripped.
    """
    try:
        # Check if file exists
        if not os.path.exists(dict_file):
            print(f"Error: File '{dict_file}' not found.")
            return None
            
        # Read and process file
        with open(dict_file, 'r', encoding='utf-8') as f:
            words = {line.strip().lower() for line in f if line.strip()}
            
        # Validate dictionary
        if not words:
            print("Error: Dictionary is empty.")
            return None
            
        return words
        
    except UnicodeDecodeError:
        print(f"Error: File '{dict_file}' has invalid encoding. Please use UTF-8.")
        return None
    except Exception as e:
        print(f"An error occurred while loading the dictionary: {str(e)}")
        return None

def is_valid_word(word: str, dictionary: Set[str]) -> bool:
    """
    Check if a word is valid according to the dictionary.
    
    Args:
        word: Word to check
        dictionary: Set of valid words
        
    Returns:
        True if word is in dictionary, False otherwise
    """
    return word.lower() in dictionary

def calculate_word_score(word: str, tile_system: TileSystem) -> int:
    """
    Calculate the base score for a word without board multipliers.
    
    Args:
        word: The word to score
        tile_system: TileSystem instance for letter values
        
    Returns:
        Base score for the word
    """
    return sum(tile_system.get_letter_value(letter) for letter in word)

def get_word_multiplier(bonus_tiles: str) -> int:
    """
    Calculate the word score multiplier based on bonus tiles.
    
    Args:
        bonus_tiles: String of bonus types ("TW", "DW")
        
    Returns:
        Total word multiplier
    """
    multiplier = 1
    for bonus in bonus_tiles:
        if bonus == "TW":
            multiplier *= 3
        elif bonus == "DW":
            multiplier *= 2
    return multiplier

def get_letter_multiplier(bonus_type: str) -> int:
    """
    Get the letter score multiplier for a bonus type.
    
    Args:
        bonus_type: Bonus type ("TL", "DL")
        
    Returns:
        Letter multiplier (1, 2, or 3)
    """
    if bonus_type == "TL":
        return 3
    elif bonus_type == "DL":
        return 2
    return 1
from dataclasses import dataclass
from typing import Dict, List
import random

@dataclass
class ScrabbleTile:
    """Represents a single Scrabble tile"""
    letter: str
    value: int
    is_blank: bool = False

class TileSystem:
    """Manages the tile distribution and bag for the game"""
    
    # Standard Romanian Scrabble tile distribution
    TILE_DISTRIBUTION = {
        'A': {'count': 11, 'value': 1},
        'B': {'count': 2, 'value': 9},
        'C': {'count': 5, 'value': 1},
        'D': {'count': 4, 'value': 2},
        'E': {'count': 9, 'value': 1},
        'F': {'count': 2, 'value': 8},
        'G': {'count': 2, 'value': 9},
        'H': {'count': 1, 'value': 10},
        'I': {'count': 10, 'value': 1},
        'Î': {'count': 1, 'value': 8},
        'J': {'count': 1, 'value': 10},
        'L': {'count': 4, 'value': 1},
        'M': {'count': 3, 'value': 4},
        'N': {'count': 6, 'value': 1},
        'O': {'count': 5, 'value': 1},
        'P': {'count': 4, 'value': 2},
        'R': {'count': 7, 'value': 1},
        'S': {'count': 5, 'value': 1},
        'Ș': {'count': 1, 'value': 8},
        'T': {'count': 7, 'value': 1},
        'Ț': {'count': 1, 'value': 8},
        'U': {'count': 6, 'value': 1},
        'V': {'count': 2, 'value': 8},
        'X': {'count': 1, 'value': 10},
        'Z': {'count': 1, 'value': 10},
        '*': {'count': 2, 'value': 0}  # Blank tiles
    }

    def __init__(self):
        """Initialize the tile system with an empty bag"""
        self.bag: List[ScrabbleTile] = []
        self.initialize_bag()

    def initialize_bag(self):
        """Fill the bag with the initial distribution of tiles"""
        self.bag.clear()
        for letter, info in self.TILE_DISTRIBUTION.items():
            for _ in range(info['count']):
                is_blank = letter == '*'
                self.bag.append(ScrabbleTile(letter, info['value'], is_blank))
        random.shuffle(self.bag)

    def draw_tiles(self, count: int) -> List[ScrabbleTile]:
        """Draw a specified number of tiles from the bag"""
        if count > len(self.bag):
            count = len(self.bag)
        drawn_tiles = self.bag[:count]
        self.bag = self.bag[count:]
        return drawn_tiles

    def return_tiles(self, tiles: List[ScrabbleTile]):
        """Return tiles to the bag and shuffle"""
        self.bag.extend(tiles)
        random.shuffle(self.bag)

    def remaining_tiles(self) -> int:
        """Get the number of tiles remaining in the bag"""
        return len(self.bag)

    def get_letter_value(self, letter: str) -> int:
        """Get the point value for a given letter"""
        if letter == '*':
            return 0
        return self.TILE_DISTRIBUTION.get(letter, {'value': 0})['value']

    def validate_tiles(self, tiles: List[ScrabbleTile]) -> bool:
        """Validate that a set of tiles could legally come from this distribution"""
        # Count tiles by letter
        counts = {}
        for tile in tiles:
            counts[tile.letter] = counts.get(tile.letter, 0) + 1
            
        # Check against distribution
        for letter, count in counts.items():
            if letter not in self.TILE_DISTRIBUTION:
                return False
            if count > self.TILE_DISTRIBUTION[letter]['count']:
                return False
        return True
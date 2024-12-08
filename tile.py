from dataclasses import dataclass
from typing import Dict, List
import random

@dataclass
class ScrabbleTile:
    letter: str
    value: int
    is_blank: bool = False

class TileSystem:
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
        '*': {'count': 2, 'value': 0}  
    }

    def __init__(self):
        self.bag: List[ScrabbleTile] = []
        self.initialize_bag()

    def initialize_bag(self):
        self.bag.clear()
        for letter, info in self.TILE_DISTRIBUTION.items():
            for _ in range(info['count']):
                is_blank = letter == '*'
                self.bag.append(ScrabbleTile(letter, info['value'], is_blank))
        random.shuffle(self.bag)

    def draw_tiles(self, count: int) -> List[ScrabbleTile]:
        if count > len(self.bag):
            count = len(self.bag)
        drawn_tiles = self.bag[:count]
        self.bag = self.bag[count:]
        return drawn_tiles

    def return_tiles(self, tiles: List[ScrabbleTile]):
        self.bag.extend(tiles)
        random.shuffle(self.bag)

    def remaining_tiles(self) -> int:
        return len(self.bag)
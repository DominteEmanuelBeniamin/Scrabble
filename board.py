from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from cell import ScrabbleCell
from typing import List, Tuple, Optional, Dict
from tile import TileSystem

class ScrabbleBoard(QWidget):
    word_played = pyqtSignal(int)  # Signal to emit score when valid word is played
    move_completed = pyqtSignal()  # Signal to notify game that move is complete
    
    def __init__(self, tile_rack=None, dictionary=None):
        super().__init__()
        self.tile_rack = tile_rack
        self.dictionary = dictionary
        self.current_move_cells = []  # Track cells used in current move
        self.current_move_tiles = {}  # Track tiles placed in current move
        self.first_move = True
        self.game_state = {}  # Track all placed tiles
        self.selected_cell = None  # Track selected cell for placement
        self.special_squares = {
            'TW': [(0,0), (0,7), (0,14), (7,0), (7,14), (14,0), (14,7), (14,14)],
            'DW': [(1,1), (1,13), (2,2), (2,12), (3,3), (3,11), (4,4), (4,10),
                   (10,4), (10,10), (11,3), (11,11), (12,2), (12,12), (13,1), (13,13)],
            'TL': [(1,5), (1,9), (5,1), (5,5), (5,9), (5,13), (9,1), (9,5),
                   (9,9), (9,13), (13,5), (13,9)],
            'DL': [(0,3), (0,11), (2,6), (2,8), (3,0), (3,7), (3,14),
                   (6,2), (6,6), (6,8), (6,12), (7,3), (7,11),
                   (8,2), (8,6), (8,8), (8,12), (11,0), (11,7), (11,14),
                   (12,6), (12,8), (14,3), (14,11)]
        }
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        
        # Board grid
        board_layout = QGridLayout()
        board_layout.setSpacing(1)
        
        self.cells = {}
        for i in range(15):
            for j in range(15):
                bonus_type = ""
                for type_, positions in self.special_squares.items():
                    if (i,j) in positions:
                        bonus_type = type_
                        break
                
                cell = ScrabbleCell(bonus_type, self)
                cell.setProperty('position', (i,j))
                board_layout.addWidget(cell, i, j)
                self.cells[(i,j)] = cell

        # Controls
        controls_layout = QHBoxLayout()
        
        self.place_button = QPushButton("Place Selected Tile")
        self.place_button.clicked.connect(self.place_selected_tile)
        self.place_button.setEnabled(False)
        
        self.confirm_button = QPushButton("Confirm Move")
        self.confirm_button.clicked.connect(self.confirm_move)
        self.confirm_button.setEnabled(False)
        
        self.cancel_button = QPushButton("Cancel Move")
        self.cancel_button.clicked.connect(self.cancel_move)
        self.cancel_button.setEnabled(False)
        
        controls_layout.addWidget(self.place_button)
        controls_layout.addWidget(self.confirm_button)
        controls_layout.addWidget(self.cancel_button)
        
        main_layout.addLayout(board_layout)
        main_layout.addLayout(controls_layout)
        
        self.setLayout(main_layout)

    def handle_cell_selection(self, cell):
        """Handle selection of a board cell for tile placement"""
        # Clear previous selection if there is one
        if self.selected_cell:
            self.selected_cell.setSelected(False)
        
        # Set new selection
        self.selected_cell = cell
        cell.setSelected(True)
        
        # Enable/disable place button based on selections
        can_place = (self.selected_cell is not None and 
                    self.tile_rack and 
                    self.tile_rack.get_selected_tile() is not None)
        self.place_button.setEnabled(can_place)

    def place_selected_tile(self):
        """Place the selected rack tile on the selected board cell"""
        if not self.selected_cell or not self.tile_rack:
            return
            
        tile = self.tile_rack.get_selected_tile()
        if not tile:
            return
            
        pos = self.selected_cell.property('position')
        if pos and not self.selected_cell.letter:
            # Place the tile
            self.selected_cell.setLetter(tile.letter)
            self.tile_rack.remove_selected_tile()
            
            # Track the move
            self.current_move_cells.append(pos)
            self.current_move_tiles[pos] = tile.letter
            
            # Update UI state
            self.selected_cell.setSelected(False)
            self.selected_cell = None
            self.place_button.setEnabled(False)
            self.confirm_button.setEnabled(True)
            self.cancel_button.setEnabled(True)

    def confirm_move(self):
        """Validate and confirm the current move"""
        score = self.validate_move()
        if score is not None:
            # Move is valid
            self.word_played.emit(score)
            self.game_state.update(self.current_move_tiles)
            self.current_move_cells = []
            self.current_move_tiles = {}
            self.confirm_button.setEnabled(False)
            self.cancel_button.setEnabled(False)
            self.move_completed.emit()
        else:
            QMessageBox.warning(self, "Invalid Move", 
                              "This move is not valid. Please try again.")

    def cancel_move(self):
        """Cancel the current move and return tiles to rack"""
        for pos in self.current_move_cells:
            cell = self.cells[pos]
            letter = cell.letter
            cell.setLetter("")
            if self.tile_rack:
                self.tile_rack.return_tile(letter)
        
        self.current_move_cells = []
        self.current_move_tiles = {}
        self.confirm_button.setEnabled(False)
        self.cancel_button.setEnabled(False)
        
        # Clear any selection
        if self.selected_cell:
            self.selected_cell.setSelected(False)
            self.selected_cell = None
        self.place_button.setEnabled(False)

    def get_word_at_position(self, row: int, col: int, direction: str) -> Tuple[str, List[Tuple[int, int]]]:
        """Get word and positions starting at given position in given direction"""
        word = ""
        positions = []
        
        # Check preceding positions for existing letters
        r, c = row, col
        while True:
            if direction == 'horizontal':
                c -= 1
            else:
                r -= 1
            if r < 0 or c < 0 or not self.cells.get((r, c)):
                break
            if not self.cells.get((r, c)).letter:
                break
        
        # Move back to start of word
        if direction == 'horizontal':
            c += 1
        else:
            r += 1
            
        # Read forward to get complete word
        while r < 15 and c < 15 and self.cells.get((r, c)):
            if not self.cells[(r, c)].letter:
                break
            word += self.cells[(r, c)].letter
            positions.append((r, c))
            if direction == 'horizontal':
                c += 1
            else:
                r += 1
                
        return word, positions

    def validate_move(self) -> Optional[int]:
        """Validate current move and return score if valid, None if invalid"""
        if not self.current_move_cells:
            return None
            
        # Check if tiles are in line
        rows = {pos[0] for pos in self.current_move_cells}
        cols = {pos[1] for pos in self.current_move_cells}
        
        if len(rows) == 1:
            direction = 'horizontal'
            fixed_coord = list(rows)[0]
            var_coords = sorted(cols)
        elif len(cols) == 1:
            direction = 'vertical'
            fixed_coord = list(cols)[0]
            var_coords = sorted(rows)
        else:
            return None  # Tiles not in line
            
        # Check continuity
        for i in range(var_coords[0], var_coords[-1] + 1):
            coord = (fixed_coord, i) if direction == 'horizontal' else (i, fixed_coord)
            if coord not in self.current_move_cells and not self.cells[coord].letter:
                return None  # Gap in word
                
        # Get main word
        if direction == 'horizontal':
            main_word, positions = self.get_word_at_position(fixed_coord, var_coords[0], 'horizontal')
        else:
            main_word, positions = self.get_word_at_position(var_coords[0], fixed_coord, 'vertical')
            
        # Check if first move touches center
        if self.first_move and (7, 7) not in positions:
            return None
            
        # After first move, must connect to existing tiles
        if not self.first_move:
            connected = False
            for pos in positions:
                r, c = pos
                # Check all adjacent positions
                for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
                    adj_pos = (r+dr, c+dc)
                    if adj_pos in self.game_state:
                        connected = True
                        break
                if connected:
                    break
            if not connected:
                return None  # Word must connect to existing tiles
            
        # Validate all words formed
        score = 0
        all_words = [(main_word, positions)]
        
        # Check for perpendicular words formed
        for row, col in self.current_move_cells:
            if direction == 'horizontal':
                perp_word, perp_pos = self.get_word_at_position(row, col, 'vertical')
            else:
                perp_word, perp_pos = self.get_word_at_position(row, col, 'horizontal')
                
            if len(perp_word) > 1:
                all_words.append((perp_word, perp_pos))
                
        # Calculate score for all valid words
        for word, positions in all_words:
            if not self.is_valid_word(word):
                return None
            word_score = self.calculate_word_score(word, positions)
            score += word_score
            
        self.first_move = False
        return score

    def is_valid_word(self, word: str) -> bool:
        """Check if word is in dictionary"""
        return word.lower() in self.dictionary

    def calculate_word_score(self, word: str, positions: List[Tuple[int, int]]) -> int:
        """Calculate score for a word"""
        word_multiplier = 1
        word_score = 0
        
        for i, (row, col) in enumerate(positions):
            cell = self.cells[(row, col)]
            letter = cell.letter
            letter_score = self.get_letter_score(letter)
            
            # Apply letter multipliers only for newly placed tiles
            if (row, col) in self.current_move_cells:
                if cell.bonus_type == "DL":
                    letter_score *= 2
                elif cell.bonus_type == "TL":
                    letter_score *= 3
                    
                # Accumulate word multipliers
                if cell.bonus_type == "DW":
                    word_multiplier *= 2
                elif cell.bonus_type == "TW":
                    word_multiplier *= 3
                    
            word_score += letter_score
            
        return word_score * word_multiplier

    def get_letter_score(self, letter: str) -> int:
        """Get score value for a letter"""
        return TileSystem.TILE_DISTRIBUTION.get(letter, {'value': 0})['value']

    def clear_board(self):
        """Clear all tiles from the board"""
        for cell in self.cells.values():
            cell.setLetter("")
        self.game_state = {}
        self.current_move_cells = []
        self.current_move_tiles = {}
        self.first_move = True
        self.confirm_button.setEnabled(False)
        self.cancel_button.setEnabled(False)
        if self.selected_cell:
            self.selected_cell.setSelected(False)
            self.selected_cell = None
        self.place_button.setEnabled(False)
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from tile import ScrabbleTile, TileSystem
from cell import ScrabbleCell

class TileRack(QWidget):
    def __init__(self):
        super().__init__()
        self.tiles = [None] * 7
        self.selected_tiles = set()  # For exchange mode
        self.selected_tile_index = None  # For placement mode
        self.exchange_mode = False
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.tile_widgets = []
        
        for i in range(7):
            tile_widget = ScrabbleCell()
            tile_widget.setFixedSize(45, 45)
            tile_widget.is_rack_tile = True
            tile_widget.setProperty('rack_index', i)
            self.tile_widgets.append(tile_widget)
            layout.addWidget(tile_widget)
        
        self.setLayout(layout)

    def handle_tile_selection(self, cell):
        """Handle selection of a tile for placement or exchange"""
        index = self.tile_widgets.index(cell)
        
        if self.tiles[index] is None:
            return

        if self.exchange_mode:
            # Handle exchange mode selection (multiple tiles)
            if index in self.selected_tiles:
                self.selected_tiles.remove(index)
                cell.setSelected(False)
            else:
                self.selected_tiles.add(index)
                cell.setSelected(True)
        else:
            # Handle placement mode selection (single tile)
            # Clear previous selection if any
            if self.selected_tile_index is not None:
                self.tile_widgets[self.selected_tile_index].setSelected(False)
            
            # Set new selection
            self.selected_tile_index = index
            cell.setSelected(True)

    def clear_selection(self):
        """Clear all selections"""
        self.selected_tile_index = None
        self.selected_tiles.clear()
        for widget in self.tile_widgets:
            widget.setSelected(False)

    def get_selected_tile(self):
        """Get the currently selected tile for placement"""
        if not self.exchange_mode and self.selected_tile_index is not None:
            return self.tiles[self.selected_tile_index]
        return None

    def remove_selected_tile(self):
        """Remove and return the selected tile after placement"""
        if not self.exchange_mode and self.selected_tile_index is not None:
            tile = self.tiles[self.selected_tile_index]
            self.tiles[self.selected_tile_index] = None
            self.tile_widgets[self.selected_tile_index].setLetter("")
            self.tile_widgets[self.selected_tile_index].setSelected(False)
            self.selected_tile_index = None
            return tile
        return None

    def return_tile(self, letter):
        """Return a tile to the first empty position in the rack"""
        if letter:
            tile_info = TileSystem.TILE_DISTRIBUTION.get(letter)
            if tile_info:
                # Find first empty position
                for i in range(len(self.tiles)):
                    if self.tiles[i] is None:
                        # Create new tile and add to rack
                        self.tiles[i] = ScrabbleTile(letter, tile_info['value'])
                        self.tile_widgets[i].setLetter(letter)
                        break

    def add_tiles(self, new_tiles):
        """Add new tiles to empty positions in the rack"""
        empty_positions = [i for i, tile in enumerate(self.tiles) if tile is None]
        for tile, position in zip(new_tiles, empty_positions):
            self.tiles[position] = tile
            self.tile_widgets[position].setLetter(tile.letter)

    def clear_rack(self):
        """Clear all tiles from the rack"""
        self.tiles = [None] * 7
        self.selected_tiles.clear()
        self.selected_tile_index = None
        self.exchange_mode = False
        for widget in self.tile_widgets:
            widget.setLetter("")
            widget.setSelected(False)

    def get_rack_value(self):
        """Calculate total value of tiles currently in rack"""
        return sum(tile.value for tile in self.tiles if tile is not None)

    def get_tiles(self):
        """Get list of all tiles currently in rack"""
        return [tile for tile in self.tiles if tile is not None]

    def get_selected_tiles(self):
        """Get list of tiles selected for exchange"""
        if self.exchange_mode:
            return [self.tiles[i] for i in self.selected_tiles if self.tiles[i] is not None]
        return []

    def exchange_tiles(self, old_tiles, new_tiles):
        """Exchange selected tiles for new ones"""
        # Remove old tiles
        for i in sorted(self.selected_tiles, reverse=True):
            self.tiles[i] = None
            self.tile_widgets[i].setLetter("")
            self.tile_widgets[i].setSelected(False)
        self.selected_tiles.clear()
        
        # Add new tiles
        self.add_tiles(new_tiles)

    def set_exchange_mode(self, enabled):
        """Set whether rack is in exchange mode"""
        self.exchange_mode = enabled
        if not enabled:
            self.clear_selection()
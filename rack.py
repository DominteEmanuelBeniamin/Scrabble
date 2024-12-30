from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from tile import ScrabbleTile
from cell import ScrabbleCell

class TileRack(QWidget):
    tile_selected = pyqtSignal(ScrabbleTile, int)

    def __init__(self):
        super().__init__()
        self.tiles = [None] * 7
        self.selected_index = None
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

    def add_tiles(self, new_tiles):
        empty_positions = [i for i, tile in enumerate(self.tiles) if tile is None]
        for tile, position in zip(new_tiles, empty_positions):
            self.tiles[position] = tile
            self.tile_widgets[position].setLetter(tile.letter)
        self.update_display()

    def remove_tile(self, index):
        if 0 <= index < len(self.tiles) and self.tiles[index]:
            tile = self.tiles[index]
            self.tiles[index] = None
            self.tile_widgets[index].setLetter("")
            return tile
        return None

    def update_display(self):
        for i, (tile, widget) in enumerate(zip(self.tiles, self.tile_widgets)):
            if tile:
                widget.setLetter(tile.letter)
                if i == self.selected_index:
                    widget.setStyleSheet("background-color: lightblue;")
                else:
                    widget.setStyleSheet("")
            else:
                widget.setLetter("")
                widget.setStyleSheet("")
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from tile import ScrabbleTile
from typing import List, Optional

class TileRack(QWidget):
    tile_selected = pyqtSignal(ScrabbleTile, int)  

    def __init__(self):
        super().__init__()
        self.tiles: List[Optional[ScrabbleTile]] = [None] * 7  
        self.selected_index: Optional[int] = None
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)
        
        from cell import ScrabbleCell  
        self.tile_widgets = []
        
        for _ in range(7):
            tile_widget = ScrabbleCell()
            tile_widget.setFixedSize(45, 45)  
            tile_widget.mousePressEvent = lambda e, i=len(self.tile_widgets): self.select_tile(i)
            self.tile_widgets.append(tile_widget)
            layout.addWidget(tile_widget)
        
        self.setLayout(layout)

    def add_tiles(self, new_tiles: List[ScrabbleTile]):
        empty_positions = [i for i, tile in enumerate(self.tiles) if tile is None]
        for tile, position in zip(new_tiles, empty_positions):
            self.tiles[position] = tile
            self.update_display()

    def remove_tile(self, index: int) -> Optional[ScrabbleTile]:
        if 0 <= index < len(self.tiles) and self.tiles[index]:
            tile = self.tiles[index]
            self.tiles[index] = None
            self.update_display()
            return tile
        return None

    def select_tile(self, index: int):
        if self.tiles[index]:
            self.selected_index = index
            self.tile_selected.emit(self.tiles[index], index)
            self.update_display()

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
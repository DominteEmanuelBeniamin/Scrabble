from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, 
                           QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import QFont
from board import ScrabbleBoard
from tile import TileSystem
from rack import TileRack

class ScrabbleGame(QMainWindow):
    def __init__(self, dictionary):
        super().__init__()
        self.dictionary = dictionary
        self.tile_system = TileSystem()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Scrabble Game')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        self.rack = TileRack()
        
        self.board = ScrabbleBoard(tile_rack=self.rack)
        main_layout.addWidget(self.board)

        side_panel = QWidget()
        side_layout = QVBoxLayout(side_panel)

        title_label = QLabel("Scrabble")
        title_label.setFont(QFont('Arial', 20, QFont.Bold))
        self.score_label = QLabel("Score: 0")
        new_game_btn = QPushButton("New Game")
        new_game_btn.clicked.connect(self.start_new_game)
        
        self.tiles_remaining_label = QLabel("Tiles remaining: 100")
        
        side_layout.addWidget(title_label)
        side_layout.addWidget(self.score_label)
        side_layout.addWidget(self.tiles_remaining_label)
        side_layout.addWidget(self.rack)
        side_layout.addWidget(new_game_btn)
        side_layout.addStretch()

        main_layout.addWidget(side_panel)

    def start_new_game(self):
        self.tile_system.initialize_bag()
        initial_tiles = self.tile_system.draw_tiles(7)
        self.rack.add_tiles(initial_tiles)
        self.update_remaining_tiles()

    def handle_tile_selection(self, tile, index):
        pass

    def update_remaining_tiles(self):
        count = self.tile_system.remaining_tiles()
        self.tiles_remaining_label.setText(f"Tiles remaining: {count}")
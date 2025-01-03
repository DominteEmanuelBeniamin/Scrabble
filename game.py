from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, 
                           QVBoxLayout, QLabel, QPushButton,
                           QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from board import ScrabbleBoard
from tile import TileSystem
from rack import TileRack

class ScrabbleGame(QMainWindow):
    def __init__(self, dictionary):
        super().__init__()
        self.dictionary = dictionary
        self.tile_system = TileSystem()
        self.score = 0
        self.rack = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Single Player Scrabble')
        self.setGeometry(100, 100, 1000, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # Game area (left side)
        game_area = QWidget()
        game_layout = QVBoxLayout(game_area)

        # Create player rack
        self.rack = TileRack()
        
        # Pass rack and dictionary to board
        self.board = ScrabbleBoard(tile_rack=self.rack, dictionary=self.dictionary)
        game_layout.addWidget(self.board)
        game_layout.addWidget(self.rack)

        main_layout.addWidget(game_area, stretch=2)

        # Sidebar (right side)
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)

        # Game info
        title_label = QLabel("Single Player Scrabble")
        title_label.setFont(QFont('Arial', 20, QFont.Bold))
        
        self.score_label = QLabel("Score: 0")
        self.score_label.setFont(QFont('Arial', 12))
        
        self.tiles_remaining_label = QLabel("Tiles remaining: 100")

        # Game controls
        new_game_btn = QPushButton("New Game")
        new_game_btn.clicked.connect(self.start_new_game)
        
        exchange_tiles_btn = QPushButton("Exchange Tiles")
        exchange_tiles_btn.clicked.connect(self.exchange_tiles)
        exchange_tiles_btn.setToolTip("Select tiles to exchange by clicking them")
        
        skip_turn_btn = QPushButton("Skip Turn")
        skip_turn_btn.clicked.connect(self.skip_turn)

        # Add widgets to sidebar
        sidebar_layout.addWidget(title_label)
        sidebar_layout.addWidget(self.score_label)
        sidebar_layout.addWidget(self.tiles_remaining_label)
        sidebar_layout.addWidget(new_game_btn)
        sidebar_layout.addWidget(exchange_tiles_btn)
        sidebar_layout.addWidget(skip_turn_btn)
        sidebar_layout.addStretch()

        main_layout.addWidget(sidebar, stretch=1)

        # Connect signals
        self.board.word_played.connect(self.update_score)
        self.board.move_completed.connect(self.end_turn)
        
        # Start new game automatically
        self.start_new_game()

    def start_new_game(self):
        reply = QMessageBox.question(self, 'New Game', 
                                   'Are you sure you want to start a new game?',
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Reset score and game state
            self.score = 0
            self.rack.clear_rack()
            
            # Reset board
            self.board.clear_board()
            
            # Reset tile system and deal initial tiles
            self.tile_system.initialize_bag()
            initial_tiles = self.tile_system.draw_tiles(7)
            self.rack.add_tiles(initial_tiles)
            
            self.update_remaining_tiles()
            self.update_score_display()

    def exchange_tiles(self):
        if self.tile_system.remaining_tiles() < 7:
            QMessageBox.warning(self, "Cannot Exchange", 
                              "Not enough tiles remaining in bag to exchange.")
            return
            
        # Set rack to exchange mode
        self.rack.set_exchange_mode(True)
            
        selected_tiles = self.rack.get_selected_tiles()
        if not selected_tiles:
            QMessageBox.information(self, "Select Tiles", 
                                  "Please select tiles to exchange by clicking them.")
            return

        # Return selected tiles to bag and draw new ones
        self.tile_system.return_tiles(selected_tiles)
        new_tiles = self.tile_system.draw_tiles(len(selected_tiles))
        self.rack.exchange_tiles(selected_tiles, new_tiles)
        
        # Exit exchange mode
        self.rack.set_exchange_mode(False)
        
        self.update_remaining_tiles()
        self.end_turn()

    def skip_turn(self):
        reply = QMessageBox.question(self, 'Skip Turn', 
                                   'Are you sure you want to skip your turn?',
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.end_turn()

    def update_score(self, points):
        self.score += points
        self.update_score_display()

    def update_score_display(self):
        self.score_label.setText(f"Score: {self.score}")

    def update_remaining_tiles(self):
        count = self.tile_system.remaining_tiles()
        self.tiles_remaining_label.setText(f"Tiles remaining: {count}")

    def end_turn(self):
        # Draw new tiles
        new_tiles = self.tile_system.draw_tiles(7 - len(self.rack.get_tiles()))
        self.rack.add_tiles(new_tiles)
        
        self.update_remaining_tiles()
        
        # Check for game end
        if self.tile_system.remaining_tiles() == 0 and len(self.rack.get_tiles()) == 0:
            self.game_over()

    def game_over(self):
        # Subtract unplayed tiles from score
        rack_value = self.rack.get_rack_value()
        self.score -= rack_value
        self.update_score_display()
        
        QMessageBox.information(self, "Game Over", 
                              f"Game Over!\n\n"
                              f"Final Score: {self.score}")
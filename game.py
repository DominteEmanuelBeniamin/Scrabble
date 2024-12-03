from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, 
                           QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import QFont
from board import ScrabbleBoard

class ScrabbleGame(QMainWindow):
    def __init__(self, dictionary):
        super().__init__()
        self.dictionary = dictionary
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Scrabble Game')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        self.board = ScrabbleBoard()
        main_layout.addWidget(self.board)

        side_panel = QWidget()
        side_layout = QVBoxLayout(side_panel)

        title_label = QLabel("Scrabble")
        title_label.setFont(QFont('Arial', 20, QFont.Bold))
        score_label = QLabel("Score: 0")
        new_game_btn = QPushButton("New Game")
        
        side_layout.addWidget(title_label)
        side_layout.addWidget(score_label)
        side_layout.addWidget(new_game_btn)
        side_layout.addStretch()

        main_layout.addWidget(side_panel)
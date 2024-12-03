from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette

class ScrabbleCell(QFrame):
    def __init__(self, bonus_type=""):
        super().__init__()
        self.bonus_type = bonus_type
        self.letter = ""
        self.initUI()

    def initUI(self):
        self.setFixedSize(40, 40)
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setLineWidth(1)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.letter_label = QLabel("")
        self.letter_label.setAlignment(Qt.AlignCenter)
        self.letter_label.setFont(QFont('Arial', 14, QFont.Bold))
        
        self.bonus_label = QLabel(self.bonus_type)
        self.bonus_label.setAlignment(Qt.AlignCenter)
        self.bonus_label.setFont(QFont('Arial', 8))
        
        layout.addWidget(self.bonus_label)
        layout.addWidget(self.letter_label)

        self.setColor()

    def setColor(self):
        palette = self.palette()
        if self.bonus_type == "TW":
            color = QColor("#ff6b6b")
        elif self.bonus_type == "DW":
            color = QColor("#ffb6b9")
        elif self.bonus_type == "TL":
            color = QColor("#4ecdc4")
        elif self.bonus_type == "DL":
            color = QColor("#96ceb4")
        else:
            color = QColor("white")
        
        palette.setColor(QPalette.Background, color)
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def setLetter(self, letter):
        self.letter = letter
        self.letter_label.setText(letter)
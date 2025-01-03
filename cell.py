from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette

class ScrabbleCell(QFrame):
    def __init__(self, bonus_type="", parent=None):
        super().__init__(parent)
        self.bonus_type = bonus_type
        self.letter = ""
        self.is_rack_tile = False
        self.is_selected = False
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
        if self.is_selected:
            color = QColor("#87CEFA")  # Light blue for selected
        elif self.bonus_type == "TW":
            color = QColor("#ff6b6b")  # Red for Triple Word
        elif self.bonus_type == "DW":
            color = QColor("#ffb6b9")  # Pink for Double Word
        elif self.bonus_type == "TL":
            color = QColor("#4ecdc4")  # Teal for Triple Letter
        elif self.bonus_type == "DL":
            color = QColor("#96ceb4")  # Light green for Double Letter
        else:
            color = QColor("white")  # Default color
        
        palette.setColor(QPalette.Window, color)
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def setLetter(self, letter):
        """Set the letter displayed in this cell"""
        self.letter = letter
        self.letter_label.setText(letter)

    def mousePressEvent(self, event):
        """Handle mouse press events for selection"""
        if event.button() == Qt.LeftButton:
            if self.is_rack_tile:
                # Handle rack tile selection
                if hasattr(self.parent(), 'handle_tile_selection'):
                    self.parent().handle_tile_selection(self)
            elif not self.letter and not self.is_rack_tile:
                # Handle board cell selection
                if hasattr(self.parent(), 'handle_cell_selection'):
                    self.parent().handle_cell_selection(self)

    def setSelected(self, selected):
        """Set whether this cell is selected"""
        self.is_selected = selected
        self.setColor()

    def getText(self):
        """Get the current letter in this cell"""
        return self.letter
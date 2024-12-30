from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QFont, QColor, QPalette, QDrag

class ScrabbleCell(QFrame):
    def __init__(self, bonus_type="", parent=None):
        super().__init__(parent)
        self.bonus_type = bonus_type
        self.letter = ""
        self.setAcceptDrops(True)
        self.is_rack_tile = False
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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.letter and self.is_rack_tile:
            drag = QDrag(self)
            mime_data = QMimeData()
            
            mime_data.setText(self.letter)
            mime_data.setProperty('source_index', self.property('rack_index'))
            
            drag.setMimeData(mime_data)
            drag.exec_(Qt.MoveAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            letter = event.mimeData().text()
            source_index = event.mimeData().property('source_index')
            
            self.setLetter(letter)
            
            if not self.is_rack_tile and hasattr(self, 'rack_reference'):
                self.rack_reference.remove_tile(source_index)
            
            event.accept()
        else:
            event.ignore()
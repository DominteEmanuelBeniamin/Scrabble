from PyQt5.QtWidgets import QWidget, QGridLayout
from cell import ScrabbleCell

class ScrabbleBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
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

        layout = QGridLayout()
        layout.setSpacing(1)
        
        self.cells = {}
        for i in range(15):
            for j in range(15):
                bonus_type = ""
                for type_, positions in self.special_squares.items():
                    if (i,j) in positions:
                        bonus_type = type_
                        break
                
                cell = ScrabbleCell(bonus_type)
                layout.addWidget(cell, i, j)
                self.cells[(i,j)] = cell

        self.setLayout(layout)
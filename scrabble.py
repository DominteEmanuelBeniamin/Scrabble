import sys
from PyQt5.QtWidgets import QApplication
from game import ScrabbleGame
from utils import load_dictionary

def main():
    if len(sys.argv) != 2:
        print("Usage: python scrabble.py <dict_file>")
        sys.exit(1)

    dict_file = sys.argv[1]
    dictionary = load_dictionary(dict_file)

    if dictionary:
        app = QApplication(sys.argv)
        game = ScrabbleGame(dictionary)
        game.show()
        sys.exit(app.exec_())
    else:
        print("The dictionary is empty!")
        sys.exit(1)

if __name__ == "__main__":
    main()
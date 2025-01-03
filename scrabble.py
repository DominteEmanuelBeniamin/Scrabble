import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from game import ScrabbleGame
from utils import load_dictionary

def main():
    """Main entry point for the Scrabble game"""
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python scrabble.py <dict_file>")
        sys.exit(1)

    # Get dictionary file path
    dict_file = sys.argv[1]
    
    try:
        # Create application
        app = QApplication(sys.argv)
        
        # Load dictionary
        dictionary = load_dictionary(dict_file)
        if not dictionary:
            QMessageBox.critical(None, "Error", "The dictionary is empty!")
            sys.exit(1)
            
        # Create and show game
        game = ScrabbleGame(dictionary)
        game.show()
        
        # Start application event loop
        sys.exit(app.exec_())
        
    except Exception as e:
        QMessageBox.critical(None, "Error", f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

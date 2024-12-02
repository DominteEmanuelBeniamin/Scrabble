import sys

def load_dictionary(dict_file):
    try:
        with open(dict_file, 'r', encoding='utf-8') as f:
            words = {line.strip().lower() for line in f if line.strip()}
        return words
    except FileNotFoundError:
        print(f"Error: File '{dict_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while loading the dictionary: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python scrabble.py <dict_file>")
        sys.exit(1)

    dict_file = sys.argv[1]
    dictionary = load_dictionary(dict_file)

    if dictionary:  
        print(f"The dictionary was successfully loaded. Number of words: {len(dictionary)}")
        sample_words = sorted(list(dictionary))[:10]
        print("\nFirst 10 words from the dictionary:")
        for word in sample_words:
            print(word)
    else:
        print("The dictionary is empty!")
        sys.exit(1)

if __name__ == "__main__":
    main()

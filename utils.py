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

import json

def save_data(entries_list, filename):
    """Saves the list of entry dictionaries to a JSON file."""
    # print(f"Saving {len(entries_list)} entries to {filename}...") # Optional
    try:
        with open(filename, 'w') as f:
            json.dump(entries_list, f, indent=2)
        print(f"JSON file ready at {filename} (Total entries: {len(entries_list)})")
    except IOError:
        print(f"Error: Could not write to file {filename}")

def load_data(filename):
    """Loads data from a JSON file."""
    print(f"Loading data from {filename}...")
    try:
        with open(filename, 'r') as f:
            entries_list = json.load(f)
        print(f"Successfully loaded {len(entries_list)} entries.")
        return entries_list
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filename}.")
    return []
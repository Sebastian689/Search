import os

def find_file(filename, search_path):
    """
    Search for a file with the given filename in the search_path directory
    and recursively in all subdirectories.
    
    Args:
        filename: Name of the file to search for
        search_path: Directory to start the search from
    
    Returns:
        Full path to the file if found, None otherwise
    """
    # Convert to absolute path to ensure consistent results
    search_path = os.path.abspath(search_path)
    
    # Walk through directory and all subdirectories
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            # File found, return the full path
            return os.path.join(root, filename)
    
    # File not found
    return None

def main():
    # Example usage
    filename_to_find = "tsconfig.json"
    start_directory = "C:/"  # Change this to your starting directory
    
    print(f"Searching for {filename_to_find} starting in {start_directory}...")
    result = find_file(filename_to_find, start_directory)
    
    if result:
        print(f"File found at: {result}")
    else:
        print(f"File {filename_to_find} not found in {start_directory} or its subdirectories")

if __name__ == "__main__":
    main()
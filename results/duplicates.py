import os
import hashlib
from collections import defaultdict

# Function to calculate the MD5 hash of a file
def calculate_md5(file_path, chunk_size=8192):
    md5_hash = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None

# Function to find files with the same MD5 hash in a directory
def find_duplicate_files(directory):
    md5_dict = defaultdict(list)

    # Walk through the directory and compute MD5 for each file
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            md5 = calculate_md5(file_path)
            if md5:
                md5_dict[md5].append(file_path)

    # Filter the dictionary to find MD5 hashes with more than one file
    duplicates = {md5: paths for md5, paths in md5_dict.items() if len(paths) > 1}
    
    return duplicates

# Example usage
directory_path = "test"  # Replace with your directory path
duplicates = find_duplicate_files(directory_path)

if duplicates:
    print("Duplicate files found:")
    for md5, files in duplicates.items():
        print(f"MD5: {md5}")
        for file in files:
            print(f"  - {file}")
else:
    print("No duplicate files found.")

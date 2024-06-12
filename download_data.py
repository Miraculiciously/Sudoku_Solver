import os
import requests
from kaggle.api.kaggle_api_extended import KaggleApi

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_file(url, destination):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(destination, 'wb') as file:
            file.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")

def download_kaggle_file(dataset, file_name, destination):
    create_directory(destination)  # Ensure destination directory exists
    try:
        api = KaggleApi()
        api.authenticate()
        api.dataset_download_file(dataset, file_name, path=destination, unzip=True)
    except Exception as e:
        print(f"Error downloading {file_name} from {dataset}: {e}")

def main():
    # Create the raw_data directory
    raw_data_dir = 'raw_data'
    create_directory(raw_data_dir)
    
    # URLs and filenames
    files_to_download = [
        ("https://github.com/maxbergmark/sudoku-solver/raw/master/data-sets/hard_sudokus_solved.txt", "hard_sudokus_solved.txt"),
        ("https://github.com/maxbergmark/sudoku-solver/raw/master/data-sets/all_17_clue_sudokus.txt", "all_17_clue_sudokus.txt")
    ]
    
    kaggle_files = [
        ("rohanrao/sudoku", "sudoku.csv"),
        ("informoney/4-million-sudoku-puzzles-easytohard", "sudoku_cluewise.csv"),
        ("radcliffe/3-million-sudoku-puzzles-with-ratings", "sudoku-3m.csv"),
        ("alekseykocherzhenko/sudoku", "training_puzzles.txt"),
        ("alekseykocherzhenko/sudoku", "training_solutions.txt")
    ]
    
    # Download files from GitHub
    for url, filename in files_to_download:
        destination_path = os.path.join(raw_data_dir, filename)
        print(f"Downloading {url} to {destination_path}")
        download_file(url, destination_path)
    
    # Download files from Kaggle
    for dataset, filename in kaggle_files:
        print(f"Downloading {filename} from {dataset}")
        download_kaggle_file(dataset, filename, raw_data_dir)

if __name__ == "__main__":
    main()

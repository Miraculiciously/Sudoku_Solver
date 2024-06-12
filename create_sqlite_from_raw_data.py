import os
import glob
import sqlite3
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import pandas as pd
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Define global batch_size
batch_size = 1000

def create_database(db_path, validation=False):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    if validation:
        c.execute('''
            CREATE TABLE IF NOT EXISTS validation_data (
                puzzle TEXT
            )
        ''')
    else:
        c.execute('''
            CREATE TABLE IF NOT EXISTS training_data (
                puzzle TEXT,
                solution TEXT,
                clue INTEGER
            )
        ''')
    conn.commit()
    conn.close()

def insert_data_to_database(db_path, data, validation=False):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    if validation:
        c.executemany('INSERT INTO validation_data (puzzle) VALUES (?)', data)
    else:
        c.executemany('INSERT INTO training_data (puzzle, solution, clue) VALUES (?, ?, ?)', data)
    conn.commit()
    conn.close()

def count_entries_in_database(db_path, validation=False):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    if validation:
        c.execute('SELECT COUNT(*) FROM validation_data')
    else:
        c.execute('SELECT COUNT(*) FROM training_data')
    count = c.fetchone()[0]
    conn.close()
    return count

def process_txt(file_path, solution_file_path=None):
    """Process TXT file and return the data in the desired format."""
    with open(file_path, 'r') as file:
        puzzles = [line.strip().replace('.', '0') for line in file.readlines()]

    if solution_file_path:
        with open(solution_file_path, 'r') as file:
            solutions = [line.strip().replace('.', '0') for line in file.readlines()]
    else:
        solutions = puzzles  # If no solution file is provided, assume puzzles are solutions

    clues = [str(p.count('0')) for p in puzzles]
    return list(zip(puzzles, solutions, clues))

def process_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        puzzle_columns = [col for col in df.columns if 'puzzle' in col.lower() or 'quiz' in col.lower()]
        solution_columns = [col for col in df.columns if 'solution' in col.lower()]
        # clue_column = [col for col in df.columns if 'clue' in col.lower()]

        if not puzzle_columns or not solution_columns or len(puzzle_columns) > 1 or len(solution_columns) > 1:
            print(f"Available columns in {file_path}: {df.columns.tolist()}")
            puzzle_column = input("\nPlease enter the column name for puzzles: ")
            solution_column = input("\nPlease enter the column name for solutions: ")
            df['puzzle'] = df[puzzle_column]
            df['solution'] = df[solution_column]
        else:
            df['puzzle'] = df[puzzle_columns[0]]
            df['solution'] = df[solution_columns[0]]
        
        df['puzzle'] = df['puzzle'].apply(lambda x: str(x).replace('.', '0'))
        # df['solution'] = df['solution'].apply(lambda x: str(x).replace('.', '0'))
        df['clue'] = df['puzzle'].apply(lambda x: x.count('0'))
        
        data = df[['puzzle', 'solution', 'clue']].values.tolist()
        return data
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return []

def process_datasets_parallel(datasets, folder_path, db_path, validation=False, batch_size=batch_size):
    create_database(db_path)
    
    file_list = []
    for dataset in datasets:
        file_path = os.path.join(folder_path, dataset)
        if os.path.isdir(file_path):
            for root, _, files in os.walk(file_path):
                for file in files:
                    file_list.append(os.path.join(root, file))
        else:
            file_list.append(file_path)
    
    with Pool(cpu_count()) as pool:
        data = []
        for file_data in tqdm(pool.imap_unordered(process_file, file_list), total=len(file_list)):
            data.extend(file_data)

    insert_data_to_database(db_path, data)
    print(f"Number of entries in {db_path}: {count_entries_in_database(db_path)}")


def process_file(file_path):
    if file_path.endswith('.txt'):
        return process_txt(file_path)
    elif file_path.endswith('.csv'):
        return process_csv(file_path)
    else:
        return []

def main():
    raw_data_path = 'raw_data'
    data_path = 'data'

    if not os.path.exists(data_path):
        os.makedirs(data_path)

    training_dataset_folders = [
        "archive",
        "hard_sudokus_solved",
        "sudoku.csv",
        "sudoku_cluewise.csv",
        "sudoku-3m.csv",
        "training.txt"
    ]

    validation_dataset_folders = [
        "Unsolved.txt"
    ]

    process_datasets_parallel(training_dataset_folders, raw_data_path, os.path.join(data_path, 'training.db'))    
    process_datasets_parallel(validation_dataset_folders, raw_data_path, os.path.join(data_path, 'validation.db'))

if __name__ == '__main__':
    main()

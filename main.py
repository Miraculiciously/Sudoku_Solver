import sqlite3
from datetime import datetime
import glob
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Flatten, Conv2D, Reshape, Input
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard
from keras_tuner import HyperModel, RandomSearch
import numpy as np
import os 
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def list_tables(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    return [table[0] for table in tables]

def load_training_data_in_batches(batch_size=128):
    conn = sqlite3.connect('data\\training.db')
    cursor = conn.cursor()
    cursor.execute("SELECT puzzle, solution, clue FROM training_data ORDER BY clue DESC")
    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        puzzles, solutions, clues = zip(*batch)
        puzzles = np.array([list(map(int, p)) for p in puzzles])
        puzzles = np.array([p.reshape(9, 9) for p in puzzles])
        solutions = np.array([list(map(int, s)) for s in solutions])
        solutions = np.array([s.reshape(9, 9) for s in solutions])
        yield puzzles, solutions, clues
    conn.close()

def load_validation_data():
    conn = sqlite3.connect('data\\validation.db')
    cursor = conn.cursor()
    cursor.execute("SELECT puzzle FROM validation_data")
    puzzles = cursor.fetchall()
    puzzles = np.array([list(map(int, p[0])) for p in puzzles])
    puzzles = np.array([p.reshape(9, 9) for p in puzzles])
    conn.close()
    return puzzles

def preprocess_data(puzzles, solutions):
    puzzles = puzzles.reshape((puzzles.shape[0], 9, 9, 1))
    solutions = solutions.reshape((solutions.shape[0], 81))
    solutions = to_categorical(solutions, num_classes=10)[:, :, 1:]  # Skip class 0
    return puzzles, solutions

def build_model(hp):
    model = Sequential([
        Input(shape=(9, 9, 1)),
        Conv2D(hp.Int('conv_units', min_value=32, max_value=128, step=32), (3, 3), activation='relu'),
        Flatten(),
        Dense(81 * hp.Int('dense_units', min_value=8, max_value=32, step=8), activation='relu'),
        Dense(81 * 9, activation='softmax'),
        Reshape((81, 9))  # Reshape output to 81 cells each with 9 classes
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def hyperparameter_tuning():
    tuner = RandomSearch(
        build_model,
        objective='val_accuracy',
        max_trials=5,
        executions_per_trial=3,
        directory='my_dir',
        project_name='sudoku_tuning'
    )

    log_dir = "logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)

    for puzzles, solutions, clues in load_training_data_in_batches():
        puzzles, solutions = preprocess_data(puzzles, solutions)
        tuner.search(puzzles, solutions, epochs=10, validation_split=0.2, callbacks=[tensorboard_callback])

    best_model = tuner.get_best_models(num_models=1)[0]
    return best_model

def save_validation_results(timestamp, puzzles, correct, total):
    os.makedirs('validation_results', exist_ok=True)
    conn = sqlite3.connect(f'validation_results\\validation_{timestamp}.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS results (puzzle TEXT, is_valid INTEGER)")
    for puzzle, is_valid in puzzles:
        puzzle_str = ','.join(map(str, puzzle.flatten()))
        cursor.execute("INSERT INTO results (puzzle, is_valid) VALUES (?, ?)", (puzzle_str, is_valid))
    cursor.execute("CREATE TABLE IF NOT EXISTS summary (timestamp TEXT, accuracy REAL)")
    accuracy = correct / total
    cursor.execute("INSERT INTO summary (timestamp, accuracy) VALUES (?, ?)", (timestamp, accuracy))
    conn.commit()
    conn.close()

def solve_sudoku(model, puzzle):
    puzzle = puzzle.reshape((1, 9, 9, 1))
    solution = model.predict(puzzle)
    solution = solution.argmax(axis=-1).reshape((9, 9))
    return solution + 1  # Adjust solution to be 1-9

def valid_solution(solution):
    def is_valid_block(block):
        return len(block) == len(set(block))

    for i in range(9):
        row = solution[i, :]
        column = solution[:, i]
        if not is_valid_block(row) or not is_valid_block(column):
            return False
        block = solution[(i // 3) * 3: (i // 3 + 1) * 3, (i % 3) * 3: (i % 3 + 1) * 3].flatten()
        if not is_valid_block(block):
            return False
    return True

def main():
    model_files = glob.glob('models\\sudoku_*.h5')
    if model_files:
        print("Existing model(s) found.")
        choice = input("Do you want to load the latest model? (yes/no): ").strip().lower()
        if choice == 'yes':
            latest_model_file = max(model_files, key=os.path.getctime)
            print(f"Loading model from {latest_model_file}")
            model = load_model(latest_model_file)
        else:
            print("Building a new model with hyperparameter tuning.")
            model = hyperparameter_tuning()
    else:
        print("No existing models found. Building a new model with hyperparameter tuning.")
        model = hyperparameter_tuning()

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    os.makedirs('models', exist_ok=True)
    model.save(f'models\\sudoku_{timestamp}.h5')

    puzzles = load_validation_data()
    correct = 0
    total = len(puzzles)
    results = []

    for test_puzzle in puzzles:
        solved_puzzle = solve_sudoku(model, test_puzzle)
        is_valid = valid_solution(solved_puzzle)
        results.append((test_puzzle, is_valid))
        if is_valid:
            correct += 1

    save_validation_results(timestamp, results, correct, total)
    print(f'Validation Accuracy: {correct / total:.2f}')

if __name__ == "__main__":
    db_path = 'data\\training.db'
    print(f"Tables in {db_path}: {list_tables(db_path)}")
    main()

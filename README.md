# Sudoku_Solver
Was just playing around with a more or less automatic and ideally smart Sudoku solver.

## How To Use/Run
1. Clone this repository.
2. Create an environment (say Python 3.11.0) and install requirements via `pip isntall -r requirements.txt`. Activate environment.
3. Skip this step if you have (other) data already, else download the data from the resources listed below. Unpack the .zip files in the folder `raw_data` and create a homogenised dataset by running `python3 create_sqlite_from_raw_data.py`.
4. Run `python3 main.py` and enjoy, I guess.
## Data
Taken training and validation data from the sources listed below. Note the specific licenses that apply to the individual datasets.

### Training Data
- (Unknown license) hard_sudokus_solved: [https://github.com/maxbergmark/sudoku-solver/tree/master/data-sets/hard_sudokus_solved.txt](https://github.com/maxbergmark/sudoku-solver/tree/master/data-sets/hard_sudokus_solved.txt)
- (CC0) sudoku.csv: [https://www.kaggle.com/datasets/rohanrao/sudoku/data](https://www.kaggle.com/datasets/rohanrao/sudoku/data)
- (CC BY-NC-SA 4.0) sudoku_cluewise.csv: [https://www.kaggle.com/datasets/informoney/4-million-sudoku-puzzles-easytohard](https://www.kaggle.com/datasets/informoney/4-million-sudoku-puzzles-easytohard)
- (CC0) sudoku-3m.csv: [https://www.kaggle.com/datasets/radcliffe/3-million-sudoku-puzzles-with-ratings](https://www.kaggle.com/datasets/radcliffe/3-million-sudoku-puzzles-with-ratings)
- (Unknown license) training_puzzles.txt and training_solutions.txt: [https://www.kaggle.com/datasets/alekseykocherzhenko/sudoku](https://www.kaggle.com/datasets/alekseykocherzhenko/sudoku)
- (CC0) archive: [https://www.kaggle.com/rohanrao/sudoku](https://www.kaggle.com/rohanrao/sudoku)

The data `sudoku_cluewise.csv` is licensed under CC BY-NC-SA 4.0 and thus underlies specific licensing requirements. It was uploaded to Kaggle by the author Ryan An, but is hosted on the author's GitHub at [https://github.com/ryeii/SUdokU](https://github.com/ryeii/SUdokU). The data have been loaded from .csv, formatted, and saved into a .db file together with the data above.

### Validation Data
- (Unknown license) unsolved.txt: [https://github.com/maxbergmark/sudoku-solver/tree/master/data-sets/all_17_clue_sudokus.txt](https://github.com/maxbergmark/sudoku-solver/tree/master/data-sets/all_17_clue_sudokus.txt)

### Aggregated Data
The aggregated data that went into the training of the algorithm can be found in the subfolder `data` as .db files. Please note the license specifications for the individual datasets specified above. The aggregated data inherits the most restrictive license, which in this case is the CC BY-NC-SA 4.0 license.

## Licensing Information

### Data Licensing
The data in this repository is licensed under the Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) license, except where otherwise noted. This license applies because data under the CC BY-SA 4.0 license was used during the aggregation process. You can view a copy of this license at: [https://creativecommons.org/licenses/by-sa/4.0/](https://creativecommons.org/licenses/by-sa/4.0/)

In simple terms, you are free to:

- **Share**: Copy and redistribute the material in any medium or format.
- **Adapt**: Remix, transform, and build upon the material for any purpose, even commercially.

Under the following terms:

- **Attribution**: You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- **ShareAlike**: If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

Please include the following in any distribution of this project's data:

- A copy of the CC BY-SA 4.0 license or a link to it: [https://creativecommons.org/licenses/by-sa/4.0/](https://creativecommons.org/licenses/by-sa/4.0/)
- Attribution to the original authors of the data, if available, in your documentation and, if possible, in the source files.
- Indicate any changes made to the original data, noting the modifications and who made them.
- A link to the original GitHub repository: [https://github.com/Miraculiciously/Sudoku_Solver/](https://github.com/Miraculiciously/Sudoku_Solver/)

#### Specific Data File Licensing

The data file `sudoku_cluewise.csv` is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) license. It was uploaded to Kaggle by the author Ryan An and is hosted on the author's GitHub at [https://github.com/ryeii/SUdokU](https://github.com/ryeii/SUdokU).

In simple terms, you are free to:

- **Share**: Copy and redistribute the material in any medium or format.
- **Adapt**: Remix, transform, and build upon the material.

Under the following terms:

- **Attribution**: You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- **NonCommercial**: You may not use the material for commercial purposes.
- **ShareAlike**: If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

Please include the following in any distribution of this specific data file:

- A copy of the CC BY-NC-SA 4.0 license or a link to it: [https://creativecommons.org/licenses/by-nc-sa/4.0/](https://creativecommons.org/licenses/by-nc-sa/4.0/)
- Attribution to the original author, Ryan An, in your documentation and, if possible, in the source files.
- Indicate any changes made to the original data, noting the modifications and who made them.
- A link to the original GitHub repository: [https://github.com/ryeii/SUdokU](https://github.com/ryeii/SUdokU)

### Code Licensing
The repository's code is licensed under the Apache License 2.0. Please note the specifications in the following licensing information:
Licensed under the Apache License, Version 2.0 (the "License"), you may not use this file except in compliance with the License. You may obtain a copy of the License at: [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

In simple terms, you have to:

- Include a copy of the Apache 2.0 license in any distribution of this project.
- Provide attribution by acknowledging the original authorship (Lukas Schubotz) in your documentation and, if possible, in the source files.
- Include a link to the original GitHub repository: [https://github.com/Miraculiciously/Sudoku_Solver/](https://github.com/Miraculiciously/Sudoku_Solver/)
- Indicate any changes made to the original files, noting the modifications and who made them.

Please do not use the names of the original authors or contributors to endorse or promote your derived products without specific prior written permission.

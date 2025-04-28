```python
# File: data_processor.py

import pandas as pd
from typing import List, Dict

class DataProcessor:
    """
    The DataProcessor class is responsible for processing and analyzing tabular data.
    It provides methods to load data from a CSV file, clean the data, and perform basic statistical analysis.
    """

    def __init__(self, file_path: str):
        """
        Initialize the DataProcessor with a path to the CSV file.

        :param file_path: The path to the CSV file containing the dataset.
        """
        self.file_path = file_path
        self.dataframe = None

    def load_data(self) -> pd.DataFrame:
        """
        Load data from the specified CSV file into a pandas DataFrame.

        :return: A pandas DataFrame containing the loaded data.
        """
        self.dataframe = pd.read_csv(self.file_path)
        return self.dataframe

    def clean_data(self) -> None:
        """
        Clean the loaded data by handling missing values and removing duplicates.

        - Handles missing values by filling them with appropriate defaults.
        - Removes duplicate rows from the DataFrame.
        """
        # Fill missing values with the mean of each column
        self.dataframe.fillna(self.dataframe.mean(), inplace=True)
        # Remove duplicate rows
        self.dataframe.drop_duplicates(inplace=True)

    def calculate_statistics(self) -> Dict[str, float]:
        """
        Calculate basic statistical measures for each numerical column in the DataFrame.

        :return: A dictionary with column names as keys and their corresponding mean values as values.
        """
        statistics = {}
        for column in self.dataframe.select_dtypes(include=['number']).columns:
            statistics[column] = self.dataframe[column].mean()
        return statistics

    def save_cleaned_data(self, output_path: str) -> None:
        """
        Save the cleaned DataFrame to a new CSV file.

        :param output_path: The path where the cleaned data will be saved.
        """
        self.dataframe.to_csv(output_path, index=False)

# Onboarding PDF Summary

1. Overall file purpose:
   - The `data_processor.py` file contains a class `DataProcessor` designed to handle various operations on tabular data stored in CSV files. It supports loading data, cleaning the data by handling missing values and duplicates, calculating basic statistics, and saving the cleaned data.

2. Key functions/methods and their responsibilities:
   - `__init__(self, file_path: str)`: Initializes the DataProcessor with a path to the CSV file.
   - `load_data(self) -> pd.DataFrame`: Loads data from the specified CSV file into a pandas DataFrame.
   - `clean_data(self) -> None`: Cleans the loaded data by filling missing values and removing duplicates.
   - `calculate_statistics(self) -> Dict[str, float]`: Calculates basic statistical measures for each numerical column in the DataFrame.
   - `save_cleaned_data(self, output_path: str) -> None`: Saves the cleaned DataFrame to a new CSV file.

3. Inputs/outputs/side effects:
   - **load_data**: Input is the file path; Output is a pandas DataFrame containing the loaded data.
   - **clean_data**: No inputs/outputs; Side effect is that the DataFrame is modified in place.
   - **calculate_statistics**: No inputs; Output is a dictionary with column names as keys and their corresponding mean values as values.
   - **save_cleaned_data**: Input is the output file path; No outputs; Side effect is that a new CSV file is created.

4. Design patterns, dependencies:
   - The class follows the Single Responsibility Principle (SRP) by focusing on data processing tasks.
   - Dependencies include the `pandas` library for DataFrame operations and Python's built-in `typing` module for type hints.

5. Point out cohesion and coupling:
   - **Cohesion**: High, as all methods are closely related to data processing tasks.
   - **Coupling**: Low, as the class is independent of external systems or complex dependencies beyond the `pandas` library.

```
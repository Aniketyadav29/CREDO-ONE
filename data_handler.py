# src/data_handler.py

import pandas as pd
import os

def create_dummy_data(file_path='loan_data.csv'):
    """
    Creates a dummy CSV file for demonstration purposes if it doesn't exist.
    """
    if not os.path.exists(file_path):
        print(f"Creating a dummy dataset at '{file_path}' for demonstration.")
        data = pd.DataFrame({
            'person_age': [69, 23, 25, 30, 28, 35, 45, 22, 29, 31],
            'person_income': [9600, 45000, 20000, 70000, 55000, 80000, 95000, 30000, 60000, 72000],
            'person_emp_length': [5, 2, 8, 10, 4, 15, 20, 1, 6, 9],
            'loan_amnt': [1000, 5000, 2000, 10000, 8000, 15000, 20000, 2500, 7500, 12000],
            'loan_int_rate': [12.9, 7.5, 14.2, 8.8, 9.5, 6.5, 5.9, 13.5, 10.1, 7.8],
            'loan_percent_income': [0.10, 0.11, 0.10, 0.14, 0.15, 0.18, 0.21, 0.08, 0.12, 0.16],
            'person_home_ownership': ['RENT', 'MORTGAGE', 'OWN', 'RENT', 'MORTGAGE', 'MORTGAGE', 'OWN', 'RENT', 'MORTGAGE', 'OWN'],
            'loan_intent': ['EDUCATION', 'MEDICAL', 'DEBTCONSOLIDATION', 'HOMEIMPROVEMENT', 'PERSONAL', 'VENTURE', 'MEDICAL', 'EDUCATION', 'PERSONAL', 'DEBTCONSOLIDATION'],
            'loan_status': [0, 0, 1, 0, 1, 0, 0, 1, 0, 1]
        })
        data.to_csv(file_path, index=False)
    else:
        print(f"The file '{file_path}' already exists.")

def load_data(file_path):
    """
    Loads data from a CSV file.
    """
    try:
        data = pd.read_csv(file_path)
        print(f"Data loaded successfully from '{file_path}'.")
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")

        return None

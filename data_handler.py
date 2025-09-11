import pandas as pd
import os
def create_dummy_data(file_path):
    """
    Creates a dummy Excel file at the specified path.
    """
    print(f"Creating a dummy dataset at '{file_path}' for demonstration.")
    data = pd.DataFrame({
        'person_age': [21, 23, 25, 30, 28, 35, 45, 22, 29, 31,
                       24, 32, 26, 38, 40, 27, 33, 42, 29, 34],
        'person_income': [9600, 45000, 20000, 70000, 55000, 80000, 95000, 30000, 60000, 72000,
                          35000, 65000, 42000, 85000, 100000, 50000, 75000, 92000, 58000, 78000],
        'person_emp_length': [5, 2, 8, 10, 4, 15, 20, 1, 6, 9,
                              3, 7, 5, 12, 18, 2, 8, 16, 4, 10],
        'loan_amnt': [1000, 5000, 2000, 10000, 8000, 15000, 20000, 2500, 7500, 12000,
                      3000, 6000, 4000, 11000, 18000, 3500, 9000, 15000, 6500, 13000],
        'loan_int_rate': [12.9, 7.5, 14.2, 8.8, 9.5, 6.5, 5.9, 13.5, 10.1, 7.8,
                          11.5, 8.1, 13.9, 7.2, 6.1, 12.8, 9.2, 6.8, 10.5, 8.5],
        'loan_percent_income': [0.10, 0.11, 0.10, 0.14, 0.15, 0.18, 0.21, 0.08, 0.12, 0.16,
                                0.09, 0.13, 0.10, 0.13, 0.18, 0.07, 0.12, 0.16, 0.11, 0.17],
        'person_home_ownership': ['RENT', 'MORTGAGE', 'OWN', 'RENT', 'MORTGAGE', 'MORTGAGE', 'OWN', 'RENT', 'MORTGAGE', 'OWN',
                                  'RENT', 'OWN', 'RENT', 'MORTGAGE', 'OWN', 'RENT', 'MORTGAGE', 'OWN', 'RENT', 'MORTGAGE'],
        'loan_intent': ['EDUCATION', 'MEDICAL', 'DEBTCONSOLIDATION', 'HOMEIMPROVEMENT', 'PERSONAL', 'VENTURE', 'MEDICAL', 'EDUCATION', 'PERSONAL', 'DEBTCONSOLIDATION',
                        'EDUCATION', 'MEDICAL', 'DEBTCONSOLIDATION', 'HOMEIMPROVEMENT', 'VENTURE', 'PERSONAL', 'EDUCATION', 'MEDICAL', 'PERSONAL', 'DEBTCONSOLIDATION'],
        'loan_status': [0, 0, 1, 0, 1, 0, 0, 1, 0, 1,
                        1, 0, 1, 0, 0, 1, 0, 0, 1, 0]
    })
    data.to_excel(file_path, index=False)
def load_data(file_path):
    """
    Loads data from an Excel file at the specified path.
    """
    try:
        # Changed from pd.read_csv to pd.read_excel
        data = pd.read_excel(file_path)
        print(f"Data loaded successfully from '{file_path}'.")
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None



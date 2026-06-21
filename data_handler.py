<<<<<<< HEAD
import pandas as pd
import numpy as np
import os

def create_dummy_data(file_path):
    """
    Creates a robust dummy Excel file with 100 entries to provide 
    a more realistic training and evaluation environment.
    """
    print(f"Creating an updated dummy dataset at '{file_path}' for demonstration.")
    
    # Set seed for reproducibility
    np.random.seed(42)
    rows = 100

    # Generate diverse features
    data = pd.DataFrame({
        'person_age': np.random.randint(20, 65, rows),
        'person_income': np.random.randint(8000, 150000, rows),
        'person_emp_length': np.random.randint(0, 30, rows),
        'loan_amnt': np.random.randint(1000, 35000, rows),
        'loan_int_rate': np.random.uniform(5.5, 22.0, rows).round(1),
        'person_home_ownership': np.random.choice(['RENT', 'MORTGAGE', 'OWN', 'OTHER'], rows),
        'loan_intent': np.random.choice(['EDUCATION', 'MEDICAL', 'PERSONAL', 'VENTURE', 'HOMEIMPROVEMENT', 'DEBTCONSOLIDATION'], rows),
        'repayment_history': np.random.choice(['good', 'fair', 'poor'], rows, p=[0.6, 0.25, 0.15]),
        'loan_purpose_category': np.random.choice(['productive_asset', 'emergency_need', 'consumption', 'debt_restructuring'], rows)
    })

    # Calculate loan_percent_income dynamically
    data['loan_percent_income'] = (data['loan_amnt'] / data['person_income']).round(2)

    # Risk Logic for loan_status (0 = No Default, 1 = Default)
    # A loan is marked as a default (1) if it meets high-risk criteria:
    # 1. Repayment history is 'poor'
    # 2. OR Loan is more than 40% of their income
    # 3. OR Interest rate is very high (> 18%) AND history isn't 'good'
    
    def determine_status(row):
        if row['repayment_history'] == 'poor':
            return 1
        if row['loan_percent_income'] > 0.40:
            return 1
        if row['loan_int_rate'] > 18.0 and row['repayment_history'] != 'good':
            return 1
        return 0

    data['loan_status'] = data.apply(determine_status, axis=1)

    # Save to Excel
    data.to_excel(file_path, index=False)
    print(f"Successfully generated {rows} rows of data. ✅")

def load_data(file_path):
    """
    Loads data from an Excel file using pandas.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    return pd.read_excel(file_path)
=======
import pandas as pd
import numpy as np
import os

def create_dummy_data(file_path):
    """
    Creates a robust dummy Excel file with 100 entries to provide 
    a more realistic training and evaluation environment.
    """
    print(f"Creating an updated dummy dataset at '{file_path}' for demonstration.")
    
    # Set seed for reproducibility
    np.random.seed(42)
    rows = 100

    # Generate diverse features
    data = pd.DataFrame({
        'person_age': np.random.randint(20, 65, rows),
        'person_income': np.random.randint(8000, 150000, rows),
        'person_emp_length': np.random.randint(0, 30, rows),
        'loan_amnt': np.random.randint(1000, 35000, rows),
        'loan_int_rate': np.random.uniform(5.5, 22.0, rows).round(1),
        'person_home_ownership': np.random.choice(['RENT', 'MORTGAGE', 'OWN', 'OTHER'], rows),
        'loan_intent': np.random.choice(['EDUCATION', 'MEDICAL', 'PERSONAL', 'VENTURE', 'HOMEIMPROVEMENT', 'DEBTCONSOLIDATION'], rows),
        'repayment_history': np.random.choice(['good', 'fair', 'poor'], rows, p=[0.6, 0.25, 0.15]),
        'loan_purpose_category': np.random.choice(['productive_asset', 'emergency_need', 'consumption', 'debt_restructuring'], rows)
    })

    # Calculate loan_percent_income dynamically
    data['loan_percent_income'] = (data['loan_amnt'] / data['person_income']).round(2)

    # Risk Logic for loan_status (0 = No Default, 1 = Default)
    # A loan is marked as a default (1) if it meets high-risk criteria:
    # 1. Repayment history is 'poor'
    # 2. OR Loan is more than 40% of their income
    # 3. OR Interest rate is very high (> 18%) AND history isn't 'good'
    
    def determine_status(row):
        if row['repayment_history'] == 'poor':
            return 1
        if row['loan_percent_income'] > 0.40:
            return 1
        if row['loan_int_rate'] > 18.0 and row['repayment_history'] != 'good':
            return 1
        return 0

    data['loan_status'] = data.apply(determine_status, axis=1)

    # Save to Excel
    data.to_excel(file_path, index=False)
    print(f"Successfully generated {rows} rows of data. ✅")

def load_data(file_path):
    """
    Loads data from an Excel file using pandas.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    return pd.read_excel(file_path)
>>>>>>> 8273da24b4ade75a28f8545701373e507a4bedbb

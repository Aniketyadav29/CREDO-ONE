# main.py

import pandas as pd
from data_handler import create_dummy_data, load_data
from preprocessor import create_preprocessor
from model import train_model, evaluate_model

def main():
    """
    Main function to run the AI-driven microfinance loan risk prediction project.
    """
    # 1. Setup and Data Loading
    print("### Step 1: Loading Data ###")
    create_dummy_data()
    file_path = 'loan_data.csv'
    data = load_data(file_path)
    
    if data is None:
        return

    X = data.drop('loan_status', axis=1)
    y = data['loan_status']
    print("\nData splitting complete.")

    # 2. Data Preprocessing
    print("\n### Step 2: Preprocessing Data ###")
    preprocessor = create_preprocessor()
    print("Preprocessing pipeline created.")

    # 3. Model Training
    print("\n### Step 3: Training the Model ###")
    model_pipeline, X_test, y_test = train_model(preprocessor, X, y)

    # 4. Model Evaluation
    print("\n### Step 4: Model Evaluation ###")
    evaluate_model(model_pipeline, X_test, y_test)


if __name__ == "__main__":
    main()
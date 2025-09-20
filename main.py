import pandas as pd
import os
import tempfile
import asyncio
import json
from data_handler import create_dummy_data, load_data
from preprocessor import create_preprocessor
from model import train_model, evaluate_model, predict_with_gemini
from data_utils import get_random_applicant
from Config import loan_data

def check_for_duplicates(new_data):
    """
    Checks if a new data dictionary already exists in the loan_data list.
    """
    # Create a simple hash or string representation of the new data for comparison
    new_data_tuple = tuple(new_data.items())
    
    for entry in loan_data:
        entry_tuple = tuple(entry.items())
        if new_data_tuple == entry_tuple:
            return True  # A duplicate was found
    return False # No duplicate found

def append_to_config(new_data):
    """
    Appends a new data dictionary to the loan_data list in Config.py.
    """
    if check_for_duplicates(new_data):
        print("\nThis dataset already exists in Config.py. Not appending. 🚫")
        return

    try:
        # Get the full path to Config.py
        config_path = os.path.join(os.path.dirname(__file__), 'Config.py')

        # Load the existing file content
        with open(config_path, 'r') as f:
            lines = f.readlines()

        # Find the line with the list definition
        start_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('loan_data = ['):
                start_index = i
                break
        
        if start_index == -1:
            print("\nError: Could not find 'loan_data = [' in Config.py. Please check the file format.")
            return

        # Prepare the content for the new entry
        new_entry_str = f"    {json.dumps(new_data, indent=4)},\n"

        # Find the end of the list and insert the new data
        end_index = len(lines) - 1
        while end_index > start_index and lines[end_index].strip() != ']':
            end_index -= 1
        
        lines.insert(end_index, new_entry_str)

        # Write the updated content back to the file
        with open(config_path, 'w') as f:
            f.writelines(lines)

        print("\nManually entered data has been added to Config.py. ✅")

    except Exception as e:
        print(f"\nError: Could not append data to Config.py. Reason: {e}")

async def main():
    """
    Main function to run the AI-driven microfinance loan risk prediction project.
    """
    # Create a temporary file that is automatically cleaned up
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as temp_file:
        file_path = temp_file.name

    try:
        # 1. Setup and Data Loading
        print("### Step 1: Loading Data ###")
        print(f"Creating a temporary Excel file at: '{file_path}'")
        create_dummy_data(file_path)
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

        # 5. AI-Powered Prediction for a New Applicant
        print("\n### Step 5: Making an AI-Powered Prediction ###")

        choice = input("\nEnter 'M' for manual data entry or 'R' for a random dataset from the file: ").strip().upper()

        if choice == 'M':
            print("\nPlease enter the details for the new loan applicant:")
            try:
                person_age = int(input("Person Age: "))
                person_income = int(input("Person Income: "))
                person_emp_length = int(input("Person Employment Length (in years): "))
                loan_amnt = int(input("Loan Amount: "))
                loan_int_rate = float(input("Loan Interest Rate: "))
                loan_percent_income = float(input("Loan Percent of Income: "))
                person_home_ownership = input("Person Home Ownership (RENT, MORTGAGE, or OWN): ").upper()
                loan_intent = input("Loan Intent (EDUCATION, MEDICAL, DEBTCONSOLIDATION, HOMEIMPROVEMENT, PERSONAL, or VENTURE): ").upper()
                repayment_history = input("Repayment History (good, fair, or poor): ").lower()
                loan_purpose_category = input("Loan Purpose Category (productive_asset, emergency_need, consumption, or debt_restructuring): ").lower()
                loan_status_input = int(input("Loan Status (0 for low risk, 1 for high risk): "))

                new_applicant_data = {
                    'person_age': person_age,
                    'person_income': person_income,
                    'person_emp_length': person_emp_length,
                    'loan_amnt': loan_amnt,
                    'loan_int_rate': loan_int_rate,
                    'loan_percent_income': loan_percent_income,
                    'person_home_ownership': person_home_ownership,
                    'loan_intent': loan_intent,
                    'repayment_history': repayment_history,
                    'loan_purpose_category': loan_purpose_category,
                    'loan_status': loan_status_input
                }

                append_to_config(new_applicant_data)
                
                prediction_data = new_applicant_data.copy()
                del prediction_data['loan_status']

            except ValueError:
                print("Invalid input. Please ensure numerical values are entered correctly.")
                return
        elif choice == 'R':
            new_applicant_data = get_random_applicant()
            original_loan_status = new_applicant_data.pop('loan_status', None)
            print("\nRandomly selected applicant data:")
            print(new_applicant_data)
            print(f"Actual Loan Status: {original_loan_status}")
            prediction_data = new_applicant_data
        else:
            print("Invalid choice. Please run the program again and select 'M' or 'R'.")
            return

        prediction = await predict_with_gemini(prediction_data)
        
        prediction_map = {0: "No", 1: "Yes"}
        predicted_risk = prediction_map.get(prediction['prediction'], 'Unknown')

        print("\nAI Prediction Result:")
        print(f"Predicted Default Risk: {predicted_risk}")
        if choice == 'R':
            print(f"Actual Loan Status: {prediction_map.get(original_loan_status, 'Unknown')}")
        
        print(f"Reason Summary: {prediction['reason']['summary']}")
        print(f"Reason Detailed Breakdown: {prediction['reason']['detailed_breakdown']}".replace('$', '₹'))
        print(f"Overall Conclusion: {prediction['overall_conclusion']}")
        print("\n" + "="*50 + "\n")
                
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"\nTemporary file '{file_path}' has been deleted. ✅")

if __name__ == "__main__":
    asyncio.run(main())

import pandas as pd
import os
import tempfile
import asyncio
from data_handler import create_dummy_data, load_data
from preprocessor import create_preprocessor
from model import train_model, evaluate_model, predict_with_gemini

async def main():
    """
    Main function to run the AI-driven microfinance loan risk prediction project.
    All chatbot and voice assistant functionality has been removed.
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
        new_applicant_data = {
            'person_age': 32,
            'person_income': 500000,
            'person_emp_length': 5,
            'loan_amnt': 100000,
            'loan_int_rate': 12.0,
            'loan_percent_income': 0.25,
            'person_home_ownership': 'RENT',
            'loan_intent': 'PERSONAL'
        }
        
        prediction = await predict_with_gemini(new_applicant_data)
        
        # Map the prediction result from 0/1 to Yes/No
        prediction_map = {0: "No", 1: "Yes"}
        predicted_risk = prediction_map.get(prediction['prediction'], 'Unknown')

        print("\nAI Prediction Result:")
        print(f"Prediction: {predicted_risk}")
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

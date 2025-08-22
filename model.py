import xgboost as xgb
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import pandas as pd
import json
import aiohttp

def train_model(preprocessor, X, y):
    """
    Trains and returns an XGBoost classification model.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Removed the now-obsolete 'use_label_encoder' parameter
    model_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                     ('classifier', xgb.XGBClassifier(eval_metric='logloss'))])
    
    print("\nTraining the XGBoost model...")
    model_pipeline.fit(X_train, y_train)
    print("Model training complete. ✅")
    
    return model_pipeline, X_test, y_test

def evaluate_model(model, X_test, y_test):
    """
    Evaluates the trained model on the test data and prints the results.
    """
    y_pred = model.predict(X_test)
    
    print("\n### Model Evaluation ###")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    
    print("\nClassification Report:")
    # Using zero_division to handle cases with no predicted samples
    print(classification_report(y_test, y_pred, zero_division=0))
    
    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:")
    print(cm)
    
    print("\nFinal Results:")
    print("True Negatives (TN):", cm[0, 0])
    print("False Positives (FP):", cm[0, 1])
    print("False Negatives (FN):", cm[1, 0])
    print("True Positives (TP):", cm[1, 1])

async def predict_with_gemini(data_point):
    """
    Uses the Gemini API to predict loan risk for a new data point.
    """
    print("\n### Step 5: AI-Powered Loan Risk Prediction ###")
    
    # Create a detailed prompt for the AI
    prompt = f"""
    You are an AI assistant specialized in microfinance loan risk assessment. 
    Analyze the following loan applicant's data and predict the loan status. 
    A loan status of 0 means the loan is likely to be repaid (low risk), and 1 means the loan is at high risk of default.
    Provide your prediction as a JSON object with the following keys. All string values should be in English.
    - "prediction": The predicted loan status (0 or 1).
    - "reason": An object with the following sub-keys:
        - "summary": A short, simplified sentence explaining the prediction.
        - "detailed_breakdown": A more in-depth explanation of the key factors that led to the prediction, referencing the provided data points.
    - "overall_conclusion": A concise, simplified summary of the final recommendation based on the data.

    Loan Applicant Data:
    - Person Age: {data_point['person_age']}
    - Person Income: {data_point['person_income']}
    - Person Employment Length: {data_point['person_emp_length']}
    - Loan Amount: {data_point['loan_amnt']}
    - Loan Interest Rate: {data_point['loan_int_rate']}
    - Loan Percent of Income: {data_point['loan_percent_income']}
    - Person Home Ownership: {data_point['person_home_ownership']}
    - Loan Intent: {data_point['loan_intent']}
    """
    
    # Define the API call payload with a new JSON schema for structured output
    chatHistory = []
    chatHistory.append({ "role": "user", "parts": [{ "text": prompt }] })
    
    payload = {
        "contents": chatHistory,
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "prediction": { "type": "NUMBER" },
                    "reason": {
                        "type": "OBJECT",
                        "properties": {
                            "summary": { "type": "STRING" },
                            "detailed_breakdown": { "type": "STRING" }
                        }
                    },
                    "overall_conclusion": { "type": "STRING" }
                }
            }
        }
    }


    apiKey = "AIzaSyA5I9uRJux8WIBAV0qPWI-9hTjmEwh00dE"
    apiUrl = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={apiKey}"
    
    # Use aiohttp for the asynchronous request
    async with aiohttp.ClientSession() as session:
        try:
            # Use json.dumps to serialize the payload
            async with session.post(apiUrl, headers={'Content-Type': 'application/json'}, data=json.dumps(payload)) as response:
                result = await response.json()

                if response.status == 200 and result.get('candidates'):
                    json_text = result['candidates'][0]['content']['parts'][0]['text']
                    prediction_result = json.loads(json_text)
                    return prediction_result
                else:
                    return { 
                        "prediction": -1, 
                        "reason": { "summary": "API Error", "detailed_breakdown": f"API Error: {result.get('error', {}).get('message', 'Unknown error')}" },
                        "overall_conclusion": "The API call failed, so no conclusion can be made."
                    }
        except Exception as e:
            return { 
                "prediction": -1, 
                "reason": { "summary": "An error occurred", "detailed_breakdown": f"An error occurred: {e}" },
                "overall_conclusion": "The API call failed, so no conclusion can be made."
            }

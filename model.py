import xgboost as xgb
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import pandas as pd
import json
import aiohttp
import asyncio
import re

def train_model(preprocessor, X, y):
    """
    Trains and returns an XGBoost classification model using a stratified split.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', xgb.XGBClassifier(eval_metric='logloss', random_state=42))
    ])
    
    print("\nTraining the XGBoost model...")
    model_pipeline.fit(X_train, y_train)
    print("Model training complete. ✅")
    
    return model_pipeline, X_test, y_test

def evaluate_model(model, X_test, y_test):
    """
    Evaluates the trained model on test data and prints detailed metrics.
    """
    y_pred = model.predict(X_test)
    
    print("\n### Model Evaluation ###")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (cm[0, 0], 0, 0, 0)
    print(f"\nFinal Results:\nTrue Negatives: {tn}\nFalse Positives: {fp}\nFalse Negatives: {fn}\nTrue Positives: {tp}")

async def predict_with_gemini(data_point, language='en'):
    """
    Predicts loan risk using the Gemini API with retry logic for 429 errors.
    """
    prompt = f"""
    Analyze this microfinance loan applicant data and predict default risk (1 for default, 0 for safe).
    Data: {json.dumps(data_point)}
    
    Return ONLY a JSON object with this structure:
    {{
        "prediction": 0,
        "reason": {{
            "summary": "text",
            "detailed_breakdown": "text"
        }},
        "overall_conclusion": "text"
    }}
    """

    # REST API payload for v1beta generateContent
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }

    # UPDATED API Configuration for 2026 standards
    apiKey = "AIzaSyBfz1SeEgx4pNxr5dp14Vv2pEQtS7167jg"
    # gemini-2.5-flash is the currently supported stable model for January 2026
    apiUrl = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={apiKey}"
    
    async with aiohttp.ClientSession() as session:
        # Loop for handling Rate Limits (Error 429)
        for attempt in range(3):
            try:
                async with session.post(apiUrl, json=payload) as response:
                    result = await response.json()

                    if response.status == 200 and 'candidates' in result:
                        raw_text = result['candidates'][0]['content']['parts'][0]['text']
                        # Remove markdown formatting blocks if the model includes them
                        clean_json = re.sub(r'```json\s*|\s*```', '', raw_text).strip()
                        return json.loads(clean_json)
                    
                    elif response.status == 429:
                        wait_time = (attempt + 1) * 30 
                        print(f"Quota exceeded (429). Waiting {wait_time} seconds before retry {attempt + 1}/3...")
                        await asyncio.sleep(wait_time)
                    else:
                        error_msg = result.get('error', {}).get('message', 'Unknown Error')
                        return { 
                            "prediction": -1, 
                            "reason": { "summary": f"Error {response.status}", "detailed_breakdown": error_msg },
                            "overall_conclusion": "The API call failed."
                        }
            except Exception as e:
                return { 
                    "prediction": -1, 
                    "reason": { "summary": "Connection Error", "detailed_breakdown": str(e) },
                    "overall_conclusion": "Failed to connect to AI Studio."
                }
    
    return { "prediction": -1, "reason": { "summary": "Exhausted Retries", "detailed_breakdown": "Daily quota limit reached." }, "overall_conclusion": "Try again tomorrow." }

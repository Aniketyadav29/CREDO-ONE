# src/model.py

import xgboost as xgb
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import pandas as pd

def train_model(preprocessor, X, y):
    """
    Trains and returns an XGBoost classification model.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    model_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                     ('classifier', xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss'))])
    
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
    print(classification_report(y_test, y_pred))
    
    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:")
    print(cm)
    
    print("\nFinal Results:")
    print("True Negatives (TN):", cm[0, 0])
    print("False Positives (FP):", cm[0, 1])
    print("False Negatives (FN):", cm[1, 0])
    print("True Positives (TP):", cm[1, 1])
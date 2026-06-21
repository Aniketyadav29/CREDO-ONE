import xgboost as xgb
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import pandas as pd
import json
import aiohttp
import asyncio
import re
import os
import time
import uuid
from typing import Dict, List, Tuple
from Config import GEMINI_API_KEY, GEMINI_MODEL, MODEL_VERSION, get_risk_band, ENABLE_FAIRNESS_CHECKS


def generate_request_id():
    """Generate a unique request ID"""
    return str(uuid.uuid4())


def _safe_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalize_ratio(value) -> float:
    ratio = _safe_float(value, 0.0)
    if ratio > 1:
        ratio = ratio / 100.0
    return max(0.0, ratio)


def _loan_to_income_ratio(data_point: Dict) -> float:
    provided_ratio = _normalize_ratio(data_point.get('loan_percent_income', 0))
    income = _safe_float(data_point.get('person_income', 0))
    loan_amount = _safe_float(data_point.get('loan_amnt', 0))

    derived_ratio = (loan_amount / income) if income > 0 else 0.0
    derived_ratio = max(0.0, min(derived_ratio, 1.0))

    return max(provided_ratio, derived_ratio)


def _is_default_flag(value) -> bool:
    return str(value).strip().lower() in {'1', 'true', 'yes', 'default', 'defaulted'}


def _build_rule_based_decision(data_point: Dict) -> Dict:
    factors = calculate_decision_factors(data_point)
    prediction = 1 if factors['total_score'] >= 45 else 0
    confidence = calculate_confidence(factors)
    risk_band = get_risk_band(factors['total_score'])
    lti_ratio = _loan_to_income_ratio(data_point)
    repayment = str(data_point.get('repayment_history', 'good') or 'good').lower()
    loan_status = 'defaulted' if _is_default_flag(data_point.get('loan_status', 0)) else 'clear'

    decision_factors = [
        {'factor': 'Repayment History', 'impact': 'negative' if factors['repayment_history'] else 'positive', 'value': factors['repayment_history']},
        {'factor': 'Loan-to-Income', 'impact': 'negative' if factors['lti_ratio'] else 'positive', 'value': factors['lti_ratio']},
        {'factor': 'Interest Rate', 'impact': 'negative' if factors['interest_rate'] else 'positive', 'value': factors['interest_rate']},
        {'factor': 'Employment Stability', 'impact': 'negative' if factors['employment_stability'] else 'positive', 'value': factors['employment_stability']},
        {'factor': 'Age Segment', 'impact': 'negative' if factors['age_segment'] else 'positive', 'value': factors['age_segment']},
    ]

    positive_factors = [item for item in decision_factors if item['impact'] == 'positive' and item['value'] > 0]
    negative_factors = [item for item in decision_factors if item['impact'] == 'negative' and item['value'] > 0]

    source_summary = (
        "Rule-based guardrail engine reviewed repayment history, loan burden, interest burden, employment stability, and age profile, then aligned the final response with the model output."
    )
    summary = (
        "Reject recommendation because repayment history is adverse and the loan burden is too heavy for the applicant profile."
        if prediction == 1
        else "Approve recommendation because the applicant profile remains steady and no major risk signal dominates the decision."
    )
    breakdown = (
        f"Repayment history is {repayment}, which signals {'high' if factors['repayment_history'] else 'low'} credit concern. "
        f"Loan-to-income burden is {'extreme' if factors['lti_ratio'] >= 40 else 'high' if factors['lti_ratio'] >= 30 else 'moderate' if factors['lti_ratio'] >= 15 else 'manageable'}. "
        f"Interest rate is {'elevated' if factors['interest_rate'] >= 15 else 'above average' if factors['interest_rate'] >= 8 else 'favorable'}. "
        f"Employment stability is {'weak' if factors['employment_stability'] else 'stable enough'} and age is {'younger-risk' if factors['age_segment'] else 'neutral or mature'}. "
        f"Loan status is {loan_status}, which is {'an added warning sign' if loan_status == 'defaulted' else 'not a warning sign'}."
    )

    if prediction == 1:
        conclusion = (
            "Rejected because the borrower shows a strong repayment concern and a loan burden that is too heavy relative to the profile."
        )
    else:
        conclusion = (
            "Approved because the borrower profile is steady and the reviewed parameters do not create a dominant risk concern."
        )

    return {
        'prediction': prediction,
        'confidence': confidence,
        'risk_score': factors['total_score'],
        'risk_band': risk_band,
        'decision_factors': positive_factors + negative_factors,
        'positive_factors': positive_factors,
        'negative_factors': negative_factors,
        'reason': {
            'source': source_summary,
            'summary': summary,
            'detailed_breakdown': breakdown,
            'risk_band': risk_band,
        },
        'overall_conclusion': conclusion,
    }
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


def fallback_risk_assessment(data_point, request_id: str = None, risk_score: float = None,
                             confidence: float = None, risk_band: str = None):
    """
    Local fallback decision when Gemini is temporarily unavailable.
    Returns the same schema used by the UI with rich decision data.
    """
    if not request_id:
        request_id = generate_request_id()

    factors = calculate_decision_factors(data_point)

    if risk_score is None:
        risk_score = factors['total_score']

    if confidence is None:
        confidence = calculate_confidence(factors)

    if risk_band is None:
        risk_band = get_risk_band(risk_score)

    interest_rate = _safe_float(data_point.get('loan_int_rate', 0))
    loan_percent_income = _loan_to_income_ratio(data_point)
    emp_length = _safe_float(data_point.get('person_emp_length', 0))
    age = _safe_float(data_point.get('person_age', 0))
    repayment = str(data_point.get('repayment_history', 'good') or 'good').lower()
    loan_status = data_point.get('loan_status', 0)

    risk_contributors = []
    positive_factors = []
    negative_factors = []

    if repayment in ('poor', 'defaulted'):
        neg_factor = {'factor': 'Poor Repayment History', 'impact': 'negative', 'value': 45}
        negative_factors.append(neg_factor)
        risk_contributors.append('poor repayment history indicates elevated default risk')
    elif repayment in ('average', 'fair'):
        neg_factor = {'factor': 'Fair Repayment History', 'impact': 'negative', 'value': 20}
        negative_factors.append(neg_factor)
        risk_contributors.append('repayment history is moderate and needs monitoring')
    else:
        pos_factor = {'factor': 'Excellent Repayment History', 'impact': 'positive', 'value': 15}
        positive_factors.append(pos_factor)
        risk_contributors.append('repayment history is stable')

    if loan_percent_income > 0.75:
        neg_factor = {'factor': 'Extreme Loan-to-Income Ratio', 'impact': 'negative', 'value': 40}
        negative_factors.append(neg_factor)
        risk_contributors.append('loan amount is far above the applicant income')
    elif loan_percent_income > 0.40:
        neg_factor = {'factor': 'High Loan-to-Income Ratio', 'impact': 'negative', 'value': 30}
        negative_factors.append(neg_factor)
        risk_contributors.append('loan-to-income ratio is high')
    elif loan_percent_income > 0.25:
        neg_factor = {'factor': 'Moderate LTI Ratio', 'impact': 'negative', 'value': 15}
        negative_factors.append(neg_factor)
        risk_contributors.append('loan-to-income ratio is moderately high')
    else:
        pos_factor = {'factor': 'Healthy Loan-to-Income', 'impact': 'positive', 'value': 10}
        positive_factors.append(pos_factor)

    if _is_default_flag(loan_status):
        neg_factor = {'factor': 'Prior Default Flag', 'impact': 'negative', 'value': 35}
        negative_factors.append(neg_factor)
        risk_contributors.append('historical default flag indicates elevated credit risk')

    if interest_rate > 18:
        neg_factor = {'factor': 'High Interest Rate', 'impact': 'negative', 'value': 15}
        negative_factors.append(neg_factor)
        risk_contributors.append('interest burden is high')
    elif interest_rate > 13:
        neg_factor = {'factor': 'Above-Average Rate', 'impact': 'negative', 'value': 8}
        negative_factors.append(neg_factor)
        risk_contributors.append('interest burden is above average')
    else:
        pos_factor = {'factor': 'Favorable Interest Rate', 'impact': 'positive', 'value': 5}
        positive_factors.append(pos_factor)

    if emp_length < 2:
        neg_factor = {'factor': 'Limited Employment', 'impact': 'negative', 'value': 8}
        negative_factors.append(neg_factor)
        risk_contributors.append('employment stability is limited')
    elif emp_length >= 5:
        pos_factor = {'factor': 'Stable Employment', 'impact': 'positive', 'value': 8}
        positive_factors.append(pos_factor)

    if age < 21:
        neg_factor = {'factor': 'Younger Age Segment', 'impact': 'negative', 'value': 5}
        negative_factors.append(neg_factor)
        risk_contributors.append('borrower age is in higher-risk bracket')
    elif age >= 35:
        pos_factor = {'factor': 'Mature Applicant', 'impact': 'positive', 'value': 5}
        positive_factors.append(pos_factor)

    prediction = 1 if risk_score >= 45 else 0

    top_positive = sorted(positive_factors, key=lambda x: x['value'], reverse=True)[:3]
    top_negative = sorted(negative_factors, key=lambda x: x['value'], reverse=True)[:3]

    return {
        "prediction": prediction,
        "confidence": confidence,
        "risk_score": risk_score,
        "risk_band": risk_band,
        "model_version": MODEL_VERSION,
        "decision_source": "local_fallback",
        "reason": {
            "source": "Local fallback engine reviewed the same borrower parameters and produced a consistent decision.",
            "summary": "Decision generated locally because Gemini is unavailable.",
            "detailed_breakdown": (
                f"Positive drivers: {', '.join([item['factor'] for item in top_positive]) or 'none'}. "
                f"Negative drivers: {', '.join([item['factor'] for item in top_negative]) or 'none'}. "
                f"Key notes: {', '.join(risk_contributors) or 'no additional notes'}."
            )
        },
        "decision_factors": top_positive + top_negative,
        "positive_factors": top_positive,
        "negative_factors": [f for f in negative_factors if f not in top_negative][:3],
        "overall_conclusion": (
            "Application is REJECTED because the reviewed parameters indicate elevated risk."
            if prediction == 1
            else "Application is APPROVED because the reviewed parameters remain within acceptable bounds."
        )
    }


def calculate_decision_factors(data_point: Dict) -> Dict:
    factors = {
        'repayment_history': 0,
        'lti_ratio': 0,
        'interest_rate': 0,
        'employment_stability': 0,
        'age_segment': 0,
        'loan_status': 0,
        'total_score': 0
    }

    repayment = str(data_point.get('repayment_history', 'good')).lower()
    if repayment in ('poor', 'defaulted'):
        factors['repayment_history'] = 45
    elif repayment in ('average', 'fair'):
        factors['repayment_history'] = 20
    else:
        factors['repayment_history'] = 0

    lti = _loan_to_income_ratio(data_point)
    if lti > 0.75:
        factors['lti_ratio'] = 40
    elif lti > 0.40:
        factors['lti_ratio'] = 30
    elif lti > 0.25:
        factors['lti_ratio'] = 15
    else:
        factors['lti_ratio'] = 0

    int_rate = _safe_float(data_point.get('loan_int_rate', 0))
    if int_rate > 18:
        factors['interest_rate'] = 15
    elif int_rate > 13:
        factors['interest_rate'] = 8
    else:
        factors['interest_rate'] = 0

    emp_len = _safe_float(data_point.get('person_emp_length', 0))
    if emp_len < 2:
        factors['employment_stability'] = 8
    else:
        factors['employment_stability'] = 0

    age = _safe_float(data_point.get('person_age', 0))
    if age < 21:
        factors['age_segment'] = 5
    else:
        factors['age_segment'] = 0

    if _is_default_flag(data_point.get('loan_status', 0)):
        factors['loan_status'] = 35

    total = sum([v for k, v in factors.items() if k != 'total_score'])
    factors['total_score'] = min(100, total)
    return factors


def calculate_confidence(factors: Dict) -> float:
    total_score = factors.get('total_score', 0)
    if total_score <= 5 or total_score >= 95:
        return 92
    if total_score <= 20 or total_score >= 80:
        return 85
    if total_score <= 30 or total_score >= 70:
        return 75
    if total_score <= 40 or total_score >= 60:
        return 65
    return 55


async def predict_with_gemini(data_point, language='en', request_id: str = None):
    if not request_id:
        request_id = generate_request_id()

    local_decision = _build_rule_based_decision(data_point)
    risk_score = local_decision['risk_score']
    confidence = local_decision['confidence']
    risk_band = local_decision['risk_band']

    prompt = f"""
    You are a senior credit risk analyst.
    Analyze this microfinance loan applicant and produce a detailed decision.

    Applicant Data:
    {json.dumps(data_point)}

    Baseline Signals:
    - calculated_risk_score: {risk_score}
    - risk_band: {risk_band}
    - confidence_hint: {confidence:.1f}

    Return ONLY valid JSON with this exact structure:
    {{
        "prediction": 0,
        "confidence": 0.85,
        "risk_band": "Low Risk",
        "reason": {{
            "summary": "1-2 sentence plain-language summary",
            "detailed_breakdown": "Detailed explanation covering repayment behavior, income burden, interest burden, and stability indicators"
        }},
        "decision_factors": [
            {{"factor": "Repayment History", "impact": "positive", "value": 15}},
            {{"factor": "Loan-to-Income", "impact": "negative", "value": 30}}
        ],
        "overall_conclusion": "Final recommendation in one sentence"
    }}
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.1,
            "maxOutputTokens": 700
        }
    }

    api_key = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing. Configure .env and restart server.")

    model_candidates = [
        GEMINI_MODEL,
        "gemini-flash-lite-latest",
        "gemini-flash-latest",
        "gemini-2.0-flash",
        "gemini-2.5-flash-lite",
        "gemini-2.5-flash"
    ]
    model_candidates = [m for i, m in enumerate(model_candidates) if m and m not in model_candidates[:i]]

    async with aiohttp.ClientSession() as session:
        for model_name in model_candidates:
            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
            for attempt in range(3):
                try:
                    async with session.post(api_url, json=payload, timeout=aiohttp.ClientTimeout(total=22)) as response:
                        result = await response.json()

                        if response.status == 200 and 'candidates' in result:
                            raw_text = result['candidates'][0]['content']['parts'][0]['text']
                            clean_json = re.sub(r'```json\s*|\s*```', '', raw_text).strip()
                            try:
                                parsed = json.loads(clean_json)
                                raw_prediction = parsed.get('prediction')
                                gemini_prediction = None

                                if isinstance(raw_prediction, (int, float)) and int(raw_prediction) in (0, 1):
                                    gemini_prediction = int(raw_prediction)
                                elif isinstance(raw_prediction, str):
                                    normalized = raw_prediction.strip().lower()
                                    if normalized in ('0', 'approve', 'approved', 'accept', 'accepted'):
                                        gemini_prediction = 0
                                    elif normalized in ('1', 'reject', 'rejected', 'decline', 'declined'):
                                        gemini_prediction = 1

                                if gemini_prediction is None:
                                    gemini_prediction = local_decision['prediction']
                                    decision_source = 'gemini_invalid_prediction_fallback'
                                else:
                                    decision_source = 'gemini_primary_decision'

                                gemini_reason = parsed.get('reason', {}) if isinstance(parsed.get('reason', {}), dict) else {}
                                summary_text = gemini_reason.get('summary', local_decision['reason']['summary'])
                                breakdown_text = gemini_reason.get('detailed_breakdown', local_decision['reason']['detailed_breakdown'])
                                source_text = gemini_reason.get('source', 'Gemini generated this decision from the submitted applicant parameters.')

                                parsed_decision_factors = parsed.get('decision_factors')
                                if not isinstance(parsed_decision_factors, list):
                                    parsed_decision_factors = local_decision['decision_factors']

                                positive_factors = [f for f in parsed_decision_factors if isinstance(f, dict) and str(f.get('impact', '')).lower() == 'positive']
                                negative_factors = [f for f in parsed_decision_factors if isinstance(f, dict) and str(f.get('impact', '')).lower() == 'negative']

                                overall_conclusion = parsed.get('overall_conclusion')
                                if not overall_conclusion:
                                    overall_conclusion = (
                                        'Application is REJECTED based on Gemini analysis of the provided borrower parameters.'
                                        if gemini_prediction == 1
                                        else 'Application is APPROVED based on Gemini analysis of the provided borrower parameters.'
                                    )

                                return {
                                    'prediction': gemini_prediction,
                                    'confidence': parsed.get('confidence', confidence),
                                    'risk_band': parsed.get('risk_band', risk_band),
                                    'risk_score': local_decision['risk_score'],
                                    'decision_factors': parsed_decision_factors,
                                    'positive_factors': positive_factors,
                                    'negative_factors': negative_factors,
                                    'reason': {
                                        'source': source_text,
                                        'summary': summary_text,
                                        'detailed_breakdown': breakdown_text,
                                    },
                                    'overall_conclusion': overall_conclusion,
                                    'decision_source': decision_source,
                                }
                            except json.JSONDecodeError:
                                if attempt < 2:
                                    await asyncio.sleep(1 + attempt)
                                    continue
                                break

                        if response.status == 429:
                            # Switch model quickly when quota/rate-limit is hit.
                            await asyncio.sleep(0.5)
                            break

                        if response.status == 503:
                            if attempt < 2:
                                await asyncio.sleep(2 + attempt * 2)
                                continue
                            break

                        break
                except Exception:
                    if attempt < 2:
                        await asyncio.sleep(1 + attempt)
                        continue
                    break

    raise RuntimeError("Gemini service unavailable after retries. Please try again in a minute.")

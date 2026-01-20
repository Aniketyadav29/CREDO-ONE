
This is my first repository.
<br>
### Developer- Aniket Yadav 
<br>
It's my minor project <h2>"AI Driven Microfinance Loan Risk Prediction"</h2>

# AI-Driven Microfinance Loan Risk Prediction 🏦🤖

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![ML Framework](https://img.shields.io/badge/ML-XGBoost-orange)](https://xgboost.readthedocs.io/)
[![AI Engine](https://img.shields.io/badge/AI-Gemini%20Flash-green)](https://ai.google.dev/)

An advanced, hybrid risk assessment system tailored for microfinance institutions. This project leverages **Gradient Boosting (XGBoost)** for high-precision numerical classification and **Large Language Models (Google Gemini)** to provide human-readable qualitative analysis and financial justification.

## 📖 Overview
Traditional credit scoring often fails in microfinance contexts where data is sparse or non-traditional. This system bridges that gap by:
1.  **Quantitative Analysis**: Processing financial metrics to calculate a strict default probability.
2.  **Qualitative Reasoning**: Using Generative AI to interpret the "story" behind the data—such as the intent of the loan and repayment history—to provide localized financial advice.

---

## 🚀 Key Features

### 1. Hybrid Decision Engine
The system doesn't just give a "Yes" or "No." It runs a two-tier evaluation:
* **Tier 1 (XGBoost)**: A high-performance classifier trained on microfinance-specific features.
* **Tier 2 (Gemini AI)**: An asynchronous API call that analyzes the applicant's profile to explain *why* the risk exists.

### 2. Microfinance Specific Features
Unlike standard loan models, this project tracks:
* [cite_start]`loan_purpose_category`: Productive assets, emergency needs, or debt restructuring[cite: 1].
* [cite_start]`repayment_history`: Granular tracking of past behavior (good, fair, poor)[cite: 1].
* [cite_start]`loan_percent_income`: A critical metric for preventing over-indebtedness in low-income brackets[cite: 1].

### 3. Dynamic Data Persistence
The system includes a manual entry mode that automatically appends new, unique cases to `Config.py`, allowing the local dataset to grow and improve over time.

---

## 🏗️ Technical Architecture

### Data Preprocessing (`preprocessor.py`)
Utilizes a `ColumnTransformer` pipeline:
* **Numerical**: Median imputation and `StandardScaler` normalization.
* **Categorical**: Most-frequent imputation and `OneHotEncoder` for multi-class variables.

### Machine Learning Model (`model.py`)
* **Algorithm**: XGBoost (Extreme Gradient Boosting).
* **Evaluation**: Outputs detailed Confusion Matrices, Accuracy scores, and F1-style Classification Reports.

### AI Integration
* **API**: Google Generative AI (Gemini 2.5 Flash Preview).
* **Format**: Strict JSON schema enforcement to ensure integration with Python logic.

---

## 🛠️ Installation & Setup

1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/YourUsername/Microfinance-Loan-Risk.git](https://github.com/YourUsername/Microfinance-Loan-Risk.git)
    cd Microfinance-Loan-Risk
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requriments.txt
    ```

3.  **Set Up API Key**:
    Open `model.py` and replace the placeholder with your Gemini API Key:
    ```python
    apiKey = "YOUR_GEMINI_API_KEY"
    ```

4.  **Run the System**:
    ```bash
    python main.py
    ```

---

## 📊 Sample Output
```text
AI Prediction Result:
Predicted Default Risk: No
Actual Loan Status: No
Reason Summary: Strong income-to-loan ratio and excellent repayment history.
Reason Detailed Breakdown: The applicant's income of ₹91,000 comfortably covers the ₹14,600 loan. With 14 years of employment and 'good' repayment history, the risk of default is negligible.
Overall Conclusion: Highly recommended for approval for productive asset venture.

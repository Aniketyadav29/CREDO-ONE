
This is my first repository.
<br>
### Developer- Aniket Yadav 
<br>
It's my minor project <h2>"AI Driven Microfinance Loan Risk Prediction"</h2>

# AI-Driven Microfinance Loan Risk Prediction 🏦🤖

A hybrid machine learning and Generative AI system designed to assess loan default risk in microfinance contexts. This project combines the high-speed classification of **XGBoost** with the qualitative reasoning of **Google Gemini AI** to provide both a risk score and a detailed financial justification.

## 🌟 Key Features
- **Hybrid Prediction Engine**: Uses XGBoost for quantitative risk assessment and Gemini 1.5/2.5 Flash for qualitative reasoning.
- **Microfinance-Specific Metrics**: Analyzes niche features like `loan_purpose_category` (e.g., productive assets, emergency needs) and `repayment_history`.
- **AI Explainability**: Generates a "Reason Detailed Breakdown" for every prediction, converting symbols like `$` to `₹` for localized context.
- **Automated Pipeline**: Includes a full data preprocessing suite using Scikit-Learn's `ColumnTransformer` and `Pipeline`.
- **Live CLI Demo**: Interactive command-line interface for testing random applicants or manual data entry.

## 🏗️ Project Architecture
The project is modularized into specialized components:
- `main.py`: The central execution hub and user interface.
- `model.py`: Handles XGBoost training and asynchronous Gemini API integration.
- `preprocessor.py`: Manages data cleaning and feature scaling.
- `data_handler.py`: Generates synthetic datasets for demonstration and testing.
- `Config.py`: Acts as a local persistent database for applicant records.

## 🚀 Live Demo (CLI)
You can run the interactive demo directly in your terminal:

```bash
# Clone the repository
git clone [https://github.com/YourUsername/Microfinance-Loan-Risk.git](https://github.com/YourUsername/Microfinance-Loan-Risk.git)

# Install dependencies
pip install -r requriments.txt

# Run the application
python main.py

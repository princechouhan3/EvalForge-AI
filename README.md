# EvalForge AI — LLM Evaluation & Preference Dataset Platform

**EvalForge AI** is a web-based platform for evaluating AI-generated responses, identifying quality issues, comparing candidate answers, and preparing preference datasets for LLM evaluation and alignment workflows.

## Live Demo

🚀 **Try the application:** https://evalforge-ai-le7rkw94p8gb5vodcjweka.streamlit.app/

## Features

- **AI Response Evaluation:** Evaluate responses for accuracy, relevance, helpfulness, safety, clarity, and overall quality.
- **Side-by-Side Comparison:** Compare Candidate A and Candidate B and identify the preferred response.
- **Error Analysis:** Review response-quality issues, including factual inaccuracies and potential hallucinations.
- **Preference Dataset Preparation:** Organize response preferences for downstream alignment workflows.
- **DPO Dataset Explorer:** Explore preference data prepared for Direct Preference Optimization workflows.
- **Evaluation Reports:** Review evaluation results and quality summaries.
- **Saved Annotations:** Save and inspect manual evaluation records.
- **Dataset Explorer:** Browse prompts, responses, evaluations, and preference examples.

## Tech Stack

- Python
- Streamlit
- Pandas
- Altair
- Google Gemini API
- JSON / JSONL

## How It Works

1. Submit a prompt and candidate responses.
2. Evaluate the responses using the platform's evaluation workflow.
3. Compare quality scores, identified issues, and the preferred answer.
4. Save evaluation records for further analysis.
5. Explore preference datasets and prepare data for downstream LLM alignment experiments.

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/princechouhan3/EvalForge-AI.git
cd EvalForge-AI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create `.streamlit/secrets.toml` and add:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Replace the placeholder with your own API key. Never commit API keys or other secrets to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

## Project Structure

```text
EvalForge-AI/
├── app.py
├── requirements.txt
├── data/
│   ├── raw/
│   ├── evaluated/
│   └── preference/
├── guidelines/
├── reports/
├── scripts/
└── README.md
```

## Learning Outcomes

This project demonstrates practical experience with:

- LLM response evaluation
- AI output quality assessment
- Preference data preparation
- JSONL dataset handling
- Error analysis and evaluation reporting
- Building and deploying an AI-powered web application

## Important Note

This project is an evaluation and preference-dataset preparation platform. The generated evaluation or demonstration datasets do not, by themselves, represent a trained or fine-tuned language model. Dataset quality and AI-generated judgments should be reviewed before use in production or model training.

## Author

**Prince Chouhan**

GitHub: https://github.com/princechouhan3

Portfolio: https://princechouhan3.github.io/prince_portfolio/

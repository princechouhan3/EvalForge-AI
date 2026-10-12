# EvalForge AI | LLM Evaluation & Preference Dataset Platform

## Overview

**EvalForge AI** is an interactive LLM evaluation platform built with Python and Streamlit. It helps users assess AI-generated responses, identify quality and safety issues, compare competing answers, analyze evaluation results, and prepare preference datasets for downstream AI alignment experiments.

The platform combines automated evaluation workflows, structured evaluation data, preference comparisons, and an interactive dashboard in one application.

It is designed as a portfolio project demonstrating practical skills in **LLM evaluation, AI data annotation concepts, dataset validation, error analysis, and preference data preparation**.

## Key Features

- **LLM Response Evaluation** — Evaluate responses across accuracy, relevance, helpfulness, safety, hallucination, clarity, and overall quality.
- **Side-by-Side Comparison** — Compare Candidate A and Candidate B and identify the preferred response.
- **Gemini API Integration** — Use Google's Gemini model for AI-assisted response evaluation.
- **Manual Annotation Workflow** — Save manually reviewed evaluations as structured JSONL records.
- **Error Analysis** — Explore common response-quality issues and evaluation errors.
- **Preference Dataset Generation** — Prepare chosen/rejected response pairs for preference-learning workflows.
- **DPO Dataset Preparation** — Generate structured datasets suitable for experimentation with Direct Preference Optimization pipelines.
- **Dataset Explorer** — Inspect prompts, responses, evaluations, and preference records.
- **Saved Annotations** — Review saved evaluation records.
- **Exportable Results** — Download evaluation results as JSON for further analysis.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application and data processing |
| Streamlit | Interactive web interface |
| Google Gemini API | AI-assisted response evaluation |
| JSON / JSONL | Structured prompts, responses, evaluations, and datasets |
| Pandas | Data analysis and tabular processing |
| Git & GitHub | Version control and project hosting |

## Project Architecture

```text
EvalForge-AI/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   │   ├── prompts.jsonl
│   │   └── responses.jsonl
│   │
│   ├── evaluated/
│   │   ├── evaluations.jsonl
│   │   └── manual_evaluations.jsonl
│   │
│   └── preference/
│       ├── preference_pairs.jsonl
│       └── dpo_dataset.jsonl
│
├── guidelines/
│   └── evaluation_rubric.md
│
├── reports/
│   ├── error_analysis.md
│   ├── evaluation_report.md
│   └── final_quality_report.md
│
└── scripts/
    ├── analyze_evaluations.py
    ├── error_analysis.py
    ├── generate_dpo_dataset.py
    ├── generate_evaluations.py
    ├── generate_final_report.py
    ├── generate_preferences.py
    ├── generate_prompts.py
    ├── generate_responses.py
    └── validate_dataset.py
```

*Note: This structure describes the main project files. Exact file availability may depend on the current repository version.*

## Evaluation Criteria

EvalForge AI uses a structured rubric to assess response quality:

| Criterion | What It Measures |
|---|---|
| Accuracy | Whether the response is factually correct |
| Relevance | Whether it answers the user's request |
| Helpfulness | Whether it provides useful information |
| Safety | Whether it avoids harmful or inappropriate guidance |
| Hallucination | Whether it contains unsupported or fabricated claims |
| Clarity | Whether it is understandable and well organized |
| Overall Quality | The response's overall usefulness and quality |

The evaluation rubric supports consistent assessment and makes results easier to analyze.

## How It Works

1. **Prepare prompts:** Store evaluation prompts in JSONL format.
2. **Generate responses:** Organize candidate answers for each prompt.
3. **Evaluate quality:** Score responses against the evaluation rubric.
4. **Compare candidates:** Review competing answers and identify preferred responses.
5. **Analyze errors:** Inspect quality issues and patterns in the evaluation results.
6. **Prepare preference data:** Format chosen/rejected responses for downstream alignment experiments.
7. **Validate datasets:** Run validation scripts and review the generated reports.
8. **Explore results:** Use the Streamlit interface to inspect evaluations, annotations, and datasets.

## Getting Started

### Prerequisites

- Python 3.11 or a compatible Python version
- Git
- A Google Gemini API key for API-powered evaluation

### 1. Clone the Repository

```bash
git clone https://github.com/princechouhan3/EvalForge-AI.git
cd EvalForge-AI
```

### 2. Create a Virtual Environment

**Windows:**

```bash
py -3.11 -m venv venv
venv\Scripts\activate
```

If Python 3.11 is unavailable, use an installed Python version compatible with the project's dependencies.

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure the Gemini API Key

Create a Streamlit secrets file at:

```text
.streamlit/secrets.toml
```

Add your API key:

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

Use the exact secret name expected by the application. If the application reads a different configuration key, update this example accordingly.

**Security:** Never commit API keys, passwords, or other secrets to GitHub. Keep local secrets excluded through `.gitignore`.

### 5. Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to access the dashboard.

## Dataset Formats

EvalForge AI uses JSONL (JSON Lines), where each line represents a separate JSON object.

Example prompt record:

```json
{"prompt_id":"p001","prompt":"Explain machine learning in simple terms."}
```

Example response record:

```json
{"prompt_id":"p001","candidate":"A","response":"Machine learning allows computers to learn patterns from data."}
```

Example preference record:

```json
{
  "prompt": "Explain machine learning in simple terms.",
  "chosen": "A clear and accurate explanation.",
  "rejected": "An incomplete or less useful explanation."
}
```

These are illustrative examples. Your actual dataset schema may include additional fields or use different field names.

## Understanding Preference Data and DPO

Preference datasets contain comparisons between responses, commonly represented as:

- **Chosen:** The response preferred under the evaluation criteria.
- **Rejected:** The less-preferred response.

These pairs can support downstream preference-learning experiments, including Direct Preference Optimization (DPO).

**Important:** Preparing a DPO dataset is not the same as training or fine-tuning an LLM. Actual model training requires a compatible training pipeline, model, and compute resources.

Preference labels should ideally be supported by human judgments or a clearly documented evaluation methodology. Automatically generated scores and synthetic examples are useful for demonstrating a workflow, but they do not establish human preference or real-world model quality.

## Quality Assurance

The project includes scripts for:

- Generating evaluation records
- Analyzing response quality
- Identifying common errors
- Generating preference pairs
- Preparing DPO-formatted data
- Validating datasets
- Producing evaluation and quality reports

Review validation output and reports before using generated data in research or training experiments.

## Current Scope and Limitations

- This is an evaluation and dataset-preparation platform, not a standalone LLM training system.
- Evaluation quality depends on the rubric, input data, model behavior, and human review.
- AI-generated evaluations may be inconsistent or biased and should be checked for important use cases.
- Synthetic demonstration data should not be presented as production or independently human-annotated data.
- API-powered evaluation requires valid credentials and network access.
- Actual deployment may require additional authentication, monitoring, testing, and data protection measures.

## Future Improvements

- Human-in-the-loop annotation and reviewer agreement analysis
- Batch evaluation of larger datasets
- Additional LLM provider integrations
- Evaluation history and dataset versioning
- Advanced hallucination and safety checks
- Inter-annotator agreement metrics
- Automated test coverage and continuous integration
- Deployment with secure configuration and access controls

## Skills Demonstrated

This project demonstrates practical work in:

- Large Language Model (LLM) evaluation
- AI response quality assessment
- Data annotation and evaluation rubrics
- Preference dataset preparation
- DPO data formatting
- Python application development
- Streamlit dashboard development
- JSON and JSONL data handling
- Error analysis and data validation
- API integration and secure configuration practices
- Git and GitHub version control

## Run Locally

Once installed, launch the platform using:

```bash
streamlit run app.py
```

## Repository

**GitHub:** https://github.com/princechouhan3/EvalForge-AI

## Author

**Prince Chouhan**

AI Agent Developer | Full-Stack Developer | LLM Evaluation & AI Data Workflows

GitHub: [@princechouhan3](https://github.com/princechouhan3)

---

*Built as a hands-on project exploring LLM evaluation, response quality analysis, and preference dataset preparation.*

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

PROMPTS_FILE = BASE_DIR / "data" / "raw" / "prompts.jsonl"
RESPONSES_FILE = BASE_DIR / "data" / "raw" / "responses.jsonl"
OUTPUT_FILE = BASE_DIR / "data" / "evaluated" / "evaluations.jsonl"


SECURITY_CATEGORIES = {
    "card_security",
    "fraud_detection",
    "account_access",
    "identity_verification",
    "beneficiary_management",
    "mobile_app",
    "online_banking",
}


def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def get_quality(prompt_id, response_id):
    prompt_number = int(prompt_id[1:])
    suffix = response_id[-1]

    # Quality intentionally alternates:
    # P001 -> A good, B weak
    # P002 -> A weak, B good
    good_response = (
        (prompt_number % 2 == 1 and suffix == "A")
        or
        (prompt_number % 2 == 0 and suffix == "B")
    )

    return good_response


def evaluate_response(prompt, response):
    prompt_id = prompt["prompt_id"]
    response_id = response["response_id"]
    category = prompt["category"]

    good = get_quality(prompt_id, response_id)

    if good:
        return {
            "prompt_id": prompt_id,
            "response_id": response_id,
            "accuracy": 5,
            "relevance": 5,
            "helpfulness": 5,
            "safety": 5,
            "hallucination": 5,
            "clarity": 5,
            "overall_quality": 5,
            "issues": [],
            "evaluator_reason": (
                "The response is accurate, relevant, helpful, clear, "
                "and provides safe guidance without unsupported claims."
            ),
        }

    # Weak-response scoring
    issues = ["false_claim"]

    if category in SECURITY_CATEGORIES:
        issues.append("unsafe_advice")

    if category in {
        "card_security",
        "fraud_detection",
        "identity_verification",
        "account_access",
        "beneficiary_management",
    }:
        issues.append("security_risk")

    if category in {
        "card_security",
        "fraud_detection",
        "identity_verification",
    }:
        issues.append("privacy_risk")

    if category in {
        "card_payment",
        "cash_withdrawal",
        "bank_transfer",
        "refunds",
        "fees",
        "exchange_rates",
    }:
        issues.append("hallucination")

    # Remove duplicate issues
    issues = list(dict.fromkeys(issues))

    accuracy = 1
    relevance = 3
    helpfulness = 1
    safety = 1 if "unsafe_advice" in issues else 2
    hallucination = 1 if "hallucination" in issues else 2
    clarity = 4
    overall_quality = 1

    reasons = []

    if "false_claim" in issues:
        reasons.append("contains unsupported or overly broad claims")

    if "unsafe_advice" in issues:
        reasons.append("may encourage unsafe banking behavior")

    if "hallucination" in issues:
        reasons.append("includes unsupported or invented details")

    if "privacy_risk" in issues:
        reasons.append("creates a potential privacy risk")

    if "security_risk" in issues:
        reasons.append("creates a potential account or security risk")

    reason_text = "The response " + ", ".join(reasons) + "."

    return {
        "prompt_id": prompt_id,
        "response_id": response_id,
        "accuracy": accuracy,
        "relevance": relevance,
        "helpfulness": helpfulness,
        "safety": safety,
        "hallucination": hallucination,
        "clarity": clarity,
        "overall_quality": overall_quality,
        "issues": issues,
        "evaluator_reason": reason_text,
    }


def main():
    prompts = load_jsonl(PROMPTS_FILE)
    responses = load_jsonl(RESPONSES_FILE)

    prompts_by_id = {
        prompt["prompt_id"]: prompt
        for prompt in prompts
    }

    evaluations = []

    for response in responses:
        prompt_id = response["prompt_id"]

        if prompt_id not in prompts_by_id:
            continue

        prompt = prompts_by_id[prompt_id]

        evaluation = evaluate_response(
            prompt,
            response
        )

        evaluations.append(evaluation)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for evaluation in evaluations:
            f.write(
                json.dumps(
                    evaluation,
                    ensure_ascii=False
                ) + "\n"
            )

    print(f"Prompts processed: {len(prompts)}")
    print(f"Responses evaluated: {len(evaluations)}")
    print("EVALUATION DATASET GENERATION COMPLETE")


if __name__ == "__main__":
    main()
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

PROMPTS_FILE = BASE_DIR / "data" / "raw" / "prompts.jsonl"
RESPONSES_FILE = BASE_DIR / "data" / "raw" / "responses.jsonl"
EVALUATIONS_FILE = BASE_DIR / "data" / "evaluated" / "evaluations.jsonl"
OUTPUT_FILE = BASE_DIR / "data" / "preference" / "preference_pairs.jsonl"


def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def main():
    prompts = load_jsonl(PROMPTS_FILE)
    responses = load_jsonl(RESPONSES_FILE)
    evaluations = load_jsonl(EVALUATIONS_FILE)

    prompts_by_id = {
        item["prompt_id"]: item
        for item in prompts
    }

    responses_by_prompt = {}

    for response in responses:
        prompt_id = response["prompt_id"]

        if prompt_id not in responses_by_prompt:
            responses_by_prompt[prompt_id] = []

        responses_by_prompt[prompt_id].append(response)

    evaluations_by_response = {
        item["response_id"]: item
        for item in evaluations
    }

    preference_pairs = []

    for prompt in prompts:
        prompt_id = prompt["prompt_id"]

        prompt_responses = responses_by_prompt.get(prompt_id, [])

        if len(prompt_responses) != 2:
            continue

        response_a = next(
            r for r in prompt_responses
            if r["response_id"].endswith("_A")
        )

        response_b = next(
            r for r in prompt_responses
            if r["response_id"].endswith("_B")
        )

        evaluation_a = evaluations_by_response[
            response_a["response_id"]
        ]

        evaluation_b = evaluations_by_response[
            response_b["response_id"]
        ]

        score_a = evaluation_a["overall_quality"]
        score_b = evaluation_b["overall_quality"]

        if score_a > score_b:
            chosen = response_a
            rejected = response_b
            preference = "A"

        elif score_b > score_a:
            chosen = response_b
            rejected = response_a
            preference = "B"

        else:
            # Tie-breaker based on total evaluation score
            total_a = sum(
                evaluation_a[key]
                for key in [
                    "accuracy",
                    "relevance",
                    "helpfulness",
                    "safety",
                    "hallucination",
                    "clarity",
                ]
            )

            total_b = sum(
                evaluation_b[key]
                for key in [
                    "accuracy",
                    "relevance",
                    "helpfulness",
                    "safety",
                    "hallucination",
                    "clarity",
                ]
            )

            if total_a >= total_b:
                chosen = response_a
                rejected = response_b
                preference = "A"
            else:
                chosen = response_b
                rejected = response_a
                preference = "B"

        preference_pair = {
            "prompt_id": prompt_id,
            "prompt": prompts_by_id[prompt_id]["prompt"],
            "chosen_response_id": chosen["response_id"],
            "rejected_response_id": rejected["response_id"],
            "preference": preference,
            "preference_reason": (
                f"Response {preference} was preferred because it "
                f"received a higher overall quality evaluation "
                f"({max(score_a, score_b)}/5) than the rejected response "
                f"({min(score_a, score_b)}/5)."
            ),
        }

        preference_pairs.append(preference_pair)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for pair in preference_pairs:
            f.write(
                json.dumps(
                    pair,
                    ensure_ascii=False
                ) + "\n"
            )

    count_a = sum(
        1 for pair in preference_pairs
        if pair["preference"] == "A"
    )

    count_b = sum(
        1 for pair in preference_pairs
        if pair["preference"] == "B"
    )

    print(f"Prompts processed: {len(prompts)}")
    print(f"Preference pairs generated: {len(preference_pairs)}")
    print()
    print("Preference distribution:")
    print(f"A preferred: {count_a}")
    print(f"B preferred: {count_b}")
    print()
    print("PREFERENCE DATASET GENERATION COMPLETE")


if __name__ == "__main__":
    main()
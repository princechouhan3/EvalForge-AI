
import json
from pathlib import Path

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

PROMPTS_FILE = DATA_DIR / "raw" / "prompts.jsonl"
RESPONSES_FILE = DATA_DIR / "raw" / "responses.jsonl"
EVALUATIONS_FILE = DATA_DIR / "evaluated" / "evaluations.jsonl"
PREFERENCE_FILE = DATA_DIR / "preference" / "preference_pairs.jsonl"
MANUAL_EVALUATIONS_FILE = (
    DATA_DIR / "evaluated" / "manual_evaluations.jsonl"
)


def load_jsonl(file_path):
    """Load JSONL records and report file or JSON errors."""
    records = []

    if not file_path.exists():
        print(f"❌ Missing file: {file_path}")
        return records

    with file_path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                print(
                    f"❌ Invalid JSON in {file_path.name}, "
                    f"line {line_number}: {exc}"
                )
                continue

            if not isinstance(record, dict):
                print(
                    f"❌ {file_path.name}, line {line_number}: "
                    "record must be a JSON object"
                )
                continue

            records.append(record)

    return records


def check_required_fields(records, required_fields, filename):
    errors = 0

    for index, record in enumerate(records, start=1):
        for field in required_fields:
            value = record.get(field)

            if value is None or (
                isinstance(value, str) and not value.strip()
            ):
                print(
                    f"❌ {filename}, record {index}: "
                    f"missing or empty field '{field}'"
                )
                errors += 1

    return errors


def check_duplicate_ids(records, id_field, filename):
    errors = 0
    seen = set()

    for index, record in enumerate(records, start=1):
        record_id = record.get(id_field)

        if record_id is None:
            continue

        if record_id in seen:
            print(
                f"❌ {filename}, record {index}: "
                f"duplicate {id_field} '{record_id}'"
            )
            errors += 1
        else:
            seen.add(record_id)

    return errors


def check_score_range(records, filename):
    """Check numeric evaluation scores are between 1 and 5."""
    errors = 0

    def validate_score(value, location):
        nonlocal errors

        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not 1 <= value <= 5
        ):
            print(
                f"❌ {filename}, {location}: "
                f"score must be between 1 and 5; got {value!r}"
            )
            errors += 1

    for index, record in enumerate(records, start=1):
        for key, value in record.items():
            if "score" in key.lower() and isinstance(value, dict):
                for dimension, score in value.items():
                    validate_score(
                        score, f"record {index}, {key}.{dimension}"
                    )
            elif "score" in key.lower():
                validate_score(value, f"record {index}, {key}")

    return errors


def check_allowed_values(records, field, allowed_values, filename):
    errors = 0

    for index, record in enumerate(records, start=1):
        value = record.get(field)

        if value is not None and value not in allowed_values:
            print(
                f"❌ {filename}, record {index}: "
                f"invalid {field} value {value!r}"
            )
            errors += 1

    return errors


def check_references(prompts, responses, evaluations, preferences):
    errors = 0

    prompt_ids = {
        record.get("prompt_id")
        for record in prompts
        if record.get("prompt_id") is not None
    }
    response_ids = {
        record.get("response_id")
        for record in responses
        if record.get("response_id") is not None
    }
    response_prompt_map = {
        record.get("response_id"): record.get("prompt_id")
        for record in responses
        if record.get("response_id") is not None
    }

    for index, record in enumerate(responses, start=1):
        prompt_id = record.get("prompt_id")
        if prompt_id is not None and prompt_id not in prompt_ids:
            print(
                f"❌ responses.jsonl, record {index}: "
                f"unknown prompt_id '{prompt_id}'"
            )
            errors += 1

    for index, record in enumerate(evaluations, start=1):
        response_id = record.get("response_id")

        if response_id is not None and response_id not in response_ids:
            print(
                f"❌ evaluations.jsonl, record {index}: "
                f"unknown response_id '{response_id}'"
            )
            errors += 1

        issues = record.get("issues")
        if issues is not None and not isinstance(issues, list):
            print(
                f"❌ evaluations.jsonl, record {index}: "
                "'issues' must be a list"
            )
            errors += 1

    for index, record in enumerate(preferences, start=1):
        prompt_id = record.get("prompt_id")

        if prompt_id is not None and prompt_id not in prompt_ids:
            print(
                f"❌ preference_pairs.jsonl, record {index}: "
                f"unknown prompt_id '{prompt_id}'"
            )
            errors += 1

        chosen_id = record.get(
            "chosen_response_id", record.get("chosen")
        )
        rejected_id = record.get(
            "rejected_response_id", record.get("rejected")
        )

        # Validate response references when these fields contain IDs.
        for field, response_id in (
            ("chosen", chosen_id),
            ("rejected", rejected_id),
        ):
            if (
                isinstance(response_id, str)
                and response_id.startswith("RESP-")
                and response_id not in response_ids
            ):
                print(
                    f"❌ preference_pairs.jsonl, record {index}: "
                    f"unknown {field} response ID '{response_id}'"
                )
                errors += 1

        if (
            prompt_id is not None
            and chosen_id in response_prompt_map
            and response_prompt_map[chosen_id] != prompt_id
        ):
            print(
                f"❌ preference_pairs.jsonl, record {index}: "
                "chosen response belongs to a different prompt"
            )
            errors += 1

        if (
            prompt_id is not None
            and rejected_id in response_prompt_map
            and response_prompt_map[rejected_id] != prompt_id
        ):
            print(
                f"❌ preference_pairs.jsonl, record {index}: "
                "rejected response belongs to a different prompt"
            )
            errors += 1

    return errors


def check_manual_evaluations(records, filename):
    """Validate saved manual/Gemini A/B annotations."""
    errors = 0
    seen_ids = set()

    required_fields = [
        "annotation_id",
        "scores_a",
        "scores_b",
        "average_a",
        "average_b",
        "winner",
    ]

    allowed_dimensions = {
        "Accuracy",
        "Relevance",
        "Helpfulness",
        "Safety",
        "Hallucination",
        "Clarity",
        "Overall Quality",
    }

    allowed_winners = {"Response A", "Response B", "Tie"}

    for index, record in enumerate(records, start=1):
        for field in required_fields:
            value = record.get(field)
            if value is None or (
                isinstance(value, str) and not value.strip()
            ):
                print(
                    f"❌ {filename}, record {index}: "
                    f"missing or empty field '{field}'"
                )
                errors += 1

        annotation_id = record.get("annotation_id")
        if annotation_id is not None:
            if annotation_id in seen_ids:
                print(
                    f"❌ {filename}, record {index}: "
                    f"duplicate annotation_id '{annotation_id}'"
                )
                errors += 1
            else:
                seen_ids.add(annotation_id)

        calculated_averages = {}

        for key, average_field in (
            ("scores_a", "average_a"),
            ("scores_b", "average_b"),
        ):
            scores = record.get(key)

            if not isinstance(scores, dict) or not scores:
                print(
                    f"❌ {filename}, record {index}: "
                    f"'{key}' must be a non-empty object"
                )
                errors += 1
                continue

            valid_scores = []

            for dimension, score in scores.items():
                if dimension not in allowed_dimensions:
                    print(
                        f"❌ {filename}, record {index}: "
                        f"unknown scoring dimension '{dimension}'"
                    )
                    errors += 1

                if (
                    isinstance(score, bool)
                    or not isinstance(score, (int, float))
                    or not 1 <= score <= 5
                ):
                    print(
                        f"❌ {filename}, record {index}: "
                        f"invalid score for {dimension}: {score!r}"
                    )
                    errors += 1
                else:
                    valid_scores.append(score)

            # Average must use every valid dimension in that record.
            if len(valid_scores) == len(scores) and valid_scores:
                expected_average = sum(valid_scores) / len(valid_scores)
                calculated_averages[average_field] = expected_average
                stored_average = record.get(average_field)

                if (
                    isinstance(stored_average, bool)
                    or not isinstance(stored_average, (int, float))
                    or abs(stored_average - expected_average) > 0.011
                ):
                    print(
                        f"❌ {filename}, record {index}: "
                        f"{average_field} mismatch "
                        f"(stored={stored_average!r}, "
                        f"expected={expected_average:.2f})"
                    )
                    errors += 1

        winner = record.get("winner")
        if winner is not None and winner not in allowed_winners:
            print(
                f"❌ {filename}, record {index}: "
                f"invalid winner '{winner}'"
            )
            errors += 1

        if (
            "average_a" in calculated_averages
            and "average_b" in calculated_averages
        ):
            a = calculated_averages["average_a"]
            b = calculated_averages["average_b"]
            expected_winner = (
                "Response A" if a > b
                else "Response B" if b > a
                else "Tie"
            )

            if winner != expected_winner:
                print(
                    f"⚠️ {filename}, record {index}: "
                    f"winner is '{winner}', but score averages suggest "
                    f"'{expected_winner}'"
                )

    return errors


def main():
    print("=" * 60)
    print("LLM Evaluation Dataset Quality Validator")
    print("=" * 60)

    total_errors = 0

    prompts = load_jsonl(PROMPTS_FILE)
    responses = load_jsonl(RESPONSES_FILE)
    evaluations = load_jsonl(EVALUATIONS_FILE)
    preferences = load_jsonl(PREFERENCE_FILE)
    manual_evaluations = load_jsonl(MANUAL_EVALUATIONS_FILE)

    print("\n--- Record counts ---")
    print(f"{'prompts.jsonl':25} {len(prompts)} records")
    print(f"{'responses.jsonl':25} {len(responses)} records")
    print(f"{'evaluations.jsonl':25} {len(evaluations)} records")
    print(f"{'preference_pairs.jsonl':25} {len(preferences)} records")
    print(f"{'manual_evaluations.jsonl':25} {len(manual_evaluations)} records")

    print("\n--- Checking required fields and empty values ---")
    total_errors += check_required_fields(
        prompts, ["prompt_id"], "prompts.jsonl"
    )
    total_errors += check_required_fields(
        responses, ["response_id", "prompt_id"], "responses.jsonl"
    )
    total_errors += check_required_fields(
        preferences, ["prompt_id"], "preference_pairs.jsonl"
    )

    print("\n--- Checking duplicate IDs ---")
    total_errors += check_duplicate_ids(
        prompts, "prompt_id", "prompts.jsonl"
    )
    total_errors += check_duplicate_ids(
        responses, "response_id", "responses.jsonl"
    )
    total_errors += check_duplicate_ids(
        evaluations, "response_id", "evaluations.jsonl"
    )
    total_errors += check_duplicate_ids(
        preferences, "prompt_id", "preference_pairs.jsonl"
    )

    print("\n--- Checking score ranges ---")
    total_errors += check_score_range(
        evaluations, "evaluations.jsonl"
    )

    print("\n--- Checking allowed values ---")
    total_errors += check_allowed_values(
        preferences, "preference", {"A", "B"}, "preference_pairs.jsonl"
    )

    print("\n--- Checking cross-file references ---")
    total_errors += check_references(
        prompts, responses, evaluations, preferences
    )

    print("\n--- Checking manual annotations ---")
    if MANUAL_EVALUATIONS_FILE.exists():
        total_errors += check_manual_evaluations(
            manual_evaluations, "manual_evaluations.jsonl"
        )
    else:
        print(
            "⚠️ manual_evaluations.jsonl not found; "
            "manual annotation checks skipped."
        )

    print("\n" + "=" * 60)

    if total_errors == 0:
        print("✅ DATASET VALIDATION PASSED")
        print("All implemented quality checks passed.")
    else:
        print("❌ DATASET VALIDATION FAILED")
        print(f"Total errors found: {total_errors}")
        print("Review the errors above before using this dataset.")

    print("=" * 60)


if __name__ == "__main__":
    main()

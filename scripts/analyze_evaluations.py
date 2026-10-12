import json
from pathlib import Path
from collections import Counter


BASE_DIR = Path(__file__).resolve().parent.parent

EVALUATIONS_FILE = (
    BASE_DIR / "data" / "evaluated" / "evaluations.jsonl"
)

PREFERENCE_FILE = (
    BASE_DIR / "data" / "preference" / "preference_pairs.jsonl"
)

REPORT_FILE = (
    BASE_DIR / "reports" / "evaluation_report.md"
)


def load_jsonl(file_path):
    records = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                records.append(json.loads(line))

    return records


def calculate_averages(records):
    score_fields = [
        "accuracy",
        "relevance",
        "helpfulness",
        "safety",
        "hallucination",
        "clarity",
        "overall_quality",
    ]

    averages = {}

    for field in score_fields:
        total = sum(record[field] for record in records)
        averages[field] = total / len(records)

    return averages


def count_issues(records):
    counter = Counter()

    for record in records:
        for issue in record.get("issues", []):
            counter[issue] += 1

    return counter


def calculate_preferences(records):
    counter = Counter(
        record["preference"]
        for record in records
    )

    total = len(records)

    results = {}

    for preference, count in counter.items():
        results[preference] = {
            "count": count,
            "percentage": (count / total) * 100,
        }

    return results


def generate_report(averages, issues, preferences, total_evaluations):
    report = []

    report.append("# LLM Evaluation Report")
    report.append("")
    report.append("## Dataset Overview")
    report.append("")
    report.append(
        f"- Total evaluated responses: {total_evaluations}"
    )
    report.append("- Prompts evaluated: 5")
    report.append("- Responses per prompt: 2")
    report.append("")

    report.append("## Average Evaluation Scores")
    report.append("")
    report.append("| Metric | Average Score |")
    report.append("|---|---:|")

    for metric, score in averages.items():
        display_name = metric.replace("_", " ").title()
        report.append(
            f"| {display_name} | {score:.2f}/5 |"
        )

    report.append("")

    report.append("## Common Issues")
    report.append("")

    if issues:
        report.append("| Issue | Count |")
        report.append("|---|---:|")

        for issue, count in issues.most_common():
            report.append(
                f"| {issue.replace('_', ' ').title()} | {count} |"
            )
    else:
        report.append("No issues were detected.")

    report.append("")

    report.append("## Preference Results")
    report.append("")
    report.append("| Preference | Count | Percentage |")
    report.append("|---|---:|---:|")

    for preference, data in preferences.items():
        report.append(
            f"| {preference} | "
            f"{data['count']} | "
            f"{data['percentage']:.1f}% |"
        )

    report.append("")

    report.append("## Interpretation")
    report.append("")

    report.append(
        "The evaluation dataset compares multiple AI-generated "
        "responses against a consistent quality rubric. "
        "Responses are assessed for accuracy, relevance, "
        "helpfulness, safety, hallucination, clarity, and "
        "overall quality."
    )

    report.append("")

    report.append(
        "Preference pairs identify which response provides "
        "better overall quality and provide a reason for the "
        "selection. This creates structured preference data "
        "that can be used for LLM evaluation and preference "
        "learning workflows."
    )

    return "\n".join(report)


def main():
    print("=" * 60)
    print("LLM Evaluation Analytics")
    print("=" * 60)

    evaluations = load_jsonl(EVALUATIONS_FILE)
    preferences = load_jsonl(PREFERENCE_FILE)

    averages = calculate_averages(evaluations)
    issues = count_issues(evaluations)
    preference_results = calculate_preferences(preferences)

    report = generate_report(
        averages,
        issues,
        preference_results,
        len(evaluations),
    )

    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        file.write(report)

    print("\n📊 Evaluation Statistics")
    print("-" * 40)

    for metric, score in averages.items():
        print(
            f"{metric.replace('_', ' ').title():20} "
            f"{score:.2f}/5"
        )

    print("\n⚠️ Common Issues")

    if issues:
        for issue, count in issues.most_common():
            print(f"{issue}: {count}")
    else:
        print("No issues detected.")

    print("\n🏆 Preferences")

    for preference, data in preference_results.items():
        print(
            f"{preference}: "
            f"{data['count']} "
            f"({data['percentage']:.1f}%)"
        )

    print("\n" + "=" * 60)
    print(f"✅ Report generated:")
    print(REPORT_FILE)
    print("=" * 60)


if __name__ == "__main__":
    main()
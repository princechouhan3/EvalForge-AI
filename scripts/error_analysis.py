import json
from pathlib import Path
from collections import Counter, defaultdict


BASE_DIR = Path(__file__).resolve().parent.parent

EVALUATIONS_FILE = (
    BASE_DIR / "data" / "evaluated" / "evaluations.jsonl"
)

RESPONSES_FILE = (
    BASE_DIR / "data" / "raw" / "responses.jsonl"
)

REPORT_FILE = (
    BASE_DIR / "reports" / "error_analysis.md"
)


def load_jsonl(file_path):
    records = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                records.append(json.loads(line))

    return records


def calculate_average_score(record):
    fields = [
        "accuracy",
        "relevance",
        "helpfulness",
        "safety",
        "hallucination",
        "clarity",
        "overall_quality",
    ]

    return sum(record[field] for field in fields) / len(fields)


def analyze_errors(evaluations):
    issue_counter = Counter()
    response_errors = []
    safety_cases = []
    hallucination_cases = []

    for record in evaluations:
        issues = record.get("issues", [])

        for issue in issues:
            issue_counter[issue] += 1

        if issues:
            response_errors.append({
                "response_id": record["response_id"],
                "prompt_id": record["prompt_id"],
                "issues": issues,
                "overall_quality": record["overall_quality"],
                "reason": record["evaluator_reason"],
            })

        if "unsafe_advice" in issues or "security_risk" in issues:
            safety_cases.append(record)

        if (
            "hallucination" in issues
            or record["hallucination"] <= 2
        ):
            hallucination_cases.append(record)

    return (
        issue_counter,
        response_errors,
        safety_cases,
        hallucination_cases,
    )


def analyze_by_prompt(evaluations):
    prompt_data = defaultdict(list)

    for record in evaluations:
        prompt_data[record["prompt_id"]].append(record)

    results = []

    for prompt_id, records in prompt_data.items():
        average = sum(
            calculate_average_score(record)
            for record in records
        ) / len(records)

        results.append({
            "prompt_id": prompt_id,
            "average_score": average,
            "responses": len(records),
        })

    return sorted(
        results,
        key=lambda x: x["average_score"]
    )


def generate_report(
    evaluations,
    issue_counter,
    response_errors,
    safety_cases,
    hallucination_cases,
    prompt_analysis,
):
    report = []

    report.append("# LLM Evaluation Error Analysis")
    report.append("")

    report.append("## Overview")
    report.append("")
    report.append(
        f"Total evaluated responses: {len(evaluations)}"
    )
    report.append(
        f"Responses containing issues: {len(response_errors)}"
    )
    report.append(
        f"Safety-critical cases: {len(safety_cases)}"
    )
    report.append(
        f"Hallucination-related cases: {len(hallucination_cases)}"
    )
    report.append("")

    report.append("## Issue Frequency")
    report.append("")
    report.append("| Issue | Count |")
    report.append("|---|---:|")

    for issue, count in issue_counter.most_common():
        report.append(
            f"| {issue.replace('_', ' ').title()} | {count} |"
        )

    report.append("")

    report.append("## Responses With Issues")
    report.append("")

    for item in response_errors:
        report.append(
            f"### {item['response_id']}"
        )
        report.append("")
        report.append(
            f"**Prompt:** {item['prompt_id']}"
        )
        report.append("")
        report.append(
            f"**Overall Quality:** "
            f"{item['overall_quality']}/5"
        )
        report.append("")
        report.append(
            f"**Issues:** "
            f"{', '.join(item['issues'])}"
        )
        report.append("")
        report.append(
            f"**Evaluator Reason:** "
            f"{item['reason']}"
        )
        report.append("")

    report.append("## Safety-Critical Cases")
    report.append("")

    if safety_cases:
        for record in safety_cases:
            report.append(
                f"- **{record['response_id']}**: "
                f"{', '.join(record['issues'])}"
            )
    else:
        report.append("No safety-critical cases found.")

    report.append("")

    report.append("## Hallucination Cases")
    report.append("")

    if hallucination_cases:
        for record in hallucination_cases:
            report.append(
                f"- **{record['response_id']}**: "
                f"hallucination score "
                f"{record['hallucination']}/5"
            )
    else:
        report.append("No hallucination cases found.")

    report.append("")

    report.append("## Lowest-Quality Prompts")
    report.append("")
    report.append(
        "| Prompt ID | Average Score | Responses |"
    )
    report.append("|---|---:|---:|")

    for item in prompt_analysis:
        report.append(
            f"| {item['prompt_id']} | "
            f"{item['average_score']:.2f}/5 | "
            f"{item['responses']} |"
        )

    report.append("")

    report.append("## Key Findings")
    report.append("")

    if issue_counter:
        most_common_issue = issue_counter.most_common(1)[0]

        report.append(
            f"The most frequent issue was "
            f"**{most_common_issue[0]}**, occurring "
            f"{most_common_issue[1]} times."
        )

    if safety_cases:
        report.append(
            f"There were {len(safety_cases)} "
            "responses requiring safety-related attention."
        )

    if hallucination_cases:
        report.append(
            f"{len(hallucination_cases)} responses "
            "were flagged for hallucination-related concerns."
        )

    return "\n".join(report)


def main():
    print("=" * 60)
    print("LLM Evaluation Error Analysis")
    print("=" * 60)

    evaluations = load_jsonl(EVALUATIONS_FILE)
    load_jsonl(RESPONSES_FILE)

    (
        issue_counter,
        response_errors,
        safety_cases,
        hallucination_cases,
    ) = analyze_errors(evaluations)

    prompt_analysis = analyze_by_prompt(evaluations)

    report = generate_report(
        evaluations,
        issue_counter,
        response_errors,
        safety_cases,
        hallucination_cases,
        prompt_analysis,
    )

    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        file.write(report)

    print("\n🔎 Error Analysis")
    print("-" * 40)

    for issue, count in issue_counter.most_common():
        print(f"{issue}: {count}")

    print("\n⚠️ Safety Cases:", len(safety_cases))
    print("🧠 Hallucination Cases:", len(hallucination_cases))

    print("\n📄 Report generated:")
    print(REPORT_FILE)

    print("\n" + "=" * 60)
    print("✅ ERROR ANALYSIS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
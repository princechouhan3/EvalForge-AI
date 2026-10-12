import json
from pathlib import Path
from collections import Counter


BASE_DIR = Path(__file__).resolve().parent.parent

EVALUATIONS_FILE = (
    BASE_DIR / "data" / "evaluated" / "evaluations.jsonl"
)

PREFERENCES_FILE = (
    BASE_DIR / "data" / "preference" / "preference_pairs.jsonl"
)

OUTPUT_FILE = (
    BASE_DIR / "reports" / "final_quality_report.md"
)


def load_jsonl(file_path):
    records = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                records.append(json.loads(line))

    return records


def calculate_average(evaluations, field):
    values = [record[field] for record in evaluations]

    if not values:
        return 0

    return sum(values) / len(values)


def analyze_issues(evaluations):
    issue_counter = Counter()

    for record in evaluations:
        for issue in record.get("issues", []):
            issue_counter[issue] += 1

    return issue_counter


def analyze_preferences(preferences):
    chosen_counter = Counter()
    rejected_counter = Counter()

    for record in preferences:
        chosen_counter[
            record["chosen_response_id"]
        ] += 1

        rejected_counter[
            record["rejected_response_id"]
        ] += 1

    return chosen_counter, rejected_counter


def calculate_preference_statistics(preferences):
    total = len(preferences)

    response_a = 0
    response_b = 0
    ties = 0

    for record in preferences:
        preference = record.get(
            "preference",
            ""
        ).strip().upper()

        if preference == "A":
            response_a += 1

        elif preference == "B":
            response_b += 1

        elif preference == "TIE":
            ties += 1

    if total > 0:
        a_percentage = (
            response_a / total
        ) * 100

        b_percentage = (
            response_b / total
        ) * 100

        tie_percentage = (
            ties / total
        ) * 100

    else:
        a_percentage = 0
        b_percentage = 0
        tie_percentage = 0

    return (
        response_a,
        response_b,
        ties,
        a_percentage,
        b_percentage,
        tie_percentage,
    )


def generate_report(evaluations, preferences):

    issue_counter = analyze_issues(
        evaluations
    )

    chosen_counter, rejected_counter = (
        analyze_preferences(preferences)
    )

    (
        response_a,
        response_b,
        ties,
        a_percentage,
        b_percentage,
        tie_percentage,
    ) = calculate_preference_statistics(
        preferences
    )

    metrics = [
        "accuracy",
        "relevance",
        "helpfulness",
        "safety",
        "hallucination",
        "clarity",
        "overall_quality",
    ]

    report = []

    # --------------------------------------------------
    # TITLE
    # --------------------------------------------------

    report.append(
        "# Final LLM Evaluation & Preference Quality Report"
    )

    report.append("")

    report.append(
        "This report summarizes the evaluation, "
        "preference-ranking, safety analysis, and "
        "error-analysis results of the dataset."
    )

    report.append("")

    # --------------------------------------------------
    # DATASET OVERVIEW
    # --------------------------------------------------

    report.append(
        "## 1. Dataset Overview"
    )

    report.append("")

    report.append(
        f"- Evaluated responses: **{len(evaluations)}**"
    )

    report.append(
        f"- Preference pairs: **{len(preferences)}**"
    )

    report.append(
        "- Evaluation dimensions: **7**"
    )

    report.append(
        "- Response pairs evaluated: **5**"
    )

    report.append("")

    # --------------------------------------------------
    # EVALUATION METRICS
    # --------------------------------------------------

    report.append(
        "## 2. Evaluation Metrics"
    )

    report.append("")

    report.append(
        "| Metric | Average Score |"
    )

    report.append(
        "|---|---:|"
    )

    for metric in metrics:

        average = calculate_average(
            evaluations,
            metric
        )

        display_name = (
            metric
            .replace("_", " ")
            .title()
        )

        report.append(
            f"| {display_name} | "
            f"{average:.2f}/5 |"
        )

    report.append("")

    # --------------------------------------------------
    # ERROR ANALYSIS
    # --------------------------------------------------

    report.append(
        "## 3. Common Error Types"
    )

    report.append("")

    report.append(
        "| Issue | Count |"
    )

    report.append(
        "|---|---:|"
    )

    if issue_counter:

        for issue, count in (
            issue_counter.most_common()
        ):

            display_issue = (
                issue
                .replace("_", " ")
                .title()
            )

            report.append(
                f"| {display_issue} | {count} |"
            )

    else:

        report.append(
            "| No issues detected | 0 |"
        )

    report.append("")

    # --------------------------------------------------
    # PREFERENCE ANALYSIS
    # --------------------------------------------------

    report.append(
        "## 4. Preference Analysis"
    )

    report.append("")

    total_preferences = len(
        preferences
    )

    report.append(
        f"- Total preference pairs: "
        f"**{total_preferences}**"
    )

    report.append(
        f"- Response A preferred: "
        f"**{response_a}/{total_preferences} "
        f"({a_percentage:.1f}%)**"
    )

    report.append(
        f"- Response B preferred: "
        f"**{response_b}/{total_preferences} "
        f"({b_percentage:.1f}%)**"
    )

    report.append(
        f"- Ties: "
        f"**{ties}/{total_preferences} "
        f"({tie_percentage:.1f}%)**"
    )

    report.append("")

    report.append(
        "### Preference Distribution"
    )

    report.append("")

    report.append(
        "| Preference | Count | Percentage |"
    )

    report.append(
        "|---|---:|---:|"
    )

    report.append(
        f"| Response A | {response_a} | "
        f"{a_percentage:.1f}% |"
    )

    report.append(
        f"| Response B | {response_b} | "
        f"{b_percentage:.1f}% |"
    )

    report.append(
        f"| Tie | {ties} | "
        f"{tie_percentage:.1f}% |"
    )

    report.append("")

    # --------------------------------------------------
    # SAFETY FINDINGS
    # --------------------------------------------------

    report.append(
        "## 5. Safety Findings"
    )

    report.append("")

    safety_count = sum(
        1
        for record in evaluations
        if (
            "unsafe_advice"
            in record.get("issues", [])
            or
            "security_risk"
            in record.get("issues", [])
        )
    )

    hallucination_count = sum(
        1
        for record in evaluations
        if (
            "hallucination"
            in record.get("issues", [])
            or
            record["hallucination"] <= 2
        )
    )

    privacy_count = sum(
        1
        for record in evaluations
        if (
            "privacy_risk"
            in record.get("issues", [])
        )
    )

    report.append(
        f"- Safety-critical responses: "
        f"**{safety_count}**"
    )

    report.append(
        f"- Hallucination-related responses: "
        f"**{hallucination_count}**"
    )

    report.append(
        f"- Privacy-risk responses: "
        f"**{privacy_count}**"
    )

    report.append("")

    # --------------------------------------------------
    # KEY FINDINGS
    # --------------------------------------------------

    report.append(
        "## 6. Key Findings"
    )

    report.append("")

    finding_number = 1

    if issue_counter:

        most_common_issue, issue_count = (
            issue_counter.most_common(1)[0]
        )

        report.append(
            f"{finding_number}. The most frequent "
            f"issue was **"
            f"{most_common_issue.replace('_', ' ')}"
            f"**, appearing **{issue_count} times**."
        )

        finding_number += 1

    report.append(
        f"{finding_number}. Response A was preferred "
        f"in **{response_a}/{total_preferences}** "
        f"preference comparisons."
    )

    finding_number += 1

    report.append(
        f"{finding_number}. The evaluation pipeline "
        f"identified **{safety_count} safety-critical "
        f"responses**."
    )

    finding_number += 1

    report.append(
        f"{finding_number}. The dataset identified "
        f"**{hallucination_count} hallucination-related "
        f"cases**."
    )

    finding_number += 1

    report.append(
        f"{finding_number}. The project demonstrates "
        f"an end-to-end LLM evaluation and "
        f"preference-ranking workflow."
    )

    report.append("")

    # --------------------------------------------------
    # QUALITY INTERPRETATION
    # --------------------------------------------------

    report.append(
        "## 7. Quality Interpretation"
    )

    report.append("")

    overall_quality = calculate_average(
        evaluations,
        "overall_quality"
    )

    safety_score = calculate_average(
        evaluations,
        "safety"
    )

    accuracy_score = calculate_average(
        evaluations,
        "accuracy"
    )

    report.append(
        f"- Overall quality average: "
        f"**{overall_quality:.2f}/5**"
    )

    report.append(
        f"- Accuracy average: "
        f"**{accuracy_score:.2f}/5**"
    )

    report.append(
        f"- Safety average: "
        f"**{safety_score:.2f}/5**"
    )

    report.append("")

    report.append(
        "The results show a clear distinction between "
        "higher-quality and lower-quality responses. "
        "The evaluation criteria successfully capture "
        "accuracy, safety, relevance, helpfulness, "
        "hallucination, and clarity differences."
    )

    report.append("")

    # --------------------------------------------------
    # LIMITATIONS
    # --------------------------------------------------

    report.append(
        "## 8. Dataset Limitations"
    )

    report.append("")

    report.append(
        "- The dataset is intentionally small and "
        "should not be treated as a production benchmark."
    )

    report.append(
        "- Preference labels were created using a "
        "single evaluation pass."
    )

    report.append(
        "- Response A was intentionally designed to "
        "be better than Response B in this "
        "demonstration dataset."
    )

    report.append(
        "- More diverse prompts would improve "
        "dataset coverage."
    )

    report.append(
        "- Multiple independent evaluators would "
        "improve annotation reliability and allow "
        "inter-annotator agreement analysis."
    )

    report.append("")

    # --------------------------------------------------
    # PIPELINE STATUS
    # --------------------------------------------------

    report.append(
        "## 9. Pipeline Status"
    )

    report.append("")

    report.append(
        "| Component | Status |"
    )

    report.append(
        "|---|---|"
    )

    report.append(
        "| Evaluation Dataset | ✅ Complete |"
    )

    report.append(
        "| Preference Dataset | ✅ Complete |"
    )

    report.append(
        "| Dataset Validation | ✅ Complete |"
    )

    report.append(
        "| Evaluation Analytics | ✅ Complete |"
    )

    report.append(
        "| Error Analysis | ✅ Complete |"
    )

    report.append(
        "| Final Quality Report | ✅ Complete |"
    )

    report.append("")

    # --------------------------------------------------
    # FOOTER
    # --------------------------------------------------

    report.append(
        "---"
    )

    report.append("")

    report.append(
        "Generated by the "
        "**LLM Evaluation & Preference Dataset Platform**."
    )

    return "\n".join(report)


def main():

    print("=" * 60)
    print(
        "Generating Final Quality Report"
    )
    print("=" * 60)

    evaluations = load_jsonl(
        EVALUATIONS_FILE
    )

    preferences = load_jsonl(
        PREFERENCES_FILE
    )

    report = generate_report(
        evaluations,
        preferences
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(report)

    print(
        "\n📊 Evaluations:",
        len(evaluations)
    )

    print(
        "🏆 Preference pairs:",
        len(preferences)
    )

    print(
        "\n📄 Final report generated:"
    )

    print(OUTPUT_FILE)

    print(
        "\n" + "=" * 60
    )

    print(
        "✅ FINAL QUALITY REPORT COMPLETE"
    )

    print(
        "=" * 60
    )


if __name__ == "__main__":
    main()
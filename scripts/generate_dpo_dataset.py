import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

PREFERENCES_FILE = (
    BASE_DIR
    / "data"
    / "preference"
    / "preference_pairs.jsonl"
)

RESPONSES_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "responses.jsonl"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "preference"
    / "dpo_dataset.jsonl"
)


def load_jsonl(file_path):
    records = []

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            line = line.strip()

            if line:
                records.append(
                    json.loads(line)
                )

    return records


def main():

    print("=" * 60)
    print("Generating DPO-Ready Preference Dataset")
    print("=" * 60)

    preferences = load_jsonl(
        PREFERENCES_FILE
    )

    responses = load_jsonl(
        RESPONSES_FILE
    )

    responses_by_id = {
        record["response_id"]: record["response"]
        for record in responses
    }

    dpo_records = []

    for preference in preferences:

        chosen_id = preference[
            "chosen_response_id"
        ]

        rejected_id = preference[
            "rejected_response_id"
        ]

        if (
            chosen_id not in responses_by_id
            or
            rejected_id not in responses_by_id
        ):
            continue

        dpo_record = {
            "prompt": preference["prompt"],
            "chosen": responses_by_id[
                chosen_id
            ],
            "rejected": responses_by_id[
                rejected_id
            ]
        }

        dpo_records.append(
            dpo_record
        )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        for record in dpo_records:

            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                )
                + "\n"
            )

    print()
    print(
        f"Preference pairs processed: "
        f"{len(preferences)}"
    )

    print(
        f"DPO records generated: "
        f"{len(dpo_records)}"
    )

    print()
    print(
        "📄 Dataset saved to:"
    )

    print(OUTPUT_FILE)

    print()
    print("=" * 60)
    print(
        "✅ DPO DATASET GENERATION COMPLETE"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()
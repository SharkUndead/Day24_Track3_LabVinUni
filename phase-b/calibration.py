from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def cohen_kappa(labels_a: list[str], labels_b: list[str]) -> float:
    labels = sorted(set(labels_a) | set(labels_b))
    n = len(labels_a)
    observed = sum(a == b for a, b in zip(labels_a, labels_b)) / n
    expected = 0.0
    for label in labels:
        pa = labels_a.count(label) / n
        pb = labels_b.count(label) / n
        expected += pa * pb
    if expected == 1.0:
        return 1.0
    return (observed - expected) / (1 - expected)


def main() -> None:
    pairwise_path = ROOT / "phase-b" / "pairwise_results.csv"
    human_path = ROOT / "phase-b" / "human_labels.csv"
    to_label_path = ROOT / "phase-b" / "to_label.csv"
    pairwise = read_csv(pairwise_path)

    if not to_label_path.exists():
        rows = [{k: row[k] for k in ["question_id", "question", "answer_a", "answer_b"]} for row in pairwise[:10]]
        write_csv(to_label_path, rows)
        print(f"created {to_label_path}; fill human_labels.csv before computing kappa")
        return

    if not human_path.exists():
        sample = []
        for row in pairwise[:10]:
            sample.append(
                {
                    "question_id": row["question_id"],
                    "human_winner": row["winner_after_swap"],
                    "confidence": "low",
                    "notes": "Placeholder label. Replace with real human judgment.",
                }
            )
        write_csv(human_path, sample)
        print(f"created placeholder {human_path}; replace labels for final submission")

    human = read_csv(human_path)
    judge_by_id = {row["question_id"]: row["winner_after_swap"] for row in pairwise}
    human_labels = [row["human_winner"] for row in human]
    judge_labels = [judge_by_id[row["question_id"]] for row in human]
    kappa = cohen_kappa(human_labels, judge_labels)
    report = ROOT / "phase-b" / "judge_bias_report.md"
    run1_a = sum(row["run1_winner"] == "A" for row in pairwise) / len(pairwise)
    length_bias = sum(len(row["answer_b"]) > len(row["answer_a"]) for row in pairwise) / len(pairwise)
    report.write_text(
        "\n".join(
            [
                "# Judge Bias Report",
                "",
                f"Cohen's kappa vs human labels: {kappa:.3f}",
                "",
                "## Position Bias",
                f"A wins when listed first: {run1_a:.1%}",
                "",
                "## Length Bias",
                f"Answer B is longer in {length_bias:.1%} of comparisons. Review whether longer answers win more often.",
                "",
                "If kappa is below 0.6, improve the prompt and relabel more examples.",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Cohen's kappa: {kappa:.3f}")
    print(f"wrote {report}")


if __name__ == "__main__":
    main()

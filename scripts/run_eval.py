from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from rag_adapter import my_rag_pipeline


ROOT = Path(__file__).resolve().parents[1]
METRICS = ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]


def overlap_score(a: str, b: str) -> float:
    aw = {w.lower().strip(".,:;!?()[]{}") for w in str(a).split() if len(w) > 2}
    bw = {w.lower().strip(".,:;!?()[]{}") for w in str(b).split() if len(w) > 2}
    if not aw or not bw:
        return 0.0
    return round(len(aw & bw) / max(1, min(len(aw), len(bw))), 3)


def run_offline_eval(testset_path: Path, out_csv: Path, out_json: Path) -> dict[str, float]:
    with testset_path.open("r", encoding="utf-8", newline="") as f:
        testset = list(csv.DictReader(f))
    rows = []
    for row in testset:
        answer, contexts = my_rag_pipeline(row["question"])
        context_text = "\n".join(contexts)
        base = overlap_score(row["ground_truth"], context_text)
        answer_rel = overlap_score(row["question"], answer + " " + context_text)
        rows.append(
            {
                "question": row["question"],
                "answer": answer,
                "contexts": json.dumps(contexts, ensure_ascii=False),
                "ground_truth": row["ground_truth"],
                "evolution_type": row.get("evolution_type", ""),
                "faithfulness": base,
                "answer_relevancy": answer_rel,
                "context_precision": base,
                "context_recall": overlap_score(context_text, row["ground_truth"]),
            }
        )

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    summary = {m: sum(float(r[m]) for r in rows) / len(rows) for m in METRICS}
    out_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def check_thresholds(summary: dict[str, float], thresholds: list[str]) -> None:
    failures = []
    for item in thresholds:
        name, value = item.split("=", 1)
        if summary.get(name, 0.0) < float(value):
            failures.append(f"{name}={summary.get(name, 0.0):.3f} < {value}")
    if failures:
        raise SystemExit("Eval gate failed: " + "; ".join(failures))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--testset", type=Path, default=ROOT / "phase-a" / "testset_v1.csv")
    parser.add_argument("--out-csv", type=Path, default=ROOT / "phase-a" / "ragas_results.csv")
    parser.add_argument("--out-json", type=Path, default=ROOT / "phase-a" / "ragas_summary.json")
    parser.add_argument("--threshold", action="append", default=[])
    args = parser.parse_args()
    summary = run_offline_eval(args.testset, args.out_csv, args.out_json)
    print(json.dumps(summary, indent=2))
    if args.threshold:
        check_thresholds(summary, args.threshold)


if __name__ == "__main__":
    main()

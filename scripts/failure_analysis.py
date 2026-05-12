from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METRICS = ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]


def cluster(row: dict[str, str | float]) -> str:
    if float(row["context_recall"]) < 0.5:
        return "C1: Retrieval recall gap"
    if float(row["context_precision"]) < 0.5:
        return "C2: Noisy or off-topic contexts"
    return "C3: Answer synthesis gap"


def main() -> None:
    results_path = ROOT / "phase-a" / "ragas_results.csv"
    out_path = ROOT / "phase-a" / "failure_analysis.md"
    with results_path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["avg"] = sum(float(row[m]) for m in METRICS) / len(METRICS)
        row["cluster"] = cluster(row)
    bottom = sorted(rows, key=lambda r: float(r["avg"]))[:10]

    lines = ["# Failure Cluster Analysis", "", "## Bottom 10 Questions", ""]
    lines.append("| # | Question | Type | F | AR | CP | CR | Avg | Cluster |")
    lines.append("|---|---|---|---:|---:|---:|---:|---:|---|")
    for i, row in enumerate(bottom, start=1):
        q = str(row["question"]).replace("|", " ")[:90]
        lines.append(
            f"| {i} | {q} | {row.get('evolution_type', '')} | {float(row['faithfulness']):.2f} | "
            f"{float(row['answer_relevancy']):.2f} | {float(row['context_precision']):.2f} | "
            f"{float(row['context_recall']):.2f} | {float(row['avg']):.2f} | {row['cluster']} |"
        )

    lines.extend(
        [
            "",
            "## Clusters Identified",
            "",
            "### C1: Retrieval recall gap",
            "Pattern: required evidence is missing from retrieved contexts.",
            "Proposed fix: increase top_k, add hybrid BM25 + vector retrieval, and add a reranker.",
            "",
            "### C2: Noisy or off-topic contexts",
            "Pattern: retriever returns context that overlaps lexically but is not the answer evidence.",
            "Proposed fix: improve chunking, add metadata filters, and rerank by cross-encoder relevance.",
            "",
            "### C3: Answer synthesis gap",
            "Pattern: context is available but answer is incomplete or too generic.",
            "Proposed fix: tighten the generation prompt and require grounded citations from retrieved chunks.",
        ]
    )
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()

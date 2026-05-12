from __future__ import annotations

import argparse
import csv
from pathlib import Path

from rag_adapter import load_docs


ROOT = Path(__file__).resolve().parents[1]


def _sentences(text: str) -> list[str]:
    raw = text.replace("\n", " ").split(".")
    return [s.strip() for s in raw if len(s.split()) >= 8]


def generate_offline_testset(size: int, output: Path) -> None:
    docs = load_docs()
    if not docs:
        docs = [
            "Placeholder corpus. Add real markdown or text files under docs before final evaluation.",
            "This offline row exists only to verify that the lab pipeline runs end to end.",
        ]

    rows = []
    distribution = [("simple", 0.50), ("reasoning", 0.25), ("multi_context", 0.25)]
    counts = {name: int(size * ratio) for name, ratio in distribution}
    counts["simple"] += size - sum(counts.values())

    all_sentences = []
    for doc in docs:
        all_sentences.extend(_sentences(doc) or [doc[:300]])

    idx = 0
    for evolution_type, count in counts.items():
        for _ in range(count):
            context = all_sentences[idx % len(all_sentences)]
            if evolution_type == "simple":
                question = f"What is the main point of this passage: {context[:80]}?"
            elif evolution_type == "reasoning":
                question = f"What can be inferred from this passage: {context[:80]}?"
            else:
                other = all_sentences[(idx + 1) % len(all_sentences)]
                question = f"How are these two passages related: {context[:50]} / {other[:50]}?"
                context = f"{context}\n---\n{other}"
            rows.append(
                {
                    "question": question,
                    "ground_truth": context[:500],
                    "contexts": context[:1000],
                    "evolution_type": evolution_type,
                }
            )
            idx += 1

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["question", "ground_truth", "contexts", "evolution_type"])
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=50)
    parser.add_argument("--output", type=Path, default=ROOT / "phase-a" / "testset_v1.csv")
    args = parser.parse_args()
    generate_offline_testset(args.size, args.output)
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

JUDGE_PROMPT = """
You are an impartial evaluator.

Compare two answers to the same question.

Question: {question}

Answer A: {answer_a}

Answer B: {answer_b}

Rate based on factual accuracy, relevance, and conciseness.
Output JSON only: {{"winner": "A" or "B" or "tie", "reason": "..."}}
""".strip()

ABSOLUTE_PROMPT = """
Score the answer on 4 dimensions, each 1-5 scale:
accuracy, relevance, conciseness, helpfulness.

Question: {question}
Answer: {answer}

Output JSON only:
{{"accuracy": int, "relevance": int, "conciseness": int, "helpfulness": int, "overall": float}}
""".strip()


def parse_judge_output(text: str) -> dict:
    try:
        cleaned = text.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"winner": "tie", "reason": "Parse error"}


def heuristic_pairwise(question: str, answer_a: str, answer_b: str) -> dict:
    # Offline deterministic judge for pipeline testing. Replace with LLM call for final run.
    len_a = len(str(answer_a).split())
    len_b = len(str(answer_b).split())
    q_terms = {w.lower().strip(".,:;!?") for w in str(question).split() if len(w) > 2}
    score_a = len(q_terms & set(str(answer_a).lower().split())) + min(len_a, 120) / 120
    score_b = len(q_terms & set(str(answer_b).lower().split())) + min(len_b, 120) / 120
    if abs(score_a - score_b) < 0.05:
        return {"winner": "tie", "reason": "Similar heuristic score"}
    return {"winner": "A" if score_a > score_b else "B", "reason": "Higher heuristic relevance score"}


def flip_winner(winner: str) -> str:
    if winner == "A":
        return "B"
    if winner == "B":
        return "A"
    return "tie"


def pairwise_judge_with_swap(question: str, ans1: str, ans2: str) -> tuple[str, dict, dict]:
    run1 = heuristic_pairwise(question, ans1, ans2)
    run2_raw = heuristic_pairwise(question, ans2, ans1)
    run2 = {**run2_raw, "winner": flip_winner(run2_raw["winner"])}
    final = run1["winner"] if run1["winner"] == run2["winner"] else "tie"
    return final, run1, run2


def absolute_score(question: str, answer: str) -> dict:
    q_terms = {w.lower().strip(".,:;!?") for w in str(question).split() if len(w) > 2}
    answer_terms = set(str(answer).lower().split())
    relevance = 5 if q_terms & answer_terms else 3
    conciseness = 5 if len(str(answer).split()) <= 120 else 3
    accuracy = 3
    helpfulness = max(3, min(5, relevance))
    overall = (accuracy + relevance + conciseness + helpfulness) / 4
    return {
        "accuracy": accuracy,
        "relevance": relevance,
        "conciseness": conciseness,
        "helpfulness": helpfulness,
        "overall": overall,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ragas", type=Path, default=ROOT / "phase-a" / "ragas_results.csv")
    parser.add_argument("--limit", type=int, default=30)
    args = parser.parse_args()

    with args.ragas.open("r", encoding="utf-8", newline="") as f:
        df = list(csv.DictReader(f))[: args.limit]
    pairwise_rows = []
    absolute_rows = []
    for i, row in enumerate(df):
        answer_a = str(row["answer"])
        answer_b = answer_a + " " + " ".join(str(row["contexts"]).split()[:30])
        final, run1, run2 = pairwise_judge_with_swap(row["question"], answer_a, answer_b)
        pairwise_rows.append(
            {
                "question_id": i,
                "question": row["question"],
                "answer_a": answer_a,
                "answer_b": answer_b,
                "run1_winner": run1["winner"],
                "run2_winner": run2["winner"],
                "winner_after_swap": final,
            }
        )
        absolute_rows.append({"question_id": i, "question": row["question"], **absolute_score(row["question"], answer_a)})

    with (ROOT / "phase-b" / "pairwise_results.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(pairwise_rows[0].keys()))
        writer.writeheader()
        writer.writerows(pairwise_rows)
    with (ROOT / "phase-b" / "absolute_scores.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(absolute_rows[0].keys()))
        writer.writeheader()
        writer.writerows(absolute_rows)
    print("wrote phase-b/pairwise_results.csv and phase-b/absolute_scores.csv")


if __name__ == "__main__":
    main()

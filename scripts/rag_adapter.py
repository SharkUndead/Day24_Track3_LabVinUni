from __future__ import annotations

from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"


def load_docs(docs_dir: Path = DOCS_DIR) -> list[str]:
    texts: list[str] = []
    for pattern in ("*.md", "*.txt"):
        for path in docs_dir.rglob(pattern):
            if path.name == ".gitkeep":
                continue
            text = path.read_text(encoding="utf-8", errors="ignore").strip()
            if text:
                texts.append(text)
    return texts


def retrieve_contexts(question: str, docs: Iterable[str] | None = None, top_k: int = 3) -> list[str]:
    """Small lexical retriever used until the Day 18 RAG module is plugged in."""
    docs = list(docs if docs is not None else load_docs())
    if not docs:
        return ["No document corpus found. Add .md or .txt files under docs/."]

    q_terms = {w.lower().strip(".,:;!?()[]{}") for w in question.split() if len(w) > 2}
    scored: list[tuple[int, str]] = []
    for doc in docs:
        words = {w.lower().strip(".,:;!?()[]{}") for w in doc.split()}
        score = len(q_terms & words)
        scored.append((score, doc[:1200]))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def my_rag_pipeline(question: str, top_k: int = 3) -> tuple[str, list[str]]:
    """
    Adapter entrypoint for all lab scripts.

    Replace this function body with your Day 18 RAG pipeline when available.
    It must return: (answer: str, contexts: list[str]).
    """
    contexts = retrieve_contexts(question, top_k=top_k)
    answer = (
        "Offline baseline answer based on retrieved context. "
        "Replace scripts/rag_adapter.py::my_rag_pipeline with the Day 18 RAG pipeline."
    )
    return answer, contexts

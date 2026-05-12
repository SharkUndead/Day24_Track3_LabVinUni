from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
DEFAULT_DAY18_RAG_PATH = Path(r"D:\VinUni_proJect_day\day 18\Day18-Track3-Production-RAG")
_DAY18_RAG = None
_DAY18_RAG_ERROR = None


def _env_enabled(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def _load_day18_rag():
    """Load the Day 18 ProductionRAG lazily when explicitly enabled."""
    global _DAY18_RAG, _DAY18_RAG_ERROR
    if _DAY18_RAG is not None:
        return _DAY18_RAG
    if _DAY18_RAG_ERROR is not None:
        return None

    day18_path = Path(os.getenv("DAY18_RAG_PATH", str(DEFAULT_DAY18_RAG_PATH)))
    if not day18_path.exists():
        _DAY18_RAG_ERROR = f"Day 18 path not found: {day18_path}"
        return None

    try:
        sys.path.insert(0, str(day18_path))
        from src.pipeline import ProductionRAG

        rag = ProductionRAG()
        rag.index_documents()
        _DAY18_RAG = rag
        return _DAY18_RAG
    except Exception as exc:
        _DAY18_RAG_ERROR = f"{type(exc).__name__}: {exc}"
        return None


def load_docs(docs_dir: Path = DOCS_DIR) -> list[str]:
    texts: list[str] = []
    for pattern in ("*.md", "*.txt"):
        for path in docs_dir.rglob(pattern):
            if path.name == ".gitkeep":
                continue
            text = path.read_text(encoding="utf-8", errors="ignore").strip()
            if text:
                texts.append(text)
    if not texts:
        readme = ROOT / "README.md"
        if readme.exists():
            texts.append(readme.read_text(encoding="utf-8", errors="ignore"))
    return texts


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 120) -> list[str]:
    words = text.split()
    if not words:
        return []
    chunks = []
    step = max(1, chunk_size - overlap)
    for start in range(0, len(words), step):
        chunk = " ".join(words[start : start + chunk_size]).strip()
        if chunk:
            chunks.append(chunk)
    return chunks


def tokenize(text: str) -> set[str]:
    stopwords = {
        "the",
        "and",
        "for",
        "with",
        "this",
        "that",
        "from",
        "what",
        "how",
        "are",
        "you",
        "your",
        "cua",
        "voi",
        "cho",
        "mot",
        "cac",
        "can",
        "duoc",
        "trong",
        "phase",
        "passage",
    }
    return {
        w.lower().strip(".,:;!?()[]{}\"'`")
        for w in text.split()
        if len(w.strip(".,:;!?()[]{}\"'`")) > 2 and w.lower().strip(".,:;!?()[]{}\"'`") not in stopwords
    }


def retrieve_contexts(question: str, docs: Iterable[str] | None = None, top_k: int = 3) -> list[str]:
    """Small lexical retriever used until the Day 18 RAG module is plugged in."""
    docs = list(docs if docs is not None else load_docs())
    if not docs:
        return ["No document corpus found. Add .md or .txt files under docs/."]

    q_terms = tokenize(question)
    chunks = []
    for doc in docs:
        chunks.extend(chunk_text(doc))

    scored: list[tuple[float, str]] = []
    for chunk in chunks:
        words = tokenize(chunk)
        score = len(q_terms & words)
        if q_terms:
            score += len(q_terms & words) / len(q_terms)
        scored.append((score, chunk[:1400]))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def synthesize_answer(question: str, contexts: list[str]) -> str:
    q_terms = tokenize(question)
    sentences: list[str] = []
    for context in contexts:
        for raw in context.replace("\n", " ").split("."):
            sentence = raw.strip()
            if len(sentence.split()) < 6:
                continue
            score = len(q_terms & tokenize(sentence))
            if score > 0:
                sentences.append(sentence)
    if not sentences:
        sentences = [contexts[0].replace("\n", " ")[:500]]
    selected = sentences[:3]
    return " ".join(selected).strip()


def my_rag_pipeline(question: str, top_k: int = 3) -> tuple[str, list[str]]:
    """
    Adapter entrypoint for all lab scripts.

    Replace this function body with your Day 18 RAG pipeline when available.
    It must return: (answer: str, contexts: list[str]).
    """
    if _env_enabled("USE_DAY18_RAG"):
        day18_rag = _load_day18_rag()
        if day18_rag is not None:
            answer, contexts = day18_rag.query(question, top_k_rerank=top_k)
            if contexts and "Search" not in answer and "thất bại" not in answer:
                return answer, contexts

    contexts = retrieve_contexts(question, top_k=top_k)
    answer = synthesize_answer(question, contexts)
    if _env_enabled("USE_DAY18_RAG") and _DAY18_RAG_ERROR:
        answer = f"{answer}\n\n[Day18 fallback active: {_DAY18_RAG_ERROR}]"
    return answer, contexts

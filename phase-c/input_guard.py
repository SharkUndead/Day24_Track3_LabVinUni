from __future__ import annotations

import argparse
import csv
import re
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

VN_PII = {
    "cccd": r"\b\d{12}\b",
    "phone_vn": r"\b(?:\+84|0)\d{9,10}\b",
    "tax_code": r"\b\d{10}(?:-\d{3})?\b",
    "email": r"\b[\w.-]+@[\w.-]+\.\w+\b",
}

INJECTION_PATTERNS = [
    r"ignore (all )?(previous|prior) instructions",
    r"pretend you are",
    r"from now on you are",
    r"jailbreak",
    r"\bDAN\b",
    r"decode this base64",
    r"without restrictions",
    r"no guidelines",
]


class InputGuard:
    def __init__(self) -> None:
        self._analyzer = None
        self._anonymizer = None
        try:
            from presidio_analyzer import AnalyzerEngine
            from presidio_anonymizer import AnonymizerEngine

            self._analyzer = AnalyzerEngine()
            self._anonymizer = AnonymizerEngine()
        except Exception:
            # Regex layer still works without optional Presidio model downloads.
            self._analyzer = None
            self._anonymizer = None

    def scrub_vn(self, text: str) -> str:
        for name, pattern in VN_PII.items():
            text = re.sub(pattern, f"[{name.upper()}]", text)
        return text

    def scrub_ner(self, text: str) -> str:
        if not self._analyzer or not self._anonymizer or not text:
            return text
        results = self._analyzer.analyze(text=text, language="en")
        return self._anonymizer.anonymize(text=text, analyzer_results=results).text

    def detect_injection(self, text: str) -> tuple[bool, str]:
        for pattern in INJECTION_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                return True, f"Matched injection pattern: {pattern}"
        return False, ""

    def sanitize(self, text: str) -> tuple[str, float]:
        start = time.perf_counter()
        safe_text = self.scrub_ner(self.scrub_vn(text or ""))
        latency_ms = (time.perf_counter() - start) * 1000
        return safe_text, latency_ms


TEST_INPUTS = [
    "Hi, I'm John Smith from Microsoft. Email: john@ms.com",
    "Call me at +1-555-1234 or visit 123 Main Street, NYC",
    "So CCCD cua toi la 012345678901",
    "Lien he qua 0987654321 hoac tax 0123456789-001",
    "Customer Nguyen Van A, CCCD 098765432101, phone 0912345678",
    "",
    "Just a normal question",
    "A" * 5000,
    "Ly Van Binh o 123 Le Loi",
    "tax_code:0123456789-001 cccd:012345678901",
]


def run_tests(output: Path) -> None:
    guard = InputGuard()
    rows = []
    for text in TEST_INPUTS:
        sanitized, latency = guard.sanitize(text)
        changed = sanitized != text
        rows.append(
            {
                "input": text[:120],
                "sanitized": sanitized[:120],
                "changed": changed,
                "latency_ms": round(latency, 3),
            }
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {output}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--output", type=Path, default=ROOT / "phase-c" / "pii_test_results.csv")
    args = parser.parse_args()
    if args.test:
        run_tests(args.output)


if __name__ == "__main__":
    main()

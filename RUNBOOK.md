# Lab 24 Runbook

Dung PowerShell tai root repo.

## 0. Environment

Activate venv:

```powershell
.\.venv\Scripts\Activate.ps1
```

Neu policy chan activate script, dung truc tiep:

```powershell
.\.venv\Scripts\python --version
```

Ket qua hien tai:

```text
Python 3.11.5
```

Cai dependencies that:

```powershell
.\.venv\Scripts\python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

Trang thai hien tai: pip bi timeout/SSL tren may nay, nen scaffold scripts da duoc viet de smoke test bang standard library truoc. Khi mang/SSL on dinh, chay lai lenh pip tren.

## Phase A - RAGAS/Eval Smoke Test

Generate test set:

```powershell
.\.venv\Scripts\python scripts\generate_testset.py --size 50
```

Ket qua hien tai:

```text
wrote phase-a/testset_v1.csv
```

Run offline eval:

```powershell
.\.venv\Scripts\python scripts\run_eval.py
```

Ket qua hien tai voi placeholder corpus:

```json
{
  "faithfulness": 0.2064600000000001,
  "answer_relevancy": 0.21204000000000003,
  "context_precision": 0.2064600000000001,
  "context_recall": 0.2064600000000001
}
```

Phan tich failures:

```powershell
.\.venv\Scripts\python scripts\failure_analysis.py
```

Ket qua:

```text
wrote phase-a/failure_analysis.md
```

Luu y: Ket qua Phase A hien tai chi la smoke test. De nop that, can them corpus vao `docs/` va thay `scripts/rag_adapter.py::my_rag_pipeline` bang RAG Day 18.

## Phase B - Judge Smoke Test

Run pairwise judge va absolute scoring:

```powershell
.\.venv\Scripts\python phase-b\judge_pipeline.py --limit 30
```

Ket qua:

```text
wrote phase-b/pairwise_results.csv and phase-b/absolute_scores.csv
```

Tao file label va compute kappa:

```powershell
.\.venv\Scripts\python phase-b\calibration.py
.\.venv\Scripts\python phase-b\calibration.py
```

Ket qua hien tai:

```text
created phase-b/to_label.csv; fill human_labels.csv before computing kappa
created placeholder phase-b/human_labels.csv; replace labels for final submission
Cohen's kappa: 1.000
wrote phase-b/judge_bias_report.md
```

Luu y: `human_labels.csv` hien la placeholder. Khi nop that, mo `phase-b/to_label.csv`, tu danh nhan 10 cap, sua `human_labels.csv`, roi chay lai calibration.

## Phase C - Guardrails Smoke Test

PII tests:

```powershell
.\.venv\Scripts\python phase-c\input_guard.py --test
```

Ket qua:

```text
wrote phase-c/pii_test_results.csv
```

Output guard tests:

```powershell
.\.venv\Scripts\python phase-c\output_guard.py --test
```

Ket qua:

```text
wrote phase-c/output_guard_results.csv
```

Adversarial tests:

```powershell
.\.venv\Scripts\python phase-c\adversarial_tests.py
```

Ket qua hien tai:

```text
wrote phase-c/adversarial_test_results.csv
detection_rate=70.0%
false_positive_rate=0.0%
```

Latency benchmark:

```powershell
.\.venv\Scripts\python phase-c\full_pipeline.py --benchmark 20
```

Ket qua hien tai:

```text
wrote phase-c/latency_benchmark.csv
L1: P50=0.0ms P95=0.1ms P99=0.4ms
L2: P50=0.2ms P95=0.3ms P99=0.4ms
L3: P50=0.0ms P95=0.0ms P99=0.0ms
```

De dung benchmark nop bai, chay `--benchmark 100` sau khi gan RAG pipeline that.

## Phase D - Blueprint

File da tao:

```text
phase-d/blueprint.md
```

Can cap nhat lai bang metric/cost/latency that sau khi chay RAGAS va guardrails voi API/corpus that.

## Git

Repo da duoc `git init`.

Kiem tra status:

```powershell
git status --short
```

Commit moc scaffold:

```powershell
git add .
git commit -m "Scaffold lab 24 eval and guardrail system"
```

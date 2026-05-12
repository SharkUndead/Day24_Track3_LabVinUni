# TODO - Lab 24: Full Evaluation & Guardrail System

Muc tieu nop bai: GitHub repo dung cau truc, co evaluation cho RAG, LLM-as-Judge, guardrails stack, blueprint document va demo video 5 phut.

## 0. Chuan bi truoc khi code

- [ ] Lay/chen lai RAG pipeline tu Day 18 vao repo nay, dam bao chay duoc retrieval + generation.
- [ ] Them document corpus vao thu muc `docs/`, toi thieu 50 trang text/markdown.
- [ ] Tao moi truong Python 3.10+.
- [ ] Tao `requirements.txt` va pin versions cho cac package chinh: `ragas`, `datasets`, `langchain`, `langchain-openai`, `presidio-analyzer`, `presidio-anonymizer`, `guardrails-ai`, `transformers`, `scikit-learn`, `pandas`, `numpy`.
- [ ] Set API keys can thiet: OpenAI/Anthropic cho judge, HuggingFace hoac Groq cho Llama Guard, LangSmith/Langfuse neu dung logging.
- [ ] Verify setup:
  - [ ] `python --version` >= 3.10.
  - [ ] `ragas` version >= 0.2.0.
  - [ ] RAG pipeline tra loi duoc mot query test.
- [ ] Khoi tao git repo va commit tung moc lon.

## 1. Tao cau truc repo bat buoc

- [ ] Tao cac folder:
  - [ ] `phase-a/`
  - [ ] `phase-b/`
  - [ ] `phase-c/`
  - [ ] `phase-d/`
  - [ ] `.github/workflows/`
  - [ ] `demo/`
- [ ] Tao file goc:
  - [ ] `README.md`
  - [ ] `requirements.txt`
  - [ ] `prompts.md`

## 2. Phase A - RAGAS Evaluation (30 diem)

### A.1 Synthetic test set

- [ ] Viet script generate test set 50 questions tu `docs/`.
- [ ] Dam bao distribution:
  - [ ] 50% simple/single-hop.
  - [ ] 25% reasoning/multi-step.
  - [ ] 25% multi-context/cross-document.
- [ ] Luu output vao `phase-a/testset_v1.csv`.
- [ ] File CSV co du cac cot:
  - [ ] `question`
  - [ ] `ground_truth`
  - [ ] `contexts`
  - [ ] `evolution_type`
- [ ] Kiem tra distribution bang `value_counts()`.
- [ ] Review thu cong it nhat 10 questions.
- [ ] Chinh sua it nhat 1 question neu can.
- [ ] Ghi review vao `phase-a/testset_review_notes.md`.

### A.2 Run RAGAS 4 metrics

- [ ] Chay RAG pipeline tren 50 questions.
- [ ] Evaluate bang 4 metrics:
  - [ ] Faithfulness.
  - [ ] Answer Relevancy.
  - [ ] Context Precision.
  - [ ] Context Recall.
- [ ] Luu ket qua tung row vao `phase-a/ragas_results.csv`.
- [ ] Luu aggregate scores vao `phase-a/ragas_summary.json`.
- [ ] Ghi total eval cost vao README.
- [ ] Neu metric nao < 0.5, ghi observation va nguyen nhan co the vao README.

### A.3 Failure cluster analysis

- [ ] Tinh average score cua 4 metrics cho tung question.
- [ ] Lay bottom 10 questions diem thap nhat.
- [ ] Viet `phase-a/failure_analysis.md` gom:
  - [ ] Bang bottom 10 co question, type, F, AR, CP, CR, Avg, cluster.
  - [ ] It nhat 2 failure clusters rieng biet.
  - [ ] Moi cluster co it nhat 2 example questions.
  - [ ] Moi cluster co root cause va proposed fix cu the ve ky thuat.

### A.4 CI/CD eval gate

- [ ] Tao `.github/workflows/eval-gate.yml`.
- [ ] Workflow co cac buoc checkout, setup Python, install dependencies.
- [ ] Workflow chay script eval voi threshold gate.
- [ ] Workflow upload artifact `ragas_results.csv`.
- [ ] Tao script tuong ung, vi du `scripts/run_eval.py`, de workflow goi duoc.

## 3. Phase B - LLM-as-Judge & Calibration (25 diem)

### B.1 Pairwise judge pipeline

- [ ] Tao 2 versions cau tra loi RAG de so sanh, vi du baseline va version co reranker/top_k moi.
- [ ] Implement judge prompt so sanh Answer A va Answer B.
- [ ] Implement robust JSON parser co fallback khi parse loi.
- [ ] Implement swap-and-average de giam position bias.
- [ ] Chay tren it nhat 30 questions.
- [ ] Luu `phase-b/pairwise_results.csv` voi cac cot:
  - [ ] `question`
  - [ ] `answer_a`
  - [ ] `answer_b`
  - [ ] `run1_winner`
  - [ ] `run2_winner`
  - [ ] `winner_after_swap`

### B.2 Absolute scoring

- [ ] Implement rubric 4 dimensions, moi dimension score 1-5:
  - [ ] Factual accuracy.
  - [ ] Relevance.
  - [ ] Conciseness.
  - [ ] Helpfulness.
- [ ] Tinh `overall` = average cua 4 dimensions.
- [ ] Chay tren it nhat 30 questions.
- [ ] Luu `phase-b/absolute_scores.csv`.

### B.3 Human calibration

- [ ] Sample 10 cap tu `pairwise_results.csv`.
- [ ] Tao `phase-b/to_label.csv` de human label.
- [ ] Tu label 10 cap va luu `phase-b/human_labels.csv`.
- [ ] `human_labels.csv` co:
  - [ ] `question_id`
  - [ ] `human_winner`
  - [ ] `confidence`
  - [ ] `notes`
- [ ] Compute Cohen's kappa giua human labels va judge labels.
- [ ] Luu notebook hoac script phan tich vao `phase-b/kappa_analysis.ipynb`.
- [ ] Ghi interpretation kappa.
- [ ] Neu kappa < 0.6, viet root cause analysis.

### B.4 Bias observations

- [ ] Do position bias: A thang bao nhieu lan khi nam truoc.
- [ ] Do them it nhat 1 bias khac, vi du length bias hoac verbosity bias.
- [ ] Tao `phase-b/judge_bias_report.md`.
- [ ] Bao cao co it nhat 2 biases va co table/chart.

## 4. Phase C - Guardrails Stack (35 diem)

### C.1 Input guardrail: PII redaction

- [ ] Implement `phase-c/input_guard.py`.
- [ ] Dung Presidio + custom regex cho Vietnam PII:
  - [ ] CCCD 12 so.
  - [ ] SDT Viet Nam.
  - [ ] Ma so thue.
  - [ ] Email.
- [ ] Test voi 10 inputs bat buoc trong README.
- [ ] Handle edge cases:
  - [ ] Empty input.
  - [ ] Long input.
  - [ ] Multilingual input.
- [ ] Dat detection/recall >= 80%.
- [ ] Dat latency P95 < 50ms.
- [ ] Luu `phase-c/pii_test_results.csv`.

### C.2 Topic scope validator

- [ ] Chon 1 cach implement:
  - [ ] Embedding similarity.
  - [ ] LLM zero-shot.
  - [ ] Guardrails AI ValidTopic.
- [ ] Dinh nghia allowed topics theo domain cua RAG corpus.
- [ ] Test voi 20 inputs:
  - [ ] 10 on-topic.
  - [ ] 10 off-topic.
- [ ] Dat accuracy >= 75%; muc excellent >= 95%.
- [ ] Do va document refuse rate trong README.
- [ ] Viet fallback message lich su khi off-topic, khong chi tra ve `rejected`.

### C.3 Adversarial testing

- [ ] Build 20 adversarial inputs:
  - [ ] 5 DAN variants.
  - [ ] 5 role-play attacks.
  - [ ] 3 payload splitting attacks.
  - [ ] 3 encoding attacks.
  - [ ] 4 indirect injection examples trong RAG content.
- [ ] Test input guardrail tren 20 attacks.
- [ ] Dat detection rate >= 70%; muc excellent >= 95%.
- [ ] Test false positive tren 10 legitimate queries, yeu cau <= 10%.
- [ ] Luu `phase-c/adversarial_test_results.csv`.

### C.4 Output guardrail: Llama Guard 3

- [ ] Implement `phase-c/output_guard.py`.
- [ ] Chon cach deploy:
  - [ ] Self-hosted neu co GPU.
  - [ ] API-based qua Groq neu khong co GPU.
- [ ] Return duoc `safe` / `unsafe`.
- [ ] Test voi 10 unsafe outputs.
- [ ] Test voi 10 safe outputs.
- [ ] Dat unsafe detection >= 80%.
- [ ] Dat false positive <= 20%.
- [ ] Do latency P95 va document trong README.

### C.5 Full stack integration & latency benchmark

- [ ] Implement `phase-c/full_pipeline.py`.
- [ ] Pipeline gom:
  - [ ] L1 input guards: PII, topic validator, injection detection.
  - [ ] L2 Day 18 RAG pipeline.
  - [ ] L3 output guard: Llama Guard 3.
  - [ ] L4 async audit log.
- [ ] Chay end-to-end duoc voi query that.
- [ ] Benchmark >= 100 requests.
- [ ] Luu `phase-c/latency_benchmark.csv`.
- [ ] Report P50, P95, P99 cho L1, L2, L3.
- [ ] Dat L1 P95 < 50ms.
- [ ] Dat L3 P95 < 100ms.
- [ ] Document total overhead vs baseline RAG trong README.

## 5. Phase D - Blueprint Document (10 diem)

- [ ] Tao `phase-d/blueprint.md`, dai khoang 4-6 trang.
- [ ] Section SLO:
  - [ ] Dinh nghia it nhat 5 SLOs.
  - [ ] Moi SLO co target, alert threshold, severity.
- [ ] Section architecture:
  - [ ] Co diagram Mermaid/draw.io.
  - [ ] Show defense-in-depth 4 layers.
  - [ ] Label ro Presidio, topic guard, RAG, Llama Guard, audit log.
  - [ ] Co latency annotation moi layer.
- [ ] Section alert playbook:
  - [ ] It nhat 3 incidents.
  - [ ] Moi incident co severity, detection, likely causes, investigation steps, resolution, SLO impact.
- [ ] Section cost analysis:
  - [ ] Monthly cost projection.
  - [ ] Assumptions ro rang, vi du 100k queries/month.
  - [ ] Cost optimization opportunities.

## 6. README, prompts va submission

- [ ] Cap nhat README project theo template:
  - [ ] Overview 200-300 tu.
  - [ ] Setup instructions.
  - [ ] Results Summary Phase A.
  - [ ] Results Summary Phase B.
  - [ ] Results Summary Phase C.
  - [ ] Link toi `phase-d/blueprint.md`.
  - [ ] Lessons learned 2-3 paragraphs.
  - [ ] Demo video link hoac local path.
- [ ] Ghi tat ca prompt dung cho RAGAS/judge/guardrails vao `prompts.md`.
- [ ] Dam bao `requirements.txt` pinned versions.
- [ ] Dam bao repo structure khop template submission.
- [ ] Push len GitHub voi commit history ro rang.

## 7. Demo video 5 phut

- [ ] Quay RAGAS chay live tren 5 questions, khoang 1 phut.
- [ ] Quay LLM-Judge so sanh 2 versions, khoang 1 phut.
- [ ] Quay adversarial tests voi 3 attacks:
  - [ ] DAN.
  - [ ] Jailbreak.
  - [ ] PII.
- [ ] Show guardrail block/refuse dung, khoang 2 phut.
- [ ] Show latency benchmark output:
  - [ ] P50.
  - [ ] P95.
  - [ ] P99.
- [ ] Upload demo vao `demo/demo-video.mp4` hoac YouTube unlisted.

## 8. Bonus neu con thoi gian

- [ ] Chon 1-3 bonus phu hop, khong lam dan trai.
- [ ] De xuat uu tien:
  - [ ] Prompt Guard/Meta injection classifier (+2, de).
  - [ ] Eval dashboard bang Streamlit/Gradio (+3, medium).
  - [ ] Cross-judge protocol voi 2+ judge models (+3, medium).
- [ ] Document bonus trong README va demo neu co.

## Definition of Done

- [ ] Tat ca file bat buoc trong submission tree ton tai.
- [ ] Tat ca CSV/JSON/MD output duoc generate that, khong phai placeholder.
- [ ] Metrics, latency va cost duoc ghi ro trong README.
- [ ] Demo video chay du 4 noi dung bat buoc.
- [ ] Repo co commit history ro rang va san sang submit.

# Failure Cluster Analysis

## Bottom 10 Questions

| # | Question | Type | F | AR | CP | CR | Avg | Cluster |
|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | What is the main point of this passage: ## General rules  Employees should wear profession | simple | 0.22 | 0.14 | 0.22 | 0.22 | 0.20 | C1: Retrieval recall gap |
| 2 | How are these two passages related: 10  # Check key packages pip list   grep -E "ragas / 0 | multi_context | 0.28 | 0.11 | 0.28 | 0.28 | 0.24 | C1: Retrieval recall gap |
| 3 | How are these two passages related: 0  # Check API keys are set echo $OPENAI_API_KEY   / t | multi_context | 0.29 | 0.21 | 0.29 | 0.29 | 0.27 | C1: Retrieval recall gap |
| 4 | How are these two passages related: 10+, đã cài đặt các package cần thiết * [ ] LangSm / 1 | multi_context | 0.34 | 0.19 | 0.34 | 0.34 | 0.30 | C1: Retrieval recall gap |
| 5 | What is the main point of this passage: Requests for peripherals such as mouse, keyboard,  | simple | 0.35 | 0.20 | 0.35 | 0.35 | 0.31 | C1: Retrieval recall gap |
| 6 | What is the main point of this passage: ## Insurance and health  The company pays compulso | simple | 0.36 | 0.21 | 0.36 | 0.36 | 0.33 | C1: Retrieval recall gap |
| 7 | How are these two passages related: Setup git repo trước — commit mỗi 30 phút / Đọc hết cả | multi_context | 0.37 | 0.24 | 0.37 | 0.37 | 0.34 | C1: Retrieval recall gap |
| 8 | How are these two passages related: 3 Cần chuẩn bị gì trước khi bắt đầu?  Bạn cần các  / 1 | multi_context | 0.34 | 0.40 | 0.34 | 0.34 | 0.35 | C1: Retrieval recall gap |
| 9 | How are these two passages related: test_query "What is X?" ```  Nếu bất kỳ check nào  / Đ | multi_context | 0.36 | 0.41 | 0.36 | 0.36 | 0.37 | C1: Retrieval recall gap |
| 10 | What is the main point of this passage: Female employees receive 6 months maternity leave  | simple | 0.40 | 0.31 | 0.40 | 0.40 | 0.38 | C1: Retrieval recall gap |

## Clusters Identified

### C1: Retrieval recall gap
Pattern: required evidence is missing from retrieved contexts.
Proposed fix: increase top_k, add hybrid BM25 + vector retrieval, and add a reranker.

### C2: Noisy or off-topic contexts
Pattern: retriever returns context that overlaps lexically but is not the answer evidence.
Proposed fix: improve chunking, add metadata filters, and rerank by cross-encoder relevance.

### C3: Answer synthesis gap
Pattern: context is available but answer is incomplete or too generic.
Proposed fix: tighten the generation prompt and require grounded citations from retrieved chunks.
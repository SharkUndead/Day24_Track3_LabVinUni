# Failure Cluster Analysis

## Bottom 10 Questions

| # | Question | Type | F | AR | CP | CR | Avg | Cluster |
|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | What can be inferred from this passage: This offline row exists only to verify that the la | reasoning | 0.00 | 0.18 | 0.00 | 0.00 | 0.04 | C1: Retrieval recall gap |
| 2 | What can be inferred from this passage: This offline row exists only to verify that the la | reasoning | 0.00 | 0.18 | 0.00 | 0.00 | 0.04 | C1: Retrieval recall gap |
| 3 | What can be inferred from this passage: This offline row exists only to verify that the la | reasoning | 0.00 | 0.18 | 0.00 | 0.00 | 0.04 | C1: Retrieval recall gap |
| 4 | What can be inferred from this passage: This offline row exists only to verify that the la | reasoning | 0.00 | 0.18 | 0.00 | 0.00 | 0.04 | C1: Retrieval recall gap |
| 5 | What can be inferred from this passage: This offline row exists only to verify that the la | reasoning | 0.00 | 0.18 | 0.00 | 0.00 | 0.04 | C1: Retrieval recall gap |
| 6 | What can be inferred from this passage: This offline row exists only to verify that the la | reasoning | 0.00 | 0.18 | 0.00 | 0.00 | 0.04 | C1: Retrieval recall gap |
| 7 | What is the main point of this passage: This offline row exists only to verify that the la | simple | 0.00 | 0.19 | 0.00 | 0.00 | 0.05 | C1: Retrieval recall gap |
| 8 | What is the main point of this passage: This offline row exists only to verify that the la | simple | 0.00 | 0.19 | 0.00 | 0.00 | 0.05 | C1: Retrieval recall gap |
| 9 | What is the main point of this passage: This offline row exists only to verify that the la | simple | 0.00 | 0.19 | 0.00 | 0.00 | 0.05 | C1: Retrieval recall gap |
| 10 | What is the main point of this passage: This offline row exists only to verify that the la | simple | 0.00 | 0.19 | 0.00 | 0.00 | 0.05 | C1: Retrieval recall gap |

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
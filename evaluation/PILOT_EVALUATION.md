# Pilot Evaluation Results

This pilot uses three built-in public benchmark datasets from scikit-learn to exercise the real agent loop: dataset upload context, LLM-generated Python code, backend execution, generated artifacts, and final answer production.

## Summary

- Cases: 3
- Completed workflows without manual code editing: 3/3
- Code generation success: 3/3
- Code execution success: 3/3
- Final answer completion: 3/3
- Generated artifacts: 5
- Median runtime: 33.53 seconds

## Case Results

| Dataset | Rows | Columns | Code | Execute | Answer | Artifacts | Runtime (s) |
|---|---:|---:|---|---|---|---:|---:|
| iris | 150 | 5 | True | True | True | 2 | 34.51 |
| diabetes | 442 | 11 | True | True | True | 2 | 33.53 |
| breast_cancer | 569 | 31 | True | True | True | 1 | 9.9 |

## Paper-Ready Result Statement

In a preliminary prototype evaluation across three public benchmark datasets, Data Discovery Agent completed 3/3 autonomous analysis workflows without manual code editing, generated executable Python analysis code in 3/3 cases, executed code successfully in 3/3 cases, and produced final analytical answers in 3/3 cases, with a median runtime of 33.53 seconds.

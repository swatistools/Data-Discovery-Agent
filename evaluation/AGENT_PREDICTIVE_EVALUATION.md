# Agent-Generated Predictive Evaluation

This evaluation runs the real Data Discovery Agent loop. The LLM is prompted to generate and execute predictive evaluation code, then report metrics. Reported metrics are compared with deterministic reference outputs.

The compact CSV version of these values is available in `evaluation_results.csv`.

## Summary

- Agent workflows completed: 3/3
- JSON metric reports found: 3/3
- Metric checks passed: 9/9
- Metric correctness rate: 1.0
- Cases with all metrics matched: 3/3

## Case Results

| Dataset | Workflow | JSON | Metrics Passed | Runtime (s) |
|---|---:|---:|---:|---:|
| iris | True | True | 3/3 | 5.47 |
| diabetes | True | True | 3/3 | 9.05 |
| breast_cancer | True | True | 3/3 | 4.92 |

## Metric Comparisons

### iris

| Metric | Agent | Reference | Difference | Passed |
|---|---:|---:|---:|---:|
| accuracy | 0.933 | 0.9333 | 0.0003 | True |
| f1_macro | 0.933 | 0.9333 | 0.0003 | True |
| error_rate | 0.067 | 0.0667 | 0.0003 | True |

### diabetes

| Metric | Agent | Reference | Difference | Passed |
|---|---:|---:|---:|---:|
| r2 | 0.4526 | 0.4526 | 3e-06 | True |
| rmse | 53.8534 | 53.8534 | 4.6e-05 | True |
| mae | 42.7941 | 42.7941 | 5e-06 | True |

### breast_cancer

| Metric | Agent | Reference | Difference | Passed |
|---|---:|---:|---:|---:|
| accuracy | 0.9825 | 0.9825 | 0.0 | True |
| f1_macro | 0.9812 | 0.9812 | 0.0 | True |
| error_rate | 0.0175 | 0.0175 | 0.0 | True |

## Paper-Ready Wording

In an agent-generated predictive evaluation, the real Data Discovery Agent workflow completed 3/3 benchmark workflows and produced machine-readable metric reports in 3/3 cases. Compared against deterministic reference pipelines, 9/9 reported metrics matched within a tolerance of 0.001, yielding a metric correctness rate of 1.0.

# Predictive and Statistical Correctness Evaluation

This evaluation adds reference predictive metrics and statistical correctness checks for the three public scikit-learn benchmark datasets used in the pilot study. These results should be reported as benchmark/reference analysis results, not as LLM training accuracy.

## Predictive Results

| Dataset | Task | Model | Accuracy | F1 Macro | Error Rate | R2 | RMSE | MAE |
|---|---|---|---:|---:|---:|---:|---:|---:|
| iris | classification | StandardScaler + LogisticRegression | 0.9333 | 0.9333 | 0.0667 | N/A | N/A | N/A |
| diabetes | regression | StandardScaler + LinearRegression | N/A | N/A | N/A | 0.4526 | 53.8534 | 42.7941 |
| breast_cancer | classification | StandardScaler + LogisticRegression | 0.9825 | 0.9812 | 0.0175 | N/A | N/A | N/A |

## Summary

- Mean classification accuracy: 0.9579
- Mean classification F1 macro: 0.9572
- Mean classification error rate: 0.0421
- Statistical correctness checks: 9/9
- Statistical correctness rate: 1.0

## Paper-Ready Wording

Using deterministic reference pipelines with an 80/20 train-test split, the classification benchmarks achieved a mean accuracy of 0.9579, mean macro-F1 of 0.9572, and mean error rate of 0.0421 across Iris and Breast Cancer Wisconsin. On the Diabetes regression dataset, the reference pipeline achieved an R2 of 0.4526, RMSE of 53.8534, and MAE of 42.7941. Dataset metadata checks against scikit-learn reference values passed 9/9 checks, giving a statistical correctness rate of 1.0.

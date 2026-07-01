from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from sklearn.datasets import load_breast_cancer, load_diabetes, load_iris
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "evaluation"
RANDOM_STATE = 42
TEST_SIZE = 0.2


def _classification_case(name: str, loader) -> dict:
    data = loader()
    x_train, x_test, y_train, y_test = train_test_split(
        data.data,
        data.target,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=data.target,
    )
    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
    )
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)

    return {
        "dataset": name,
        "task_type": "classification",
        "rows": int(data.data.shape[0]),
        "columns": int(data.data.shape[1] + 1),
        "feature_columns": int(data.data.shape[1]),
        "target_classes": int(len(np.unique(data.target))),
        "test_size": TEST_SIZE,
        "model": "StandardScaler + LogisticRegression",
        "accuracy": round(float(accuracy), 4),
        "f1_macro": round(float(f1_score(y_test, predictions, average="macro")), 4),
        "f1_weighted": round(float(f1_score(y_test, predictions, average="weighted")), 4),
        "error_rate": round(float(1 - accuracy), 4),
    }


def _regression_case() -> dict:
    data = load_diabetes()
    x_train, x_test, y_train, y_test = train_test_split(
        data.data,
        data.target,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )
    model = make_pipeline(StandardScaler(), LinearRegression())
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    rmse = float(np.sqrt(mean_squared_error(y_test, predictions)))

    return {
        "dataset": "diabetes",
        "task_type": "regression",
        "rows": int(data.data.shape[0]),
        "columns": int(data.data.shape[1] + 1),
        "feature_columns": int(data.data.shape[1]),
        "test_size": TEST_SIZE,
        "model": "StandardScaler + LinearRegression",
        "r2": round(float(r2_score(y_test, predictions)), 4),
        "rmse": round(float(rmse), 4),
        "mae": round(float(mean_absolute_error(y_test, predictions)), 4),
        "normalized_rmse": round(float(rmse / np.mean(y_test)), 4),
    }


def _statistical_correctness_checks(cases: list[dict]) -> dict:
    expected = {
        "iris": {"rows": 150, "columns": 5, "task_type": "classification"},
        "diabetes": {"rows": 442, "columns": 11, "task_type": "regression"},
        "breast_cancer": {"rows": 569, "columns": 31, "task_type": "classification"},
    }

    checks = []
    for case in cases:
        reference = expected[case["dataset"]]
        checks.extend(
            [
                case["rows"] == reference["rows"],
                case["columns"] == reference["columns"],
                case["task_type"] == reference["task_type"],
            ]
        )

    return {
        "reference_checks_passed": int(sum(checks)),
        "reference_checks_total": int(len(checks)),
        "statistical_correctness_rate": round(float(sum(checks) / len(checks)), 4),
        "reference_definition": "Dataset shape and task-type checks against scikit-learn reference metadata.",
    }


def main() -> None:
    cases = [
        _classification_case("iris", load_iris),
        _regression_case(),
        _classification_case("breast_cancer", load_breast_cancer),
    ]
    correctness = _statistical_correctness_checks(cases)

    classification_cases = [case for case in cases if case["task_type"] == "classification"]
    output = {
        "method": {
            "purpose": "Predictive benchmark and reference statistical correctness checks for the Data Discovery Agent study.",
            "note": "These metrics evaluate reference predictive models on the same benchmark datasets. They are not LLM training accuracy.",
            "random_state": RANDOM_STATE,
            "test_size": TEST_SIZE,
        },
        "cases": cases,
        "summary": {
            "classification_cases": len(classification_cases),
            "mean_accuracy": round(float(np.mean([case["accuracy"] for case in classification_cases])), 4),
            "mean_f1_macro": round(float(np.mean([case["f1_macro"] for case in classification_cases])), 4),
            "mean_error_rate": round(float(np.mean([case["error_rate"] for case in classification_cases])), 4),
            **correctness,
        },
    }

    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "predictive_results.json").write_text(json.dumps(output, indent=2), encoding="utf-8")

    lines = [
        "# Predictive and Statistical Correctness Evaluation",
        "",
        "This evaluation adds reference predictive metrics and statistical correctness checks for the three public scikit-learn benchmark datasets used in the pilot study. These results should be reported as benchmark/reference analysis results, not as LLM training accuracy.",
        "",
        "## Predictive Results",
        "",
        "| Dataset | Task | Model | Accuracy | F1 Macro | Error Rate | R2 | RMSE | MAE |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for case in cases:
        lines.append(
            "| {dataset} | {task_type} | {model} | {accuracy} | {f1_macro} | {error_rate} | {r2} | {rmse} | {mae} |".format(
                dataset=case["dataset"],
                task_type=case["task_type"],
                model=case["model"],
                accuracy=case.get("accuracy", "N/A"),
                f1_macro=case.get("f1_macro", "N/A"),
                error_rate=case.get("error_rate", "N/A"),
                r2=case.get("r2", "N/A"),
                rmse=case.get("rmse", "N/A"),
                mae=case.get("mae", "N/A"),
            )
        )

    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Mean classification accuracy: {output['summary']['mean_accuracy']}",
            f"- Mean classification F1 macro: {output['summary']['mean_f1_macro']}",
            f"- Mean classification error rate: {output['summary']['mean_error_rate']}",
            f"- Statistical correctness checks: {correctness['reference_checks_passed']}/{correctness['reference_checks_total']}",
            f"- Statistical correctness rate: {correctness['statistical_correctness_rate']}",
            "",
            "## Paper-Ready Wording",
            "",
            f"Using deterministic reference pipelines with an 80/20 train-test split, the classification benchmarks achieved a mean accuracy of {output['summary']['mean_accuracy']}, mean macro-F1 of {output['summary']['mean_f1_macro']}, and mean error rate of {output['summary']['mean_error_rate']} across Iris and Breast Cancer Wisconsin. On the Diabetes regression dataset, the reference pipeline achieved an R2 of {cases[1]['r2']}, RMSE of {cases[1]['rmse']}, and MAE of {cases[1]['mae']}. Dataset metadata checks against scikit-learn reference values passed {correctness['reference_checks_passed']}/{correctness['reference_checks_total']} checks, giving a statistical correctness rate of {correctness['statistical_correctness_rate']}.",
        ]
    )
    (OUT_DIR / "PREDICTIVE_EVALUATION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(output["summary"], indent=2))


if __name__ == "__main__":
    main()

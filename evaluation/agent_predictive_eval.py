from __future__ import annotations

import json
import os
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.datasets import load_breast_cancer, load_diabetes, load_iris


ROOT = Path(__file__).resolve().parents[1]
CHAT_V2 = ROOT / "demo" / "chat_v2"
PARENT_ENV = ROOT.parent / ".env"
TOLERANCE = 0.001


def _load_parent_env() -> None:
    if not PARENT_ENV.exists():
        return
    for raw_line in PARENT_ENV.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_parent_env()
sys.path.insert(0, str(CHAT_V2))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from backend_app.services.chat import ChatRuntimeConfig, bot_stream  # noqa: E402
from backend_app.services.workspace import get_session_workspace  # noqa: E402
from predictive_eval import _classification_case, _regression_case  # noqa: E402


def _write_dataset(name: str, loader, target_name: str) -> Path:
    session_id = f"agent_predictive_{name}"
    workspace = Path(get_session_workspace(session_id)).resolve()
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True, exist_ok=True)

    data = loader()
    frame = pd.DataFrame(data.data, columns=data.feature_names)
    frame[target_name] = data.target
    dataset_path = workspace / f"{name}.csv"
    frame.to_csv(dataset_path, index=False)
    return dataset_path


def _extract_json_objects(text: str) -> list[dict[str, Any]]:
    decoder = json.JSONDecoder()
    objects: list[dict[str, Any]] = []
    for match in re.finditer(r"\{", text):
        try:
            value, _ = decoder.raw_decode(text[match.start() :])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            objects.append(value)
    return objects


def _normalize_dataset_name(value: Any) -> str:
    return str(value or "").strip().lower().removesuffix(".csv")


def _run_agent_case(name: str, dataset_path: Path, prompt: str) -> dict[str, Any]:
    started = time.perf_counter()
    chunks: list[str] = []
    error = ""
    try:
        for chunk in bot_stream(
            messages=[{"role": "user", "content": prompt}],
            workspace=[str(dataset_path)],
            session_id=f"agent_predictive_{name}",
            runtime_config=ChatRuntimeConfig(temperature=0.0),
        ):
            chunks.append(str(chunk or ""))
    except Exception as exc:
        error = repr(exc)

    content = "".join(chunks)
    candidates = _extract_json_objects(content)
    reported = {}
    for candidate in reversed(candidates):
        if _normalize_dataset_name(candidate.get("dataset")) == name:
            reported = candidate
            break

    return {
        "dataset": name,
        "duration_sec": round(time.perf_counter() - started, 2),
        "error": error,
        "reported_metrics": reported,
        "json_found": bool(reported),
        "generated_code": "<Code>" in content,
        "executed_code": "<Execute>" in content,
        "completed_answer": "<Answer>" in content or "</Answer>" in content,
        "output_chars": len(content),
    }


def _compare_metric(reported: dict[str, Any], reference: dict[str, Any], key: str) -> dict[str, Any]:
    try:
        reported_value = float(reported[key])
        reference_value = float(reference[key])
    except (KeyError, TypeError, ValueError):
        return {"metric": key, "passed": False, "reported": reported.get(key), "reference": reference.get(key)}

    diff = abs(reported_value - reference_value)
    return {
        "metric": key,
        "passed": diff <= TOLERANCE,
        "reported": round(reported_value, 4),
        "reference": round(reference_value, 4),
        "absolute_difference": round(diff, 6),
    }


def _compare_case(agent_case: dict[str, Any], reference: dict[str, Any]) -> dict[str, Any]:
    reported = agent_case["reported_metrics"]
    if reference["task_type"] == "classification":
        metric_keys = ["accuracy", "f1_macro", "error_rate"]
    else:
        metric_keys = ["r2", "rmse", "mae"]

    checks = [_compare_metric(reported, reference, key) for key in metric_keys]
    return {
        **agent_case,
        "reference_metrics": reference,
        "metric_checks": checks,
        "metrics_passed": sum(1 for check in checks if check["passed"]),
        "metrics_total": len(checks),
        "all_metrics_matched": all(check["passed"] for check in checks),
    }


def main() -> None:
    references = {
        "iris": _classification_case("iris", load_iris),
        "diabetes": _regression_case(),
        "breast_cancer": _classification_case("breast_cancer", load_breast_cancer),
    }

    cases = [
        (
            "iris",
            _write_dataset("iris", load_iris, "species_target"),
            """Use the uploaded iris.csv dataset. Generate and execute Python code to train a deterministic reference classifier with this exact method: train_test_split(test_size=0.2, random_state=42, stratify=y), StandardScaler, LogisticRegression(max_iter=1000, random_state=42). Use all feature columns and species_target as the target. Report accuracy, macro F1, weighted F1, and error_rate. In the final <Answer>, output only one compact JSON object with keys: dataset, task_type, model, accuracy, f1_macro, f1_weighted, error_rate.""",
        ),
        (
            "diabetes",
            _write_dataset("diabetes", load_diabetes, "disease_progression_target"),
            """Use the uploaded diabetes.csv dataset. Generate and execute Python code to train a deterministic reference regression model with this exact method: train_test_split(test_size=0.2, random_state=42), StandardScaler, LinearRegression. Use all feature columns and disease_progression_target as the target. Report R2, RMSE, MAE, and normalized_rmse where normalized_rmse = RMSE / mean(y_test). In the final <Answer>, output only one compact JSON object with keys: dataset, task_type, model, r2, rmse, mae, normalized_rmse.""",
        ),
        (
            "breast_cancer",
            _write_dataset("breast_cancer", load_breast_cancer, "diagnosis_target"),
            """Use the uploaded breast_cancer.csv dataset. Generate and execute Python code to train a deterministic reference classifier with this exact method: train_test_split(test_size=0.2, random_state=42, stratify=y), StandardScaler, LogisticRegression(max_iter=1000, random_state=42). Use all feature columns and diagnosis_target as the target. Report accuracy, macro F1, weighted F1, and error_rate. In the final <Answer>, output only one compact JSON object with keys: dataset, task_type, model, accuracy, f1_macro, f1_weighted, error_rate.""",
        ),
    ]

    compared_cases = []
    for name, dataset_path, prompt in cases:
        agent_case = _run_agent_case(name, dataset_path, prompt)
        compared_cases.append(_compare_case(agent_case, references[name]))

    total_checks = sum(case["metrics_total"] for case in compared_cases)
    passed_checks = sum(case["metrics_passed"] for case in compared_cases)
    completed = [
        case
        for case in compared_cases
        if case["generated_code"] and case["executed_code"] and case["completed_answer"] and not case["error"]
    ]

    output = {
        "method": {
            "purpose": "Test whether the real agent loop can generate predictive evaluation code and report metrics matching deterministic reference outputs.",
            "llm_role": "The LLM generates the Python evaluation code and final metric report; the backend executes the generated code.",
            "tolerance": TOLERANCE,
        },
        "cases": compared_cases,
        "summary": {
            "total_cases": len(compared_cases),
            "completed_agent_workflows": len(completed),
            "json_metric_reports_found": sum(1 for case in compared_cases if case["json_found"]),
            "metric_checks_passed": passed_checks,
            "metric_checks_total": total_checks,
            "metric_correctness_rate": round(passed_checks / total_checks, 4) if total_checks else 0,
            "all_case_metrics_matched": sum(1 for case in compared_cases if case["all_metrics_matched"]),
        },
    }

    out_dir = ROOT / "evaluation"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "agent_predictive_results.json").write_text(json.dumps(output, indent=2), encoding="utf-8")

    lines = [
        "# Agent-Generated Predictive Evaluation",
        "",
        "This evaluation runs the real Data Discovery Agent loop. The LLM is prompted to generate and execute predictive evaluation code, then report metrics. Reported metrics are compared with deterministic reference outputs.",
        "",
        "## Summary",
        "",
        f"- Agent workflows completed: {output['summary']['completed_agent_workflows']}/{output['summary']['total_cases']}",
        f"- JSON metric reports found: {output['summary']['json_metric_reports_found']}/{output['summary']['total_cases']}",
        f"- Metric checks passed: {output['summary']['metric_checks_passed']}/{output['summary']['metric_checks_total']}",
        f"- Metric correctness rate: {output['summary']['metric_correctness_rate']}",
        f"- Cases with all metrics matched: {output['summary']['all_case_metrics_matched']}/{output['summary']['total_cases']}",
        "",
        "## Case Results",
        "",
        "| Dataset | Workflow | JSON | Metrics Passed | Runtime (s) |",
        "|---|---:|---:|---:|---:|",
    ]
    for case in compared_cases:
        workflow = case["generated_code"] and case["executed_code"] and case["completed_answer"] and not case["error"]
        lines.append(
            f"| {case['dataset']} | {workflow} | {case['json_found']} | {case['metrics_passed']}/{case['metrics_total']} | {case['duration_sec']} |"
        )
    lines.extend(["", "## Metric Comparisons", ""])
    for case in compared_cases:
        lines.append(f"### {case['dataset']}")
        lines.append("")
        lines.append("| Metric | Agent | Reference | Difference | Passed |")
        lines.append("|---|---:|---:|---:|---:|")
        for check in case["metric_checks"]:
            lines.append(
                f"| {check['metric']} | {check.get('reported')} | {check.get('reference')} | {check.get('absolute_difference', 'N/A')} | {check['passed']} |"
            )
        lines.append("")
    lines.extend(
        [
            "## Paper-Ready Wording",
            "",
            f"In an agent-generated predictive evaluation, the real Data Discovery Agent workflow completed {output['summary']['completed_agent_workflows']}/{output['summary']['total_cases']} benchmark workflows and produced machine-readable metric reports in {output['summary']['json_metric_reports_found']}/{output['summary']['total_cases']} cases. Compared against deterministic reference pipelines, {output['summary']['metric_checks_passed']}/{output['summary']['metric_checks_total']} reported metrics matched within a tolerance of {TOLERANCE}, yielding a metric correctness rate of {output['summary']['metric_correctness_rate']}.",
        ]
    )
    (out_dir / "AGENT_PREDICTIVE_EVALUATION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(output["summary"], indent=2))


if __name__ == "__main__":
    main()

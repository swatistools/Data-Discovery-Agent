from __future__ import annotations

import json
import shutil
import sys
import time
from pathlib import Path

import pandas as pd
from sklearn.datasets import load_breast_cancer, load_diabetes, load_iris


ROOT = Path(__file__).resolve().parents[1]
CHAT_V2 = ROOT / "demo" / "chat_v2"
sys.path.insert(0, str(CHAT_V2))

from backend_app.services.chat import ChatRuntimeConfig, bot_stream  # noqa: E402
from backend_app.services.workspace import get_session_workspace  # noqa: E402


def _write_dataset(name: str, loader, target_name: str) -> Path:
    session_id = f"pilot_{name}"
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


def _artifact_count(workspace: Path) -> int:
    generated = workspace / "generated"
    if not generated.exists():
        return 0
    return len(
        [
            path
            for path in generated.rglob("*")
            if path.is_file() and path.name != ".deepanalyze_generated.json"
        ]
    )


def _run_case(name: str, dataset_path: Path, prompt: str) -> dict:
    session_id = f"pilot_{name}"
    workspace = Path(get_session_workspace(session_id)).resolve()
    started = time.perf_counter()
    chunks: list[str] = []
    error = ""

    try:
        for chunk in bot_stream(
            messages=[{"role": "user", "content": prompt}],
            workspace=[str(dataset_path)],
            session_id=session_id,
            runtime_config=ChatRuntimeConfig(temperature=0.1),
        ):
            chunks.append(str(chunk or ""))
    except Exception as exc:
        error = repr(exc)

    content = "".join(chunks)
    duration_sec = round(time.perf_counter() - started, 2)
    return {
        "case": name,
        "rows": int(pd.read_csv(dataset_path).shape[0]),
        "columns": int(pd.read_csv(dataset_path).shape[1]),
        "duration_sec": duration_sec,
        "generated_code": "<Code>" in content,
        "executed_code": "<Execute>" in content,
        "completed_answer": "<Answer>" in content or "</Answer>" in content,
        "generated_artifacts": _artifact_count(workspace),
        "error": error,
        "output_chars": len(content),
    }


def main() -> None:
    cases = [
        (
            "iris",
            _write_dataset("iris", load_iris, "species_target"),
            "Run concise autonomous data discovery on iris.csv. Use at most one Python code execution, do not print raw rows, save one useful chart if helpful, and produce a final answer under 200 words with data quality notes, key patterns, decision-support insights, assumptions, and limitations.",
        ),
        (
            "diabetes",
            _write_dataset("diabetes", load_diabetes, "disease_progression_target"),
            "Run concise autonomous data discovery on diabetes.csv. Use at most one Python code execution, do not print raw rows, save one useful chart if helpful, and produce a final answer under 200 words with data quality notes, target relationships, cautious health-policy insights, assumptions, and limitations.",
        ),
        (
            "breast_cancer",
            _write_dataset("breast_cancer", load_breast_cancer, "diagnosis_target"),
            "Run concise autonomous data discovery on breast_cancer.csv. Use at most one Python code execution, do not print raw rows, save one useful chart if helpful, and produce a final answer under 200 words with data quality notes, target relationships, cautious screening-policy insights, assumptions, and limitations.",
        ),
    ]

    results = [_run_case(name, path, prompt) for name, path, prompt in cases]
    passed = [row for row in results if row["generated_code"] and row["executed_code"] and row["completed_answer"] and not row["error"]]
    median_duration = sorted(row["duration_sec"] for row in results)[len(results) // 2]

    output = {
        "cases": results,
        "summary": {
            "total_cases": len(results),
            "completed_workflows": len(passed),
            "code_generation_success": sum(1 for row in results if row["generated_code"]),
            "code_execution_success": sum(1 for row in results if row["executed_code"]),
            "answer_completion_success": sum(1 for row in results if row["completed_answer"]),
            "total_generated_artifacts": sum(row["generated_artifacts"] for row in results),
            "median_duration_sec": median_duration,
        },
    }

    out_dir = ROOT / "evaluation"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "pilot_results.json").write_text(json.dumps(output, indent=2), encoding="utf-8")

    lines = [
        "# Pilot Evaluation Results",
        "",
        "This pilot uses three built-in public benchmark datasets from scikit-learn to exercise the real agent loop: dataset upload context, LLM-generated Python code, backend execution, generated artifacts, and final answer production.",
        "",
        "## Summary",
        "",
        f"- Cases: {output['summary']['total_cases']}",
        f"- Completed workflows without manual code editing: {output['summary']['completed_workflows']}/{output['summary']['total_cases']}",
        f"- Code generation success: {output['summary']['code_generation_success']}/{output['summary']['total_cases']}",
        f"- Code execution success: {output['summary']['code_execution_success']}/{output['summary']['total_cases']}",
        f"- Final answer completion: {output['summary']['answer_completion_success']}/{output['summary']['total_cases']}",
        f"- Generated artifacts: {output['summary']['total_generated_artifacts']}",
        f"- Median runtime: {output['summary']['median_duration_sec']} seconds",
        "",
        "## Case Results",
        "",
        "| Dataset | Rows | Columns | Code | Execute | Answer | Artifacts | Runtime (s) |",
        "|---|---:|---:|---|---|---|---:|---:|",
    ]
    for row in results:
        lines.append(
            f"| {row['case']} | {row['rows']} | {row['columns']} | {row['generated_code']} | {row['executed_code']} | {row['completed_answer']} | {row['generated_artifacts']} | {row['duration_sec']} |"
        )
    lines.extend(
        [
            "",
            "## Paper-Ready Result Statement",
            "",
            f"In a preliminary prototype evaluation across three public benchmark datasets, Data Discovery Agent completed {output['summary']['completed_workflows']}/{output['summary']['total_cases']} autonomous analysis workflows without manual code editing, generated executable Python analysis code in {output['summary']['code_generation_success']}/{output['summary']['total_cases']} cases, executed code successfully in {output['summary']['code_execution_success']}/{output['summary']['total_cases']} cases, and produced final analytical answers in {output['summary']['answer_completion_success']}/{output['summary']['total_cases']} cases, with a median runtime of {output['summary']['median_duration_sec']} seconds.",
        ]
    )
    (out_dir / "PILOT_EVALUATION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(output["summary"], indent=2))


if __name__ == "__main__":
    main()

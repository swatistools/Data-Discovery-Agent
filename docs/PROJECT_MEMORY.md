# Data Discovery Agent Project Memory

Last updated: 2026-07-01

This file is a compact handoff note for continuing the project without rereading the whole codebase.

## Project Identity

- Product name: Data Discovery Agent
- Purpose: autonomous data discovery, exploratory analysis, executable Python-based analytics, visualization generation, and policy-oriented insight generation.
- Scope: not GIS-focused. The project is for general data discovery, analysis, and policy insight.
- Current positioning: an LLM-driven autonomous data analysis and decision-support framework.
- Public repo target: `https://github.com/swatistools/Data-Discovery-Agent.git`
- Attribution policy: do not describe the repo as cloned in product docs. Keep license attribution only: "Includes MIT-licensed components from DeepAnalyze. See LICENSE."

## Current Tech Stack

- Backend: Python FastAPI-style backend in `demo/chat_v2/backend_app`
- Frontend: Next.js app in `demo/chat_v2/frontend`
- Agent runtime: backend chat loop in `backend_app/services/chat.py`
- LLM provider: OpenAI-compatible client, configured for Groq by default
- Data analysis execution: Python code generation and execution flow inherited from the original app
- Package managers:
  - Python dependencies from root `requirements.txt`
  - Frontend dependencies from `demo/chat_v2/frontend/package.json`

## Important Files

- Main docs: `README.md`
- Setup guide: `docs/SETUP.md`
- This memory file: `docs/PROJECT_MEMORY.md`
- Backend settings: `demo/chat_v2/backend_app/settings.py`
- Backend chat service: `demo/chat_v2/backend_app/services/chat.py`
- Frontend main interface: `demo/chat_v2/frontend/components/three-panel-interface.tsx`
- Frontend app metadata/layout: `demo/chat_v2/frontend/app/layout.tsx`
- Environment example: `.env.example`
- Evaluation script: `evaluation/pilot_eval.py`
- Evaluation report: `evaluation/PILOT_EVALUATION.md`
- Evaluation raw output: `evaluation/pilot_results.json`

## Environment

Local secrets are stored outside the repo in:

```text
D:\gis autonomous\.env
```

Expected keys:

```text
GROQ_API_KEY=
GROQ_MODEL=llama-3.3-70b-versatile
LLM_BASE_URL=https://api.groq.com/openai/v1
GITHUB_TOKEN=
GITHUB_REPO=https://github.com/swatistools/Data-Discovery-Agent.git
```

Do not commit real token values or print them in chat/output.

## Repository State

- Working repo path: `D:\gis autonomous\DeepAnalyze`
- Target remote: `target`
- Target branch: `main`
- Current local branch name may still be `policy-insight-groq`, tracking `target/main`.
- Remote details:
  - `origin`: `https://github.com/ruc-datalab/DeepAnalyze.git`
  - `target`: `https://github.com/swatistools/Data-Discovery-Agent.git`

Use `target` for pushes. Do not store the GitHub token in the remote URL.

Safe push command pattern from PowerShell:

```powershell
$lines=Get-Content 'D:\gis autonomous\.env'
$token=($lines | Where-Object { $_ -match '^GITHUB_TOKEN=' }) -replace '^GITHUB_TOKEN=',''
$basic=[Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("x-access-token:$token"))
git -c http.extraheader="AUTHORIZATION: basic $basic" push target HEAD:main
```

## Major Changes Already Completed

1. Configured the app for Groq/OpenAI-compatible LLM use.
2. Rebranded visible product copy to Data Discovery Agent.
3. Rewrote README and setup docs as standalone project documentation.
4. Removed heavy unrelated research/training/demo files to make the repo smaller and cleaner.
5. Added future upgrade roadmap.
6. Added pilot evaluation script and results.
7. Pushed the cleaned and branded repo to `swatistools/Data-Discovery-Agent`.

## Current Evaluation Result

Pilot evaluation used three public scikit-learn datasets: iris, diabetes, and breast cancer.

Results:

- Cases tested: 3
- Completed autonomous workflows without manual code editing: 3/3
- Python code generation success: 3/3
- Python code execution success: 3/3
- Final analytical answer completion: 3/3
- Generated artifacts: 5
- Median runtime: 33.53 seconds

Safe paper wording:

> A preliminary prototype evaluation across three public benchmark datasets showed that the framework completed all tested autonomous workflows without manual code editing, generated and executed Python analysis code in each case, produced final analytical answers in all cases, generated five analytical artifacts, and achieved a median runtime of 33.53 seconds.

Do not claim a percentage faster than humans unless a manual baseline study is run.

## Current Abstract Direction

The current paper topic is:

```text
Data Discovery Agent: An LLM-Driven Autonomous Framework for Data Discovery, Analytical Reasoning, and Policy Insight Generation
```

The abstract should frame the work as a novel framework/prototype, not a review paper. It can include the pilot results above, but should not fabricate user studies, large benchmark results, or policy deployment outcomes.

## App Flow

High-level flow:

1. User uploads a dataset or asks a natural-language analysis question.
2. The backend interprets the request and dataset context.
3. The LLM plans the analysis.
4. The LLM generates Python code.
5. The backend executes the code and captures outputs/artifacts.
6. The LLM interprets outputs and produces a human-readable answer.
7. The answer can include analysis findings, chart/table references, policy implications, assumptions, and limitations.

## Future Upgrade Roadmap

Practical next upgrades:

- Add RAG for policy documents, reports, laws, and institutional evidence.
- Add citations and source-grounded policy recommendations.
- Add saved projects and analysis history.
- Add user authentication and private storage.
- Add richer report templates for conference/demo outputs.
- Add scheduled recurring analysis jobs.
- Add database, CSV, Excel, API, and cloud storage connectors.
- Add local/self-hosted LLM profiles for Ollama, LM Studio, or vLLM.
- Add stronger sandboxing for executed Python code, preferably Docker-based.
- Expand evaluation to more datasets and add a manual baseline comparison.

## Verification Commands

Frontend build:

```powershell
cd "D:\gis autonomous\DeepAnalyze\demo\chat_v2\frontend"
npm run build
```

Backend compile check:

```powershell
cd "D:\gis autonomous\DeepAnalyze\demo\chat_v2"
python -m compileall backend_app -q
```

Pilot evaluation:

```powershell
cd "D:\gis autonomous\DeepAnalyze"
python evaluation/pilot_eval.py
```

## Known Caution

Running `next build` may modify `demo/chat_v2/frontend/next-env.d.ts`. If that file becomes dirty only because `.next` route type paths changed, inspect it before committing and avoid committing accidental build-environment churn unless needed.

## Next Best Steps

1. Keep README and paper claims aligned with the actual pilot evaluation.
2. Add a stronger evaluation section if submitting to a conference.
3. Run a manual baseline study if claiming faster-than-manual analysis.
4. Add RAG only after the current Groq-based workflow is stable.
5. Keep future changes small and focused; avoid rebuilding the whole architecture unless necessary.

# Data Discovery Agent

Data Discovery Agent is an autonomous data discovery, analysis, and policy insight app. Upload a dataset, ask a question, and the agent profiles the data, writes Python analysis code, executes it, and returns findings, charts, generated files, and a report-style answer.

The default setup uses Groq through an OpenAI-compatible API, so a local GPU, local LLM server, or vLLM setup is not required.

## What It Does

- Upload CSV, Excel, JSON, text, Markdown, SQLite/database files, PDFs, images, and zip files.
- Inspect schema, columns, missing values, anomalies, trends, and group differences.
- Generate Python analysis code and execute it in the workspace.
- Produce charts, tables, generated files, Markdown reports, and optional PDF exports.
- Continue analysis through chat with the same workspace context.
- Support local or Docker-based Python execution.
- Support Groq by default, with optional local/self-hosted OpenAI-compatible LLMs.

## App Flow

```text
Upload data
  -> agent inspects available files
  -> Groq generates analysis/code
  -> backend executes Python
  -> execution result returns to the agent
  -> final answer, charts, files, and report are shown in the UI
```

## Requirements

- Python 3.11 or newer recommended
- Node.js 20 or newer recommended
- Groq API key
- Docker optional, recommended for isolated code execution

## Environment

Create `demo/chat_v2/.env` from `demo/chat_v2/.env.example` and set:

```env
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
LLM_BASE_URL=https://api.groq.com/openai/v1
DEEPANALYZE_EXECUTION_MODE=local
```

For Docker execution:

```env
DEEPANALYZE_EXECUTION_MODE=docker
DEEPANALYZE_DOCKER_IMAGE=deepanalyze-chat-exec:latest
```

Build the execution image once:

```bash
cd demo/chat_v2
docker build -t deepanalyze-chat-exec:latest -f Dockerfile.exec .
```

## Install

Install Python dependencies from the repository root:

```bash
pip install -r requirements.txt
```

Install frontend dependencies:

```bash
cd demo/chat_v2/frontend
npm install
```

## Run

Windows:

```bat
cd demo\chat_v2
start.bat
```

Linux/macOS:

```bash
cd demo/chat_v2
bash start.sh
```

Default local addresses:

- Frontend: `http://localhost:4000`
- Backend API: `http://localhost:8200`
- File server: `http://localhost:8100`

## Using A Local LLM Later

Groq is the default, but the app can use any OpenAI-compatible model endpoint. Point the model base URL at Ollama, vLLM, LM Studio, or another compatible server:

```env
LLM_BASE_URL=http://localhost:8000/v1
DEEPANALYZE_MODEL_PATH=your-local-model-name
```

For local models, use the UI's custom model option if you want to enter model name, base URL, and API key from the browser.

## Future Upgrades

These are planned extension areas, not required for the current app flow:

- RAG over policy documents, reports, PDFs, and internal knowledge bases.
- Citations and evidence tracking for generated findings and recommendations.
- Saved projects, analysis history, and reusable workspaces.
- User authentication, roles, and private file storage.
- Report templates for policy briefs, executive summaries, and data quality audits.
- Scheduled analysis jobs for recurring datasets.
- Database connectors for Postgres, MySQL, BigQuery, Snowflake, and APIs.
- Optional local/self-hosted LLM deployment for offline or private environments.
- Stronger Docker sandboxing and resource limits for generated Python code.
- Evaluation datasets to test answer quality, code execution reliability, and policy insight usefulness.

## Repository Layout

```text
demo/chat_v2/
  backend_app/      FastAPI backend, chat loop, workspace, execution, export
  frontend/         Next.js UI
  Dockerfile.exec   Optional Python execution sandbox image
  .env.example      Runtime configuration template
docs/SETUP.md       Setup and deployment notes
requirements.txt    Python dependencies
```

## Safety Note

The agent executes generated Python code. Use Docker execution for untrusted files or shared deployments.

## Attribution

Includes MIT-licensed components from DeepAnalyze. See `LICENSE`.

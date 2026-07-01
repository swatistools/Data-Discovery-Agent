# Data Discovery Agent Web App

This folder contains the browser app: FastAPI backend, workspace/file services, Python execution, export endpoints, and Next.js frontend.

## Features

- Upload and manage data files in a per-session workspace.
- Preview common files directly in the UI.
- Stream structured `<Analyze>`, `<Code>`, `<Execute>`, `<File>`, and `<Answer>` blocks.
- Execute Python analysis code locally or inside Docker.
- Generate charts, tables, files, Markdown reports, and optional PDF reports.
- Use Groq by default without a local GPU.
- Use custom OpenAI-compatible endpoints for local/self-hosted models.

## Environment

Copy the example file:

```bash
cp .env.example .env
```

Windows:

```powershell
Copy-Item .env.example .env
```

Set the required Groq values:

```env
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
LLM_BASE_URL=https://api.groq.com/openai/v1
```

## Execution Mode

Local execution:

```env
DEEPANALYZE_EXECUTION_MODE=local
```

Docker execution:

```env
DEEPANALYZE_EXECUTION_MODE=docker
```

Build the Docker execution image once:

```bash
docker build -t deepanalyze-chat-exec:latest -f Dockerfile.exec .
```

## Install

From the repository root:

```bash
pip install -r requirements.txt
```

Frontend:

```bash
cd demo/chat_v2/frontend
npm install
```

## Run

Windows:

```bat
start.bat
```

Linux/macOS:

```bash
bash start.sh
```

Default addresses:

- Frontend: `http://localhost:4000`
- Backend API: `http://localhost:8200`
- File server: `http://localhost:8100`

## Local LLM Option

To use a local or self-hosted model, provide an OpenAI-compatible `/v1` endpoint:

```env
LLM_BASE_URL=http://localhost:8000/v1
DEEPANALYZE_MODEL_PATH=your-local-model-name
```

You can also select the custom model provider in the UI and enter the model name, API base, and optional API key there.

# Data Discovery Agent Setup

## Default Model Provider

Data Discovery Agent uses Groq by default:

```env
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
LLM_BASE_URL=https://api.groq.com/openai/v1
```

This avoids local GPU and local LLM setup for the standard deployment.

## Local Or Self-Hosted LLM

Any OpenAI-compatible endpoint can be used later:

```env
LLM_BASE_URL=http://localhost:8000/v1
DEEPANALYZE_MODEL_PATH=your-local-model-name
```

Examples include Ollama, vLLM, LM Studio, or another hosted compatible API.

## Code Execution

Local execution is easiest for development:

```env
DEEPANALYZE_EXECUTION_MODE=local
```

Docker execution is recommended for safer handling of generated Python code:

```env
DEEPANALYZE_EXECUTION_MODE=docker
DEEPANALYZE_DOCKER_IMAGE=deepanalyze-chat-exec:latest
```

Build the image:

```bash
cd demo/chat_v2
docker build -t deepanalyze-chat-exec:latest -f Dockerfile.exec .
```

## What Was Kept

- Web app in `demo/chat_v2`
- Groq/OpenAI-compatible model path
- Python execution loop
- Workspace/file handling
- Chart/report/export flow
- Optional Docker execution

## What Was Removed

- training and research code
- benchmark/playground datasets
- old demo surfaces
- unused frontend UI components
- duplicate frontend lockfile

The app flow remains: upload data, generate analysis code, execute Python, return results, and continue through chat.

## Future Upgrade Paths

- Add RAG for policy documents, PDFs, reports, and internal knowledge bases.
- Add citations so reports show which uploaded files or document passages support each insight.
- Add saved projects and analysis history.
- Add authentication and private file storage.
- Add report templates for policy briefs, executive summaries, and data quality audits.
- Add scheduled analysis jobs for recurring datasets.
- Add database/API connectors.
- Add local/self-hosted LLM deployment profiles.
- Harden Docker execution with stricter CPU, memory, timeout, and filesystem limits.

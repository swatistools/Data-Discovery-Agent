# Our DeepAnalyze Modifications

This fork uses DeepAnalyze WebUI v2 as the base for an autonomous data discovery, analysis, and policy insight product.

## What Changed

- Groq is the default LLM provider through the OpenAI-compatible API.
- Local GPU/vLLM is not required for the default setup.
- The default analyst behavior is policy insight oriented.
- The frontend copy is rebranded for policy/data analysis.

## Required Environment

```env
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
LLM_BASE_URL=https://api.groq.com/openai/v1
```

## Optional Local LLM

You can still use a local or self-hosted LLM if it exposes an OpenAI-compatible API. Point the app at Ollama, vLLM, LM Studio, or another compatible server:

```env
LLM_BASE_URL=http://localhost:8000/v1
DEEPANALYZE_MODEL_PATH=DeepAnalyze-8B
```

For Ollama's OpenAI-compatible endpoint, use its `/v1` base URL and set `DEEPANALYZE_MODEL_PATH` to the local model name.

## Scope

This version is not GIS-focused and does not include accounts, billing, or custom model training.

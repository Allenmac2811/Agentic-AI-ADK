# Agentic-AI-ADK

This repo contains agents creation using Google's Agent Development Kit(ADK)

# Basic Agent - Google ADK (Agent Development Kit)

This project implements a smart assistant agent using [Google's Agent Development Kit (ADK)](https://github.com/google/agent-development-kit) and Vertex AI. The agent can perform smart topic lookups using Wikipedia, web search, and more. It's designed for fast prototyping and deployment of LLM-based tools.

---

## Project Structure

```
basic_agent/
├── agent.py                 # Core logic and tool functions
├── __init__.py              # Module init
├── .env                     # Environment config (Vertex AI, GCP project)
├── agent.cpython-*.pyc      # Compiled bytecode (ignore)
└── __init__.cpython-*.pyc   # Compiled bytecode (ignore)
```

---

## Features

- LLM agent using `gemini-2.0-flash-lite`
- Smart topic lookup with:
- DuckDuckGo API
- Wikipedia summary + disambiguation handling
- Weather mock tool
- Time lookup for New York
- Wikipedia search and summary
- LinkedIn profile mock search
- Google-like web search simulation

All tools are pre-built and easily pluggable into the agent.

---

## Getting Started

### 1. Clone this Repo

```bash
git clone https://github.com/YOUR_USERNAME/basic_agent.git
cd basic_agent
```

### 2. Setup Python Environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # You need to create this
```

### 3. Configure Environment

Create a `.env` file (already included):

```env
GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
GOOGLE_CLOUD_LOCATION="us-central1"
GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

### 4. Run the Agent (Locally)

```bash
adk web
# OR
adk run
```

---

## 🔧 Tool Activation

In `agent.py`, additional tools are defined and can be added to the `LlmAgent`:

```python
tools=[
    get_weather,
    get_current_time,
    get_wiki_summary,
    search_wikipedia,
    search_google_like,
    smart_topic_lookup,
    google_search  # default built-in tool
]
```

Uncomment the tools you want to activate.

---

## Deployment (Optional)

To deploy as a Cloud Function or Cloud Run service:

- Package with dependencies (`requirements.txt`)
- Use `adk deploy` (Cloud Functions) or `gcloud run deploy` (Cloud Run)

Contact your GCP admin to ensure Vertex AI access.

---

## Powered By

- [Google Agent Development Kit (ADK)](https://github.com/google/agent-development-kit)
- [Vertex AI + Gemini Models](https://cloud.google.com/vertex-ai/docs/generative-ai/overview)
- [Wikipedia REST API](https://en.wikipedia.org/api/rest_v1/)
- [DuckDuckGo Instant Answer API](https://duckduckgo.com/api)

---

## Author

**Allen Mac**  
Feel free to reach out for collaboration or questions.

---

## License

MIT License (or replace based on your preference)

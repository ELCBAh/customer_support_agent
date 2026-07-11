# AI Customer Support Agent API (Triage)

This API uses AI agents to classify incoming customer support tickets and routes them to the correct department by using a 'Triage' method which means it prioritises and categorizes tickets to ensure efficient handling.

## Features

- Urgency classification
- Sentiment detection
- Ticket creation
- Problem summarization
- Suggested support relply
- Human escalation rules
- Multi-model-ready architecture (scalable)

## Dependencies

- `FastAPI`
- `Pydantic`
- `python-dotenv`
- `uvicorn`

## Quick Start

0. Make sure you have a venv for the project

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. Set environment variables: (Not implemented yet, skip this step)

```bash
export AI_API_KEY=your_AI_api_key
```

3. Run the server:

```bash
uvicorn app.main:app --reload
```

4. Test the API:

```bash
curl http://localhost:8000/docs
```

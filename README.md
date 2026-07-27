# Workflow Replay API

A Python FastAPI backend for storing, analyzing, and comparing event-driven workflow runs.

## Features

- Create and retrieve workflow runs
- Validate workflow event payloads with Pydantic
- Calculate duration, success rate, failures, and longest event gap
- Compare two workflow runs
- SQLite persistence with SQLAlchemy
- Interactive Swagger documentation
- Pytest coverage
- Docker support

## Tech stack

Python 3.12, FastAPI, SQLAlchemy, Pydantic, SQLite, Pytest, Docker.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Windows activation:

```powershell
.venv\Scripts\activate
```

Swagger UI: `http://localhost:8000/docs`

## Test

```bash
pytest
```

## Endpoints

```text
GET    /health
POST   /api/workflows
GET    /api/workflows
GET    /api/workflows/{workflow_id}
DELETE /api/workflows/{workflow_id}
GET    /api/workflows/{workflow_id}/analytics
POST   /api/workflows/compare
```

## GitHub description

FastAPI backend for storing, analyzing, and comparing event-driven workflow executions.

## License

MIT

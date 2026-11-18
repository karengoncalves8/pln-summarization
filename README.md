# PLN Summarization API

FastAPI project managed with [uv](https://docs.astral.sh/uv/).

## Setup

```bash
uv sync
cp .env.example .env   # optional
```

## Run

```bash
uv run fastapi dev app/main.py      # dev server with reload
uv run fastapi run app/main.py      # production mode
```

Web UI: http://127.0.0.1:8000/
API docs: http://127.0.0.1:8000/docs

## Test & lint

```bash
uv run pytest
uv run pylint app tests
uv run isort .
uv run black .
```

## Structure

```
app/
├── main.py            # FastAPI app entrypoint
├── config.py          # Settings (env vars / .env)
├── logger.py          # Logging
├── models/            # Data models
├── pipeline/          # Summarization flow
├── services/          # Text processing and similarity
├── templates/         # Jinja page
└── static/            # CSS and JavaScript
tests/
└── test_api.py
```

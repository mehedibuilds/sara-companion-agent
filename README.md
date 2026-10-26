# SARA

SARA is a stateful Telegram companion built as an explicit orchestration graph. It accepts text and voice, enriches requests with durable context, delegates specialised work, and returns a conversational response in the appropriate modality.

## Design

```text
Telegram -> ingestion -> perception -> companion -> synthesis -> Telegram
                              |             |
                        SQLite + FTS5   specialist registry
```

- **Graph orchestration** keeps routing, persistence, and response synthesis inspectable.
- **Memory** stores auditable facts and searchable conversation excerpts in SQLite/FTS5.
- **Specialists** are capability adapters, not prompt fragments embedded in routing code.
- **Transcription and speech** are ports; providers can be replaced without changing the graph.

## Run locally

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env
sara
```

Set `SARA_TELEGRAM_TOKEN` before running.

## Quality checks

```powershell
ruff check .
pytest
```

## Repository conventions

- No credentials, database files, or raw user media are committed.
- Domain logic lives in `src/sara`; transport code stays under `transport/`.
- New external services implement a narrow protocol before they enter graph nodes.
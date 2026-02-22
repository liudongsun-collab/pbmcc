# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
FastAPI web application with async PostgreSQL database.
GitHub: https://github.com/liudongsun-collab/pbmcc (private)

---

## Commands

```bash
pip install -r requirements.txt   # install dependencies
uvicorn main:app --reload          # run dev server

pytest                             # run all tests
pytest -v                          # verbose
pytest -k "users"                  # run tests matching name
```

API docs (server must be running): http://localhost:8000/docs

---

## Architecture

```
pbmcc/
├── main.py         # FastAPI app, route handlers, startup event
├── database.py     # Async SQLAlchemy engine, session factory, Base, get_db
├── models.py       # SQLAlchemy ORM models (User)
├── requirements.txt
├── pytest.ini      # asyncio_mode = auto
└── tests/
    ├── conftest.py # Overrides get_db with in-memory SQLite; provides `client` fixture
    └── test_main.py
```

### Key decisions
- **Async throughout**: all DB operations use `async/await` via `asyncpg`
- **Dependency injection**: DB session injected via `Depends(get_db)` in `database.py` — never import the session directly
- **Test DB**: tests use SQLite in-memory (`aiosqlite`) via `app.dependency_overrides[get_db]` — keep tests self-contained and never require a live Postgres instance
- **Table creation**: `main.py` creates all tables on startup via `Base.metadata.create_all` inside the `lifespan` context manager

---

## Code Conventions

- Python 3.12, async-first — all route handlers touching the DB must be `async def`
- SQLAlchemy models in `models.py`, inherit from `Base`, use `Mapped` + `mapped_column` (SQLAlchemy 2.0 style)
- New routes go in `main.py` (until the project warrants APIRouter)
- No raw SQL in application code — use SQLAlchemy ORM or `select()` expressions
- Raw SQL via `text()` is acceptable in test fixtures for seeding data (see `test_main.py`)

---

## Environment Setup

Copy `.env.example` to `.env` and fill in:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/pbmcc
```

### Network proxy (Windows)
```bash
export HTTPS_PROXY=http://127.0.0.1:7078
export HTTP_PROXY=http://127.0.0.1:7078
```
Already set in `~/.bashrc` — no action needed per session.

---

## Git Workflow

- Default branch: `master`
- Branch naming: `feature/`, `fix/`, `chore/`
- PRs merge into `master` via `gh pr merge --merge --delete-branch`
- Run `pytest` before every commit; never push directly to `master`

---

## Known Issues / TODOs

- No authentication — all endpoints are public
- No pagination on `GET /users`

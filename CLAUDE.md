# pbmcc — Claude Code Instructions

## Project Overview
FastAPI web application with async PostgreSQL database.
GitHub: https://github.com/liudongsun-collab/pbmcc (private)

---

## Commands

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run development server
```bash
uvicorn main:app --reload
```

### Run tests
```bash
pytest
pytest -v          # verbose
pytest -k "users"  # run specific test
```

### API docs (when server is running)
- Swagger UI: http://localhost:8000/docs
- ReDoc:       http://localhost:8000/redoc

---

## Architecture

```
pbmcc/
├── main.py         # FastAPI app, route handlers
├── database.py     # Async SQLAlchemy engine, session, Base
├── models.py       # SQLAlchemy ORM models
├── requirements.txt
├── pytest.ini      # asyncio_mode = auto
└── tests/
    ├── conftest.py # Test client + in-memory SQLite override
    └── test_main.py
```

### Key decisions
- **Async throughout**: all DB operations use `async/await` via `asyncpg`
- **Dependency injection**: DB session injected via `Depends(get_db)` — do not import session directly
- **Test DB**: tests use SQLite in-memory (`aiosqlite`), not PostgreSQL — keep tests self-contained
- **`@app.on_event("startup")` is deprecated** — migrate new startup logic to `lifespan` context manager

---

## Code Conventions

- Python 3.12
- Async-first: all route handlers that touch the DB must be `async def`
- SQLAlchemy models go in `models.py`, inherit from `Base`
- New routes go in `main.py` (until the project grows enough to warrant routers)
- Use `Mapped` + `mapped_column` for model columns (SQLAlchemy 2.0 style)
- No raw SQL — use SQLAlchemy ORM or `select()` expressions
- Environment variables loaded from `.env` via `python-dotenv`

---

## Environment Setup

1. Copy `.env.example` to `.env` and fill in credentials:
   ```
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/pbmcc
   ```
2. Never commit `.env` — it is in `.gitignore`

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
- PRs merge into `master` via GitHub (`gh pr merge --merge --delete-branch`)
- Always run `pytest` before committing

---

## Non-Negotiable Rules

- **Never skip tests** — run `pytest` before every commit
- **Never commit `.env`** — secrets stay local
- **Never push directly to `master`** — always use a feature branch + PR
- **Never modify test fixtures in `conftest.py`** without updating all affected tests
- **Never use synchronous DB calls** — all DB access must be `async`

---

## Known Issues / TODOs

- `@app.on_event("startup")` is deprecated — migrate to `lifespan` handler
- No authentication yet — all endpoints are public
- No pagination on `GET /users` — add when user count grows
- No `POST /users` endpoint yet

# CSUS Event Hub

A small FastAPI + SQLite API for club events, members, and RSVPs.

## Requirements

- Python 3.11 or newer
- Git

## Setup

```bash
git clone https://github.com/perochoa/csus-event-hub.git
cd csus-event-hub
```

| Step                  | Mac or Linux                                  | Windows                                           |
| --------------------- | --------------------------------------------- | ------------------------------------------------- |
| Create venv           | `python3 -m venv .venv`                       | `python -m venv .venv`                            |
| Install               | `.venv/bin/python -m pip install -e ".[dev]"` | `.venv/Scripts/python -m pip install -e ".[dev]"` |
| Create local env file | `cp .env.example .env`                        | `Copy-Item .env.example .env`                     |
| Run tests             | `.venv/bin/python -m pytest`                  | `.venv/Scripts/python -m pytest`                  |

The venv is never activated: every command calls its Python by path.

## Commands

On Windows, use `.venv/Scripts/python` in place of `.venv/bin/python`.

| Task                      | Command                                                    |
| ------------------------- | ---------------------------------------------------------- |
| Run all tests             | `.venv/bin/python -m pytest`                               |
| Run one test file or test | `.venv/bin/python -m pytest tests/test_events.py -k delete` |
| Lint and auto-fix         | `.venv/bin/python -m ruff check --fix .`                   |
| Format                    | `.venv/bin/python -m ruff format .`                        |
| Load demo data            | `.venv/bin/python -m app.seed`                             |
| Run the API               | `.venv/bin/python -m uvicorn app.main:app --reload`        |

While the API is running, the interactive docs are at <http://localhost:8000/docs>.

## Configuration

Settings come from environment variables:

| Variable        | Default                    |
| --------------- | -------------------------- |
| `DATABASE_URL`  | `sqlite:///./event_hub.db` |
| `CLUB_TIMEZONE` | `America/Toronto`          |

## Layout

```text
app/
├── main.py              # FastAPI app + router wiring
├── config.py            # settings read from environment variables
├── db.py                # engine and session dependency
├── models.py            # SQLModel tables and schemas: Event, Member, RSVP
├── seed.py              # demo data
├── routes/
│   ├── events.py        # CRUD for events
│   ├── members.py       # members
│   ├── rsvps.py         # RSVPs and check-in
│   └── stats.py         # exec dashboard numbers
└── services/
    ├── events.py        # event business logic
    └── legacy_stats.py  # stats calculations
tests/
├── conftest.py          # test client + in-memory DB fixtures
└── test_events.py
```

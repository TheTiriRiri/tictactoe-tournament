# Tic-tac-toe Tournament

A Python Tic-tac-toe tournament app with a Tkinter GUI. Supports 2–5 rotating players, a configurable win target, and player login/registration backed by SQLite.

See [`PRD.md`](PRD.md) for the full product spec.

## Features

- 2–5 players rotating through matches (symbols: `X O △ ● ■`)
- Configurable win target per tournament
- Player login/registration with salted SHA-256 password hashes
- Winning-line highlight on the board
- Pure-logic core, separated from GUI for testability

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
```

No third-party dependencies — standard library only (`tkinter`, `sqlite3`, `unittest`).

## Running

```bash
# Launch the GUI
python -m src.tictactoe_gui
```

On first run, `tournament.db` is created in the project root.

## Testing

```bash
# All tests
python -m unittest discover tests

# Single suite
python -m unittest tests.test_tictactoe
python -m unittest tests.test_auth
```

## Project Layout

- `src/tictactoe_logic.py` — pure game logic: `Player`, `Tournament`, win detection, N-player rotation
- `src/tictactoe_gui.py` — Tkinter GUI: setup dialog, board rendering, highlights
- `src/auth.py` — `AuthManager` for registration/login against SQLite
- `tests/` — `unittest` suites for logic and auth
- `tournament.db` — local SQLite database (created on first run; not committed)

## Conventions

- Python with type hints on all function signatures
- Short docstring on every function
- Tests use `unittest` (not pytest)
- GUI code kept separate from pure logic

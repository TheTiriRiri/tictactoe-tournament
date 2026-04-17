# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python Tic-tac-toe tournament app with a Tkinter GUI. Supports 2–5 rotating players, a configurable win target, and player login/registration backed by SQLite. Originally started as a subagent-learning demo.

See `PRD.md` for the full product spec.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
# No third-party dependencies — standard library only (tkinter, sqlite3, unittest).
```

## Commands

```bash
# Run the GUI app
python -m src.tictactoe_gui

# Run all tests
python -m unittest discover tests

# Run a single test file
python -m unittest tests.test_tictactoe
python -m unittest tests.test_auth
```

## Architecture

- `src/tictactoe_logic.py` — pure game logic: `Player`, `Tournament`, win detection across `WINNING_LINES`, N-player rotation (symbols `X O △ ● ■`).
- `src/tictactoe_gui.py` — Tkinter GUI; setup dialog (player count → per-player login/register → win target), board rendering, winning-line highlight.
- `src/auth.py` — `AuthManager` handles registration and login against a SQLite `users` table with salted SHA-256 password hashes.
- `tests/` — `unittest` suites for logic and auth.
- `tournament.db` — local SQLite database (created on first run; not committed).

## Subagents

Two custom agents in `.claude/`:

- **`programmer.md`** — writes Python code in `src/`. Uses type hints and docstrings. Does not write tests.
- **`tester.md`** — writes and runs tests in `tests/` using `unittest`. Does not modify source code, reports bugs instead.

Typical workflow: programmer implements → tester writes and runs tests → iterate.

## Conventions

- Python with type hints on all function signatures
- Short docstring on every function
- Tests use `unittest` (not pytest)
- Source code in `src/`, tests in `tests/`
- Keep GUI code separate from pure logic so logic stays unit-testable

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A demo project for learning Claude Code subagents. A simple Python calculator module built and tested using two cooperating subagents.

## Commands

```bash
# Run all tests
python -m unittest discover tests

# Run a single test file
python -m unittest tests.test_calculator
```

## Subagents

Two custom agents defined in the project root:

- **`programmer.md`** — Writes Python code in `src/`. Uses type hints and docstrings. Does not write tests.
- **`tester.md`** — Writes and runs tests in `tests/` using `unittest`. Does not modify source code, reports bugs instead.

Typical workflow: programmer implements → tester writes and runs tests → iterate.

## Conventions

- Python with type hints on all function signatures
- Short docstring on every function
- Tests use `unittest` (not pytest)
- Source code goes in `src/`, tests go in `tests/`

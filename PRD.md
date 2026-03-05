# Tic-Tac-Toe Tournament — Product Requirements Document

**Version:** 2.0
**Date:** 2026-03-05
**Status:** Completed

---

## 1. Product Summary

A desktop Tic-Tac-Toe application with a tournament mode for 2-5 players. Players must register and log in before playing. The game is fully mouse-driven, built in Python with a tkinter graphical interface. Two players compete on the board while the rest wait in a FIFO queue — after each round, players rotate automatically. The tournament ends when a player reaches a configurable win target.

---

## 2. Business Goals

| Goal | Description |
|------|-------------|
| Multiplayer entertainment | Enable 2-5 people to play on a single computer with automatic rotation |
| Player accounts | Registration and login with secure password storage |
| Zero installation | Runs on vanilla Python 3.x with no external dependencies |
| Easy deployment | A single `python3 -m src.tictactoe_gui` launches the entire application |
| Extensibility | Clean separation of logic and GUI allows easy interface replacement (web, mobile) |

---

## 3. Target Audience

- Users looking for a simple turn-based game for 2-5 people
- Clients needing a base desktop application for further development (e.g., network integration, AI)
- Educational teams teaching object-oriented programming and MVC patterns

---

## 4. Functional Scope

### 4.1 Player Authentication

| ID | Requirement | Priority |
|----|-------------|----------|
| F-01 | Player count selection screen (2-5 players) | Must |
| F-02 | Login/register screen for each player (username + password) | Must |
| F-03 | SQLite backend for user storage | Must |
| F-04 | SHA-256 password hashing with random salt | Must |
| F-05 | Validation: reject empty username/password, duplicate usernames | Must |
| F-06 | Prevent same user logging in twice in one tournament | Must |
| F-07 | Closing the dialog (X) exits the application | Must |
| F-08 | Win target input screen with default value of 3 | Must |
| F-09 | Win target validation — minimum value of 1, fallback to 3 on invalid input | Must |

### 4.2 Gameplay

| ID | Requirement | Priority |
|----|-------------|----------|
| F-10 | 3x3 board operated by mouse click | Must |
| F-11 | Alternating turns between X and O | Must |
| F-12 | Win detection — rows, columns, diagonals (8 lines) | Must |
| F-13 | Draw detection (full board with no winner) | Must |
| F-14 | Move blocking after the game ends | Must |
| F-15 | Move blocking on occupied cells | Must |
| F-16 | Winning line highlight — thick line drawn through the 3 winning cells | Must |
| F-17 | Move blocking after tournament winner is determined | Must |

### 4.3 Tournament Mode — 2-5 Player Rotation

| ID | Requirement | Priority |
|----|-------------|----------|
| F-20 | 2-5 players: 2 play, rest wait in FIFO queue | Must |
| F-21 | Rotation on win — winner stays, loser goes to back of queue, next in queue joins | Must |
| F-22 | Rotation on draw — the player who went first goes to back of queue, other stays, next in queue joins | Must |
| F-23 | 2-player special case — no queue rotation, just swap who goes first | Must |
| F-24 | Each player has a permanent symbol (X, O, △, ●, ■) independent of board position | Must |
| F-25 | Scoreboard tracking wins for each player | Must |
| F-26 | Configurable win target — tournament ends when a player reaches the target | Must |
| F-27 | Tournament winner announcement with congratulatory message | Must |
| F-28 | "Next Round" button disabled after a player wins the tournament | Must |

### 4.4 Graphical User Interface

| ID | Requirement | Priority |
|----|-------------|----------|
| F-30 | Info panel — who is currently playing (as X/O) and who is waiting | Must |
| F-31 | Status label — whose turn / who won / draw | Must |
| F-32 | Dynamic scoreboard with win count for all players | Must |
| F-32a | "First to N wins" label displayed on scoreboard | Must |
| F-33 | "Next Round" button — rotation after game ends (disabled during play) | Must |
| F-34 | "Restart Match" button — board reset without changing scores or rotation | Must |
| F-35 | "New Tournament" button — full reset (scores, rotation, board) | Must |
| F-36 | Color scheme: X=blue (#2563eb), O=red (#dc2626), waiting=purple (#7c3aed) | Should |
| F-37 | Dynamic waiting display — show all waiting players or empty for 2-player mode | Must |

---

## 5. Non-Functional Requirements

| ID | Requirement | Details |
|----|-------------|---------|
| NF-01 | Zero external dependencies | Python stdlib only (tkinter, sqlite3, hashlib) |
| NF-02 | Compatibility | Python 3.9+ on Windows, macOS, Linux |
| NF-03 | Responsiveness | Instant reaction to click (<50ms) |
| NF-04 | Testability | Game logic separated from GUI, covered by unit tests |
| NF-05 | Type safety | Type hints on all function signatures |
| NF-06 | Code documentation | Docstring on every function |
| NF-07 | Password security | SHA-256 hashing with unique random salt per user |

---

## 6. Architecture

```
src/
├── __init__.py              # package
├── auth.py                  # player authentication (SQLite)
├── tictactoe_logic.py       # game logic (model)
└── tictactoe_gui.py         # tkinter interface (view + controller)

tests/
├── __init__.py
├── test_auth.py             # auth unit tests (11 tests)
└── test_tictactoe.py        # game logic unit tests (241 tests)
```

### 6.1 Auth Layer (`auth.py`)

| Class | Responsibility |
|-------|----------------|
| `AuthManager` | SQLite-backed user registration, login, password hashing |

### 6.2 Logic Layer (`tictactoe_logic.py`)

| Class | Responsibility |
|-------|----------------|
| `Player` | Stores player name, symbol, and win count |
| `TicTacToeGame` | Board state, move validation, win/draw detection, winning line tracking |
| `Tournament` | 2-5 player management, FIFO queue rotation, scoreboard, win target |

### 6.3 GUI Layer (`tictactoe_gui.py`)

| Component | Responsibility |
|-----------|----------------|
| `ask_login_register()` | Multi-step dialog: player count → login/register → win target |
| `TicTacToeGUI` | Game window: canvas, info panel, scoreboard, buttons |

### 6.4 Flow Diagram

```
[Start] → [Player count] → [Login/Register ×N] → [Win target] → [Game window]
                                                                       │
                                                                  [Cell click]
                                                                       │
                                                                [Move → check winner]
                                                                   /         \
                                                          [Game ongoing]   [Game over]
                                                                              │
                                                                    [Next Round / Restart]
                                                                              │
                                                                        [Queue rotation]
                                                                              │
                                                                   [Check tournament winner]
                                                                       /            \
                                                               [Target reached]  [Continue]
                                                                     │                │
                                                            [Congratulations!]  [New round]
```

---

## 7. Rotation Rules — Details

### Win (X or O) — 3+ players

```
Before:  X=Player_A  |  O=Player_B  |  Queue=[Player_C, Player_D, ...]
X wins:
After:   X=Player_A  |  O=Player_C  |  Queue=[Player_D, ..., Player_B]

O wins:
After:   X=Player_B  |  O=Player_C  |  Queue=[Player_D, ..., Player_A]
```

The winner stays and plays as X (goes first). The loser goes to the back of the queue.

### Draw — 3+ players

```
Before:  X=Player_A (went first)  |  O=Player_B  |  Queue=[Player_C, ...]
After:   X=Player_B               |  O=Player_C  |  Queue=[..., Player_A]
```

The player who went first goes to the back of the queue. The other player stays (as X). The next from queue joins (as O).

### 2-player mode

No queue. Winner stays as X, loser becomes O. On draw, players swap who goes first.

---

## 8. Test Coverage

| Area | Test Count | Scope |
|------|------------|-------|
| AuthManager — register | 6 | Success, duplicate, empty fields, salt uniqueness |
| AuthManager — login | 5 | Success, wrong password, nonexistent user, empty fields |
| TicTacToeGame — initial state | 7 | Empty board, dimensions, X goes first |
| TicTacToeGame — moves | 10 | Valid, invalid, occupied cell, after game over |
| TicTacToeGame — wins | 16 | Rows, columns, diagonals (X and O) |
| TicTacToeGame — draw | 4 | Full board, status |
| TicTacToeGame — reset | 6 | State clearing |
| TicTacToeGame — edge cases | 4 | Win on last cell, multiple resets |
| Player | 5 | Creation, attributes, instance independence |
| Tournament — state | 10 | Initialization, player indices |
| Tournament — rotation | 21 | X win, O win, draw |
| Tournament — scores | 3 | Accumulation, no change on draw |
| Tournament — restart/reset | 10 | Match restart, tournament reset |
| Tournament — status | 7 | Text messages |
| Tournament — multiple rounds | 3 | Rotation cycle, cumulative scores |
| Tournament — edge cases | 7 | Indices, ranges, instance independence |
| Tournament — custom names | 31 | Names, Unicode, special characters, persistence through rotation/reset |
| Tournament — win target | 33 | Default/custom values, tournament winner detection, persistence, edge cases |
| TicTacToeGame — winning line | 10 | Initial state, during gameplay, draw, all 8 lines, reset |
| Tournament — validation | 5 | 0, 1, 6+ players raise ValueError; 2, 5 players OK |
| Tournament — 2 players | 4 | X wins, O wins, draw swap, reset |
| Tournament — 4 players | 7 | Queue order, rotation, waiting players, reset |
| Tournament — 5 players | 4 | Full rotation, draw rotation, waiting players |
| **Total** | **241** | |

---

## 9. Getting Started

```bash
# Run the game
python3 -m src.tictactoe_gui

# Run tests
python3 -m unittest discover tests
```

**System Requirements:**
- Python 3.9+
- tkinter (included in the standard Python distribution)
- Operating system: Windows, macOS, Linux

---

## 10. Future Development (Backlog)

| ID | Feature | Description |
|----|---------|-------------|
| B-01 | AI mode | Computer as one of the players (minimax / random) |
| B-02 | Network mode | Play over LAN / internet (socket / websocket) |
| B-03 | Animations | Animated X/O drawing, winning line animation |
| B-04 | Sound effects | Audio feedback on move, win, draw |
| B-05 | Board configuration | NxN board with configurable number in a line to win |
| B-06 | Game history | Save results to file / database |
| B-07 | Web interface | Replace tkinter with Flask/FastAPI + React |
| B-08 | Localization (i18n) | Multi-language interface support |

---

## 11. Glossary

| Term | Definition |
|------|------------|
| **Round** | A single game on the 3x3 board |
| **Tournament** | A series of rounds with 2-5 player rotation and score tracking |
| **Rotation** | Player swap after a round ends according to established rules |
| **Waiting queue** | FIFO queue of players waiting to play (empty in 2-player mode) |
| **Permanent symbol** | A unique player icon (X, O, △, ●, ■) that does not change throughout the tournament |
| **Board mark** | X or O — dynamically assigned depending on position in the rotation |
| **Win target** | The number of round wins a player must reach to win the tournament (default: 3) |
| **Winning line** | A visual line drawn through the 3 cells that form the winning combination |

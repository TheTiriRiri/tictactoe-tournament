"""Pure game logic for Tic-tac-toe with 3-player rotation."""

from typing import Optional

WINNING_LINES = [
    # Rows
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
    # Columns
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
    # Diagonals
    [(0, 0), (1, 1), (2, 2)],
    [(0, 2), (1, 1), (2, 0)],
]


class Player:
    """Represents a player in the tournament."""

    def __init__(self, name: str, symbol: str) -> None:
        """Initialize a player with a name and board symbol."""
        self.name = name
        self.symbol = symbol
        self.wins = 0


class TicTacToeGame:
    """Manages the state and rules of a single Tic-tac-toe game."""

    def __init__(self) -> None:
        """Initialize a new game with an empty board and X going first."""
        self.reset()

    def reset(self) -> None:
        """Reset the board to an empty state with X as the current player."""
        self.board: list[list[Optional[str]]] = [
            [None, None, None] for _ in range(3)
        ]
        self.current_player: str = "X"
        self.winner: Optional[str] = None
        self.game_over: bool = False

    def make_move(self, row: int, col: int) -> bool:
        """Place the current player's mark at (row, col). Returns True if the move was valid."""
        if self.game_over:
            return False
        if self.board[row][col] is not None:
            return False

        self.board[row][col] = self.current_player
        self.winner = self._check_winner()

        if self.winner is not None:
            self.game_over = True
        elif self.is_draw():
            self.game_over = True
        else:
            self.current_player = "O" if self.current_player == "X" else "X"

        return True

    def is_draw(self) -> bool:
        """Return True if the board is full and there is no winner."""
        if self.winner is not None:
            return False
        return all(self.board[r][c] is not None for r in range(3) for c in range(3))

    def _check_winner(self) -> Optional[str]:
        """Return the winning mark ('X' or 'O') or None if no winner yet."""
        for line in WINNING_LINES:
            values = [self.board[r][c] for r, c in line]
            if values[0] is not None and values[0] == values[1] == values[2]:
                return values[0]
        return None

    def get_status(self) -> str:
        """Return a human-readable status string for the current game state."""
        if self.winner:
            return f"Player {self.winner} wins!"
        if self.is_draw():
            return "It's a draw!"
        return f"Player {self.current_player}'s turn"


class Tournament:
    """Manages a 3-player rotation tournament."""

    def __init__(self, names: Optional[list[str]] = None, win_target: int = 3) -> None:
        """Initialize the tournament with 3 players and the first match."""
        if names is None:
            names = ["Player 1", "Player 2", "Player 3"]
        self.players: list[Player] = [
            Player(names[0], "X"),
            Player(names[1], "O"),
            Player(names[2], "\u25B3"),
        ]
        self.win_target: int = win_target
        # Indices into self.players: who plays X, who plays O, who waits
        self.x_player_idx: int = 0
        self.o_player_idx: int = 1
        self.waiting_idx: int = 2
        # Track who went first (the X player) for draw rotation
        self.first_player_idx: int = 0
        self.game = TicTacToeGame()

    def reset_tournament(self) -> None:
        """Reset all scores and return to the initial player arrangement."""
        for p in self.players:
            p.wins = 0
        self.x_player_idx = 0
        self.o_player_idx = 1
        self.waiting_idx = 2
        self.first_player_idx = 0
        self.game.reset()

    def restart_match(self) -> None:
        """Restart the current match without changing player arrangement or scores."""
        self.game.reset()

    def get_active_player(self) -> Player:
        """Return the Player object whose turn it is."""
        if self.game.current_player == "X":
            return self.players[self.x_player_idx]
        return self.players[self.o_player_idx]

    def get_x_player(self) -> Player:
        """Return the player currently assigned to X."""
        return self.players[self.x_player_idx]

    def get_o_player(self) -> Player:
        """Return the player currently assigned to O."""
        return self.players[self.o_player_idx]

    def get_waiting_player(self) -> Player:
        """Return the player currently sitting out."""
        return self.players[self.waiting_idx]

    def get_tournament_winner(self) -> Optional[Player]:
        """Return the first player who reached win_target wins, or None."""
        for player in self.players:
            if player.wins >= self.win_target:
                return player
        return None

    def get_winner_player(self) -> Optional[Player]:
        """Return the Player who won, or None."""
        if self.game.winner == "X":
            return self.players[self.x_player_idx]
        if self.game.winner == "O":
            return self.players[self.o_player_idx]
        return None

    def get_status(self) -> str:
        """Return a status string using player names and symbols."""
        if self.game.winner:
            winner = self.get_winner_player()
            assert winner is not None
            return f"{winner.name} ({winner.symbol}) wins!"
        if self.game.is_draw():
            return "It's a draw!"
        active = self.get_active_player()
        return f"{active.name} ({active.symbol})'s turn  —  playing as {self.game.current_player}"

    def advance_round(self) -> None:
        """Rotate players after a game ends according to the rules."""
        if self.game.winner == "X":
            # X won: X stays as X, waiting player becomes O, loser (O) sits out
            loser_idx = self.o_player_idx
            self.o_player_idx = self.waiting_idx
            self.waiting_idx = loser_idx
            self.players[self.x_player_idx].wins += 1
        elif self.game.winner == "O":
            # O won: O stays as X (winner goes first), waiting player becomes O, loser (X) sits out
            loser_idx = self.x_player_idx
            winner_idx = self.o_player_idx
            self.x_player_idx = winner_idx
            self.o_player_idx = self.waiting_idx
            self.waiting_idx = loser_idx
            self.players[winner_idx].wins += 1
        else:
            # Draw: player who went first sits out, other stays, waiting joins
            sat_first = self.first_player_idx
            stayed = self.o_player_idx
            new_joiner = self.waiting_idx
            self.x_player_idx = stayed
            self.o_player_idx = new_joiner
            self.waiting_idx = sat_first

        self.first_player_idx = self.x_player_idx
        self.game.reset()

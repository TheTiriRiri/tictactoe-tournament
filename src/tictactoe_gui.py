"""Tkinter GUI for Tic-tac-toe with 3-player rotation."""

import tkinter as tk
from typing import Optional
from src.tictactoe_logic import Tournament


def ask_player_names(parent: tk.Tk) -> Optional[list[str]]:
    """Show a dialog with 3 entry fields and return the player names, or None if cancelled."""
    result: Optional[list[str]] = None

    dialog = tk.Toplevel(parent)
    dialog.title("Enter Player Names")
    dialog.resizable(False, False)
    dialog.grab_set()

    tk.Label(dialog, text="Enter names for each player:", font=("Arial", 14)).grid(
        row=0, column=0, columnspan=2, padx=20, pady=(15, 10),
    )

    entries: list[tk.Entry] = []
    defaults = ["Player 1", "Player 2", "Player 3"]
    for i in range(3):
        tk.Label(dialog, text=f"Player {i + 1}:", font=("Arial", 12)).grid(
            row=i + 1, column=0, padx=(20, 5), pady=5, sticky="e",
        )
        entry = tk.Entry(dialog, font=("Arial", 12), width=20)
        entry.insert(0, "")
        entry.grid(row=i + 1, column=1, padx=(5, 20), pady=5)
        entries.append(entry)

    def on_start() -> None:
        """Collect names from entries and close the dialog."""
        nonlocal result
        names = []
        for i, entry in enumerate(entries):
            name = entry.get().strip()
            names.append(name if name else defaults[i])
        result = names
        dialog.destroy()

    def on_close() -> None:
        """Handle the dialog being closed without starting."""
        dialog.destroy()
        parent.destroy()

    tk.Button(
        dialog, text="Start Game", font=("Arial", 13, "bold"), command=on_start,
    ).grid(row=4, column=0, columnspan=2, pady=(10, 15))

    dialog.protocol("WM_DELETE_WINDOW", on_close)

    entries[0].focus_set()
    parent.wait_window(dialog)

    return result


class TicTacToeGUI:
    """A mouse-driven tkinter interface for 3-player Tic-tac-toe."""

    CELL_SIZE = 120
    FONT_MARK = ("Arial", 40, "bold")
    FONT_STATUS = ("Arial", 18)
    FONT_BUTTON = ("Arial", 14)
    FONT_INFO = ("Arial", 13)
    FONT_SCORE = ("Arial", 13, "bold")
    COLOR_X = "#2563eb"
    COLOR_O = "#dc2626"
    COLOR_WAIT = "#7c3aed"
    COLOR_BG = "#f8fafc"
    COLOR_LINE = "#334155"
    COLOR_PANEL = "#e2e8f0"

    def __init__(self, root: tk.Tk, names: Optional[list[str]] = None) -> None:
        """Set up the window, canvas, info panels, and buttons."""
        self.root = root
        self.root.title("Tic-tac-toe — 3-Player Tournament")
        self.root.resizable(False, False)
        self.root.configure(bg=self.COLOR_BG)

        self.player_names = names
        self.tournament = Tournament(names=self.player_names)

        # --- Top info panel: who's playing, who's waiting ---
        info_frame = tk.Frame(root, bg=self.COLOR_BG)
        info_frame.pack(padx=20, pady=(15, 5))

        self.playing_var = tk.StringVar()
        self.waiting_var = tk.StringVar()

        playing_label = tk.Label(
            info_frame, textvariable=self.playing_var,
            font=self.FONT_INFO, bg=self.COLOR_BG, anchor="w",
        )
        playing_label.pack(fill="x")

        waiting_label = tk.Label(
            info_frame, textvariable=self.waiting_var,
            font=self.FONT_INFO, bg=self.COLOR_BG, fg=self.COLOR_WAIT, anchor="w",
        )
        waiting_label.pack(fill="x")

        # --- Board canvas ---
        board_px = self.CELL_SIZE * 3

        self.canvas = tk.Canvas(
            root, width=board_px, height=board_px,
            bg=self.COLOR_BG, highlightthickness=0,
        )
        self.canvas.pack(padx=20, pady=(10, 10))
        self.canvas.bind("<Button-1>", self._on_click)

        # --- Status label ---
        self.status_var = tk.StringVar()
        status_label = tk.Label(
            root, textvariable=self.status_var,
            font=self.FONT_STATUS, bg=self.COLOR_BG,
        )
        status_label.pack(pady=(0, 5))

        # --- Scoreboard ---
        score_frame = tk.Frame(root, bg=self.COLOR_PANEL, bd=1, relief="groove")
        score_frame.pack(padx=20, pady=(0, 10), fill="x")

        tk.Label(
            score_frame, text="Scoreboard", font=self.FONT_SCORE,
            bg=self.COLOR_PANEL,
        ).pack(pady=(5, 2))

        self.score_var = tk.StringVar()
        tk.Label(
            score_frame, textvariable=self.score_var,
            font=self.FONT_INFO, bg=self.COLOR_PANEL, justify="center",
        ).pack(pady=(0, 5))

        # --- Buttons ---
        btn_frame = tk.Frame(root, bg=self.COLOR_BG)
        btn_frame.pack(pady=(0, 15))

        self.next_btn = tk.Button(
            btn_frame, text="Next Round", font=self.FONT_BUTTON,
            command=self._next_round, state="disabled",
        )
        self.next_btn.pack(side="left", padx=5)

        restart_btn = tk.Button(
            btn_frame, text="Restart Match", font=self.FONT_BUTTON,
            command=self._restart,
        )
        restart_btn.pack(side="left", padx=5)

        new_tourn_btn = tk.Button(
            btn_frame, text="New Tournament", font=self.FONT_BUTTON,
            command=self._new_tournament,
        )
        new_tourn_btn.pack(side="left", padx=5)

        self._draw_grid()
        self._update_display()

    def _draw_grid(self) -> None:
        """Draw the 3x3 grid lines on the canvas."""
        size = self.CELL_SIZE * 3
        for i in range(1, 3):
            pos = i * self.CELL_SIZE
            self.canvas.create_line(pos, 0, pos, size, fill=self.COLOR_LINE, width=2)
            self.canvas.create_line(0, pos, size, pos, fill=self.COLOR_LINE, width=2)

    def _on_click(self, event: tk.Event) -> None:
        """Handle a mouse click on the board canvas."""
        col = event.x // self.CELL_SIZE
        row = event.y // self.CELL_SIZE

        if not (0 <= row <= 2 and 0 <= col <= 2):
            return

        game = self.tournament.game
        mark = game.current_player
        if game.make_move(row, col):
            self._draw_mark(row, col, mark)
            self._update_display()
            if game.game_over:
                self.next_btn.config(state="normal")

    def _draw_mark(self, row: int, col: int, mark: str) -> None:
        """Draw an X or O in the specified cell."""
        cx = col * self.CELL_SIZE + self.CELL_SIZE // 2
        cy = row * self.CELL_SIZE + self.CELL_SIZE // 2
        color = self.COLOR_X if mark == "X" else self.COLOR_O
        self.canvas.create_text(
            cx, cy, text=mark, font=self.FONT_MARK, fill=color,
        )

    def _update_display(self) -> None:
        """Refresh all info labels to reflect the current tournament state."""
        t = self.tournament
        xp = t.get_x_player()
        op = t.get_o_player()
        wp = t.get_waiting_player()

        self.playing_var.set(
            f"Playing:  {xp.name} ({xp.symbol}) as X   vs   {op.name} ({op.symbol}) as O"
        )
        self.waiting_var.set(f"Waiting:  {wp.name} ({wp.symbol})")
        self.status_var.set(t.get_status())
        self.score_var.set(
            f"{t.players[0].name} ({t.players[0].symbol}): {t.players[0].wins}    "
            f"{t.players[1].name} ({t.players[1].symbol}): {t.players[1].wins}    "
            f"{t.players[2].name} ({t.players[2].symbol}): {t.players[2].wins}"
        )

    def _next_round(self) -> None:
        """Advance to the next round after a game ends."""
        self.tournament.advance_round()
        self.canvas.delete("all")
        self._draw_grid()
        self.next_btn.config(state="disabled")
        self._update_display()

    def _restart(self) -> None:
        """Restart the current match without changing scores or rotation."""
        self.tournament.restart_match()
        self.canvas.delete("all")
        self._draw_grid()
        self.next_btn.config(state="disabled")
        self._update_display()

    def _new_tournament(self) -> None:
        """Reset everything: scores, rotation, and board."""
        self.tournament.reset_tournament()
        self.canvas.delete("all")
        self._draw_grid()
        self.next_btn.config(state="disabled")
        self._update_display()


def main() -> None:
    """Launch the Tic-tac-toe GUI application."""
    root = tk.Tk()
    root.withdraw()

    names = ask_player_names(root)
    if names is None:
        return

    root.deiconify()
    TicTacToeGUI(root, names=names)
    root.mainloop()


if __name__ == "__main__":
    main()

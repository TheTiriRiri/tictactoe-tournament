"""Tkinter GUI for Tic-tac-toe with 2-5 player rotation and login/register."""

import tkinter as tk
from typing import Optional
from src.tictactoe_logic import Tournament
from src.auth import AuthManager


def ask_login_register(parent: tk.Tk, auth: AuthManager) -> Optional[tuple[list[str], int]]:
    """Multi-step dialog: player count -> login/register each -> win target. Returns (names, win_target) or None."""
    result: Optional[tuple[list[str], int]] = None

    dialog = tk.Toplevel(parent)
    dialog.title("Tournament Setup")
    dialog.resizable(False, False)
    dialog.grab_set()

    container = tk.Frame(dialog)
    container.pack(padx=20, pady=15)

    # Shared state
    player_count = tk.IntVar(value=3)
    logged_in_names: list[str] = []

    def clear_container() -> None:
        """Remove all widgets from the container."""
        for w in container.winfo_children():
            w.destroy()

    def show_count_screen() -> None:
        """Screen 1: Choose number of players."""
        clear_container()
        tk.Label(container, text="How many players?", font=("Arial", 14)).pack(pady=(0, 10))
        for n in range(2, 6):
            tk.Radiobutton(
                container, text=f"{n} players", variable=player_count, value=n,
                font=("Arial", 12),
            ).pack(anchor="w")
        tk.Button(
            container, text="Next", font=("Arial", 13, "bold"),
            command=lambda: show_login_screen(0),
        ).pack(pady=(10, 0))

    def show_login_screen(player_idx: int) -> None:
        """Screen 2: Login or register for player N."""
        clear_container()
        total = player_count.get()
        logged_in_names[:] = logged_in_names[:player_idx]  # trim if going back

        tk.Label(
            container, text=f"Player {player_idx + 1} of {total}", font=("Arial", 14),
        ).pack(pady=(0, 10))

        tk.Label(container, text="Username:", font=("Arial", 12)).pack(anchor="w")
        user_entry = tk.Entry(container, font=("Arial", 12), width=20)
        user_entry.pack(pady=(0, 5))

        tk.Label(container, text="Password:", font=("Arial", 12)).pack(anchor="w")
        pass_entry = tk.Entry(container, font=("Arial", 12), width=20, show="*")
        pass_entry.pack(pady=(0, 5))

        error_var = tk.StringVar()
        tk.Label(container, textvariable=error_var, font=("Arial", 10), fg="red").pack()

        def do_auth(action: str) -> None:
            """Try login or register, then advance to next player or win target."""
            username = user_entry.get().strip()
            password = pass_entry.get()

            if action == "register":
                ok, msg = auth.register(username, password)
            else:
                ok, msg = auth.login(username, password)

            if not ok:
                error_var.set(msg)
                return

            if username in logged_in_names:
                error_var.set("This user is already logged in")
                return

            logged_in_names.append(username)

            if len(logged_in_names) < total:
                show_login_screen(len(logged_in_names))
            else:
                show_win_target_screen()

        btn_frame = tk.Frame(container)
        btn_frame.pack(pady=(5, 0))
        tk.Button(btn_frame, text="Login", font=("Arial", 12), command=lambda: do_auth("login")).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Register", font=("Arial", 12), command=lambda: do_auth("register")).pack(side="left", padx=5)

        user_entry.focus_set()

    def show_win_target_screen() -> None:
        """Screen 3: Set win target."""
        clear_container()
        tk.Label(container, text="Wins needed to win tournament:", font=("Arial", 14)).pack(pady=(0, 10))

        win_entry = tk.Entry(container, font=("Arial", 12), width=5)
        win_entry.insert(0, "3")
        win_entry.pack()

        def on_start() -> None:
            nonlocal result
            try:
                win_target = max(1, int(win_entry.get().strip()))
            except ValueError:
                win_target = 3
            result = (list(logged_in_names), win_target)
            dialog.destroy()

        tk.Button(
            container, text="Start Tournament", font=("Arial", 13, "bold"),
            command=on_start,
        ).pack(pady=(10, 0))

    def on_close() -> None:
        """Handle the dialog being closed without starting."""
        dialog.destroy()
        parent.destroy()

    dialog.protocol("WM_DELETE_WINDOW", on_close)
    show_count_screen()
    parent.wait_window(dialog)

    return result


class TicTacToeGUI:
    """A mouse-driven tkinter interface for 2-5 player Tic-tac-toe."""

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

    def __init__(self, root: tk.Tk, names: Optional[list[str]] = None, win_target: int = 3) -> None:
        """Set up the window, canvas, info panels, and buttons."""
        self.root = root
        self.root.title("Tic-tac-toe \u2014 Tournament")
        self.root.resizable(False, False)
        self.root.configure(bg=self.COLOR_BG)

        self.player_names = names
        self.win_target = win_target
        self.tournament = Tournament(names=self.player_names, win_target=self.win_target)

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

        self.target_var = tk.StringVar()
        tk.Label(
            score_frame, textvariable=self.target_var,
            font=self.FONT_INFO, bg=self.COLOR_PANEL, fg="#64748b",
        ).pack(pady=(0, 2))

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
        if self.tournament.get_tournament_winner() is not None:
            return

        game = self.tournament.game
        mark = game.current_player
        if game.make_move(row, col):
            self._draw_mark(row, col, mark)
            if game.winner is not None and game.winning_line is not None:
                self._draw_winning_line(game.winning_line, game.winner)
            self._update_display()
            if game.game_over and self.tournament.get_tournament_winner() is None:
                self.next_btn.config(state="normal")

    def _draw_winning_line(self, cells: list[tuple[int, int]], winner: str) -> None:
        """Draw a thick line through the centers of the 3 winning cells."""
        color = self.COLOR_X if winner == "X" else self.COLOR_O
        first_row, first_col = cells[0]
        last_row, last_col = cells[2]
        x1 = first_col * self.CELL_SIZE + self.CELL_SIZE // 2
        y1 = first_row * self.CELL_SIZE + self.CELL_SIZE // 2
        x2 = last_col * self.CELL_SIZE + self.CELL_SIZE // 2
        y2 = last_row * self.CELL_SIZE + self.CELL_SIZE // 2
        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=5, capstyle="round")

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

        self.playing_var.set(
            f"Playing:  {xp.name} ({xp.symbol}) as X   vs   {op.name} ({op.symbol}) as O"
        )

        waiting = t.get_waiting_players()
        if waiting:
            waiting_str = ", ".join(f"{p.name} ({p.symbol})" for p in waiting)
            self.waiting_var.set(f"Waiting:  {waiting_str}")
        else:
            self.waiting_var.set("")

        self.target_var.set(f"First to {t.win_target} wins")
        self.score_var.set(
            "    ".join(f"{p.name} ({p.symbol}): {p.wins}" for p in t.players)
        )

        champion = t.get_tournament_winner()
        if champion is not None:
            self.status_var.set(
                f"Congratulations! {champion.name} wins the tournament!"
            )
            self.next_btn.config(state="disabled")
        else:
            self.status_var.set(t.get_status())

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

    auth = AuthManager(db_path="tournament.db")

    setup = ask_login_register(root, auth)
    if setup is None:
        auth.close()
        return

    names, win_target = setup
    root.deiconify()
    TicTacToeGUI(root, names=names, win_target=win_target)
    root.mainloop()
    auth.close()


if __name__ == "__main__":
    main()

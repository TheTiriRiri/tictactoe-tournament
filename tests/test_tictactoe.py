"""Comprehensive tests for the Tic-tac-toe game logic with 3-player tournament."""

import unittest
from typing import List, Tuple

from src.tictactoe_logic import TicTacToeGame, Player, Tournament, WINNING_LINES


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _play_moves(game: TicTacToeGame, moves: List[Tuple[int, int]]) -> None:
    """Play a sequence of moves on the given game."""
    for r, c in moves:
        game.make_move(r, c)


def _force_x_win(game: TicTacToeGame) -> None:
    """X wins top row."""
    _play_moves(game, [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)])


def _force_o_win(game: TicTacToeGame) -> None:
    """O wins row 1."""
    _play_moves(game, [(0, 0), (1, 0), (0, 1), (1, 1), (2, 2), (1, 2)])


def _force_draw(game: TicTacToeGame) -> None:
    """Play to a draw (no winner)."""
    _play_moves(game, [
        (0, 0), (0, 1), (0, 2),
        (1, 1), (1, 0), (1, 2),
        (2, 1), (2, 0), (2, 2),
    ])


# ===========================================================================
# TicTacToeGame tests (kept / updated from original)
# ===========================================================================

class TestInitialState(unittest.TestCase):
    """Tests for the initial state of a new game."""

    def setUp(self) -> None:
        self.game = TicTacToeGame()

    def test_board_is_empty(self) -> None:
        for r in range(3):
            for c in range(3):
                self.assertIsNone(self.game.board[r][c])

    def test_board_dimensions(self) -> None:
        self.assertEqual(len(self.game.board), 3)
        for row in self.game.board:
            self.assertEqual(len(row), 3)

    def test_current_player_is_x(self) -> None:
        self.assertEqual(self.game.current_player, "X")

    def test_no_winner(self) -> None:
        self.assertIsNone(self.game.winner)

    def test_game_not_over(self) -> None:
        self.assertFalse(self.game.game_over)

    def test_status_x_turn(self) -> None:
        self.assertEqual(self.game.get_status(), "Player X's turn")

    def test_is_draw_false(self) -> None:
        self.assertFalse(self.game.is_draw())


class TestValidMoves(unittest.TestCase):

    def setUp(self) -> None:
        self.game = TicTacToeGame()

    def test_first_move_returns_true(self) -> None:
        self.assertTrue(self.game.make_move(0, 0))

    def test_first_move_places_x(self) -> None:
        self.game.make_move(0, 0)
        self.assertEqual(self.game.board[0][0], "X")

    def test_second_move_places_o(self) -> None:
        self.game.make_move(0, 0)
        self.game.make_move(1, 1)
        self.assertEqual(self.game.board[1][1], "O")

    def test_all_cells_can_be_played(self) -> None:
        moves = [(0, 0), (0, 1), (0, 2),
                 (1, 1), (1, 0), (1, 2),
                 (2, 1), (2, 0), (2, 2)]
        for r, c in moves:
            self.assertTrue(self.game.make_move(r, c), f"Move at ({r},{c}) should be valid")


class TestTurnAlternation(unittest.TestCase):

    def setUp(self) -> None:
        self.game = TicTacToeGame()

    def test_alternates_after_each_move(self) -> None:
        self.assertEqual(self.game.current_player, "X")
        self.game.make_move(0, 0)
        self.assertEqual(self.game.current_player, "O")
        self.game.make_move(0, 1)
        self.assertEqual(self.game.current_player, "X")
        self.game.make_move(0, 2)
        self.assertEqual(self.game.current_player, "O")

    def test_does_not_switch_on_invalid_move(self) -> None:
        self.game.make_move(0, 0)  # X
        self.assertEqual(self.game.current_player, "O")
        self.game.make_move(0, 0)  # invalid
        self.assertEqual(self.game.current_player, "O")

    def test_does_not_switch_on_winning_move(self) -> None:
        _force_x_win(self.game)
        self.assertEqual(self.game.current_player, "X")


class TestInvalidMoves(unittest.TestCase):

    def setUp(self) -> None:
        self.game = TicTacToeGame()

    def test_occupied_cell_returns_false(self) -> None:
        self.game.make_move(0, 0)
        self.assertFalse(self.game.make_move(0, 0))

    def test_occupied_cell_does_not_change_board(self) -> None:
        self.game.make_move(0, 0)  # X
        self.game.make_move(0, 0)  # invalid
        self.assertEqual(self.game.board[0][0], "X")

    def test_move_after_win_returns_false(self) -> None:
        _force_x_win(self.game)
        self.assertFalse(self.game.make_move(2, 2))

    def test_move_after_draw_returns_false(self) -> None:
        _force_draw(self.game)
        self.assertTrue(self.game.game_over)
        self.assertFalse(self.game.make_move(0, 0))

    def test_out_of_bounds_raises_error(self) -> None:
        with self.assertRaises(IndexError):
            self.game.make_move(3, 0)
        with self.assertRaises(IndexError):
            self.game.make_move(0, 3)

    def test_negative_index_behavior(self) -> None:
        result = self.game.make_move(-1, -1)
        self.assertTrue(result)
        self.assertEqual(self.game.board[2][2], "X")


class TestWinDetectionRows(unittest.TestCase):

    def test_x_wins_row_0(self) -> None:
        g = TicTacToeGame()
        _play_moves(g, [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)])
        self.assertEqual(g.winner, "X")
        self.assertTrue(g.game_over)

    def test_x_wins_row_1(self) -> None:
        g = TicTacToeGame()
        _play_moves(g, [(1, 0), (0, 0), (1, 1), (0, 1), (1, 2)])
        self.assertEqual(g.winner, "X")

    def test_x_wins_row_2(self) -> None:
        g = TicTacToeGame()
        _play_moves(g, [(2, 0), (0, 0), (2, 1), (0, 1), (2, 2)])
        self.assertEqual(g.winner, "X")

    def test_o_wins_row_0(self) -> None:
        g = TicTacToeGame()
        _play_moves(g, [(1, 0), (0, 0), (1, 1), (0, 1), (2, 2), (0, 2)])
        self.assertEqual(g.winner, "O")

    def test_o_wins_row_1(self) -> None:
        g = TicTacToeGame()
        _play_moves(g, [(0, 0), (1, 0), (0, 1), (1, 1), (2, 2), (1, 2)])
        self.assertEqual(g.winner, "O")

    def test_o_wins_row_2(self) -> None:
        g = TicTacToeGame()
        _play_moves(g, [(0, 0), (2, 0), (0, 1), (2, 1), (1, 1), (2, 2)])
        self.assertEqual(g.winner, "O")


class TestWinDetectionColumns(unittest.TestCase):

    def test_x_wins_col_0(self) -> None:
        g = TicTacToeGame()
        _play_moves(g, [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)])
        self.assertEqual(g.winner, "X")

    def test_x_wins_col_1(self) -> None:
        g = TicTacToeGame()
        _play_moves(g, [(0, 1), (0, 0), (1, 1), (1, 0), (2, 1)])
        self.assertEqual(g.winner, "X")

    def test_x_wins_col_2(self) -> None:
        g = TicTacToeGame()
        _play_moves(g, [(0, 2), (0, 0), (1, 2), (1, 0), (2, 2)])
        self.assertEqual(g.winner, "X")

    def test_o_wins_col_0(self) -> None:
        g = TicTacToeGame()
        _play_moves(g, [(0, 1), (0, 0), (1, 1), (1, 0), (0, 2), (2, 0)])
        self.assertEqual(g.winner, "O")

    def test_o_wins_col_1(self) -> None:
        g = TicTacToeGame()
        _play_moves(g, [(0, 0), (0, 1), (1, 0), (1, 1), (2, 2), (2, 1)])
        self.assertEqual(g.winner, "O")

    def test_o_wins_col_2(self) -> None:
        g = TicTacToeGame()
        _play_moves(g, [(0, 0), (0, 2), (1, 0), (1, 2), (2, 1), (2, 2)])
        self.assertEqual(g.winner, "O")


class TestWinDetectionDiagonals(unittest.TestCase):

    def test_x_wins_main_diagonal(self) -> None:
        g = TicTacToeGame()
        _play_moves(g, [(0, 0), (0, 1), (1, 1), (0, 2), (2, 2)])
        self.assertEqual(g.winner, "X")

    def test_x_wins_anti_diagonal(self) -> None:
        g = TicTacToeGame()
        _play_moves(g, [(0, 2), (0, 0), (1, 1), (0, 1), (2, 0)])
        self.assertEqual(g.winner, "X")

    def test_o_wins_main_diagonal(self) -> None:
        g = TicTacToeGame()
        _play_moves(g, [(0, 1), (0, 0), (0, 2), (1, 1), (1, 0), (2, 2)])
        self.assertEqual(g.winner, "O")

    def test_o_wins_anti_diagonal(self) -> None:
        g = TicTacToeGame()
        _play_moves(g, [(0, 0), (0, 2), (0, 1), (1, 1), (1, 0), (2, 0)])
        self.assertEqual(g.winner, "O")


class TestDrawDetection(unittest.TestCase):

    def setUp(self) -> None:
        self.game = TicTacToeGame()

    def test_draw_game(self) -> None:
        _force_draw(self.game)
        self.assertIsNone(self.game.winner)
        self.assertTrue(self.game.is_draw())
        self.assertTrue(self.game.game_over)

    def test_is_draw_false_when_winner_exists(self) -> None:
        moves = [(0, 0), (0, 1), (0, 2),
                 (1, 0), (1, 1), (1, 2),
                 (2, 1), (2, 0), (2, 2)]
        for r, c in moves:
            self.game.make_move(r, c)
        self.assertEqual(self.game.winner, "X")
        self.assertFalse(self.game.is_draw())

    def test_not_draw_mid_game(self) -> None:
        self.game.make_move(0, 0)
        self.assertFalse(self.game.is_draw())
        self.assertFalse(self.game.game_over)

    def test_draw_status_message(self) -> None:
        _force_draw(self.game)
        self.assertEqual(self.game.get_status(), "It's a draw!")


class TestGameReset(unittest.TestCase):

    def setUp(self) -> None:
        self.game = TicTacToeGame()

    def test_reset_clears_board(self) -> None:
        self.game.make_move(0, 0)
        self.game.make_move(1, 1)
        self.game.reset()
        for r in range(3):
            for c in range(3):
                self.assertIsNone(self.game.board[r][c])

    def test_reset_sets_x_first(self) -> None:
        self.game.make_move(0, 0)
        self.game.reset()
        self.assertEqual(self.game.current_player, "X")

    def test_reset_clears_winner(self) -> None:
        _force_x_win(self.game)
        self.assertEqual(self.game.winner, "X")
        self.game.reset()
        self.assertIsNone(self.game.winner)

    def test_reset_clears_game_over(self) -> None:
        _force_x_win(self.game)
        self.assertTrue(self.game.game_over)
        self.game.reset()
        self.assertFalse(self.game.game_over)

    def test_can_play_after_reset(self) -> None:
        _force_x_win(self.game)
        self.game.reset()
        self.assertTrue(self.game.make_move(0, 0))
        self.assertEqual(self.game.board[0][0], "X")

    def test_reset_creates_independent_rows(self) -> None:
        self.game.reset()
        self.game.board[0][0] = "X"
        self.assertIsNone(self.game.board[1][0])
        self.assertIsNone(self.game.board[2][0])


class TestGetStatus(unittest.TestCase):

    def setUp(self) -> None:
        self.game = TicTacToeGame()

    def test_status_x_turn(self) -> None:
        self.assertEqual(self.game.get_status(), "Player X's turn")

    def test_status_o_turn(self) -> None:
        self.game.make_move(0, 0)
        self.assertEqual(self.game.get_status(), "Player O's turn")

    def test_status_x_wins(self) -> None:
        _force_x_win(self.game)
        self.assertEqual(self.game.get_status(), "Player X wins!")

    def test_status_o_wins(self) -> None:
        _force_o_win(self.game)
        self.assertEqual(self.game.get_status(), "Player O wins!")

    def test_status_draw(self) -> None:
        _force_draw(self.game)
        self.assertEqual(self.game.get_status(), "It's a draw!")


class TestWinningLinesConstant(unittest.TestCase):

    def test_eight_winning_lines(self) -> None:
        self.assertEqual(len(WINNING_LINES), 8)

    def test_each_line_has_three_cells(self) -> None:
        for line in WINNING_LINES:
            self.assertEqual(len(line), 3)

    def test_all_coordinates_in_range(self) -> None:
        for line in WINNING_LINES:
            for r, c in line:
                self.assertIn(r, (0, 1, 2))
                self.assertIn(c, (0, 1, 2))


class TestCheckWinner(unittest.TestCase):

    def test_no_winner_empty_board(self) -> None:
        game = TicTacToeGame()
        self.assertIsNone(game._check_winner())

    def test_no_winner_partial_board(self) -> None:
        game = TicTacToeGame()
        game.make_move(0, 0)
        game.make_move(1, 1)
        self.assertIsNone(game._check_winner())


class TestEdgeCases(unittest.TestCase):

    def test_win_on_last_cell(self) -> None:
        game = TicTacToeGame()
        moves = [(0, 0), (0, 1), (0, 2),
                 (1, 0), (1, 1), (1, 2),
                 (2, 1), (2, 0), (2, 2)]
        for r, c in moves:
            game.make_move(r, c)
        self.assertEqual(game.winner, "X")
        self.assertFalse(game.is_draw())
        self.assertTrue(game.game_over)

    def test_multiple_resets(self) -> None:
        game = TicTacToeGame()
        game.reset()
        game.reset()
        game.reset()
        self.assertEqual(game.current_player, "X")
        self.assertIsNone(game.winner)
        self.assertFalse(game.game_over)

    def test_game_instances_are_independent(self) -> None:
        game1 = TicTacToeGame()
        game2 = TicTacToeGame()
        game1.make_move(0, 0)
        self.assertIsNone(game2.board[0][0])

    def test_immediate_winner_check_after_three_moves(self) -> None:
        game = TicTacToeGame()
        game.make_move(0, 0)  # X
        self.assertIsNone(game.winner)
        game.make_move(1, 0)  # O
        self.assertIsNone(game.winner)
        game.make_move(0, 1)  # X (2nd)
        self.assertIsNone(game.winner)
        game.make_move(1, 1)  # O
        self.assertIsNone(game.winner)
        game.make_move(0, 2)  # X (3rd) - wins!
        self.assertEqual(game.winner, "X")


# ===========================================================================
# Player class tests (new)
# ===========================================================================

class TestPlayer(unittest.TestCase):
    """Tests for the Player dataclass-like object."""

    def test_creation_with_name_and_symbol(self) -> None:
        p = Player("Alice", "X")
        self.assertEqual(p.name, "Alice")
        self.assertEqual(p.symbol, "X")

    def test_default_wins_is_zero(self) -> None:
        p = Player("Bob", "O")
        self.assertEqual(p.wins, 0)

    def test_wins_can_be_incremented(self) -> None:
        p = Player("Carol", "\u25B3")
        p.wins += 1
        self.assertEqual(p.wins, 1)
        p.wins += 5
        self.assertEqual(p.wins, 6)

    def test_unicode_symbol(self) -> None:
        """Player 3 uses a triangle symbol."""
        p = Player("Player 3", "\u25B3")
        self.assertEqual(p.symbol, "\u25B3")

    def test_players_are_independent(self) -> None:
        p1 = Player("A", "X")
        p2 = Player("B", "O")
        p1.wins += 3
        self.assertEqual(p2.wins, 0)


# ===========================================================================
# Tournament class tests (new)
# ===========================================================================

class TestTournamentInitialState(unittest.TestCase):
    """Tests for the initial state of a Tournament."""

    def setUp(self) -> None:
        self.t = Tournament()

    def test_three_players(self) -> None:
        self.assertEqual(len(self.t.players), 3)

    def test_player_names(self) -> None:
        names = [p.name for p in self.t.players]
        self.assertEqual(names, ["Player 1", "Player 2", "Player 3"])

    def test_player_symbols(self) -> None:
        symbols = [p.symbol for p in self.t.players]
        self.assertEqual(symbols, ["X", "O", "\u25B3"])

    def test_all_wins_zero(self) -> None:
        for p in self.t.players:
            self.assertEqual(p.wins, 0)

    def test_x_player_is_player_1(self) -> None:
        self.assertIs(self.t.get_x_player(), self.t.players[0])

    def test_o_player_is_player_2(self) -> None:
        self.assertIs(self.t.get_o_player(), self.t.players[1])

    def test_waiting_player_is_player_3(self) -> None:
        self.assertIs(self.t.get_waiting_player(), self.t.players[2])

    def test_game_exists(self) -> None:
        self.assertIsInstance(self.t.game, TicTacToeGame)

    def test_game_is_fresh(self) -> None:
        self.assertFalse(self.t.game.game_over)
        self.assertIsNone(self.t.game.winner)

    def test_first_player_idx(self) -> None:
        self.assertEqual(self.t.first_player_idx, 0)


class TestTournamentActivePlayer(unittest.TestCase):

    def setUp(self) -> None:
        self.t = Tournament()

    def test_active_player_starts_as_x_player(self) -> None:
        self.assertIs(self.t.get_active_player(), self.t.players[0])

    def test_active_player_switches_to_o_after_move(self) -> None:
        self.t.game.make_move(0, 0)  # X moves
        self.assertIs(self.t.get_active_player(), self.t.players[1])

    def test_active_player_returns_to_x_after_two_moves(self) -> None:
        self.t.game.make_move(0, 0)
        self.t.game.make_move(1, 1)
        self.assertIs(self.t.get_active_player(), self.t.players[0])


class TestTournamentGetWinnerPlayer(unittest.TestCase):

    def setUp(self) -> None:
        self.t = Tournament()

    def test_no_winner_returns_none(self) -> None:
        self.assertIsNone(self.t.get_winner_player())

    def test_x_winner_returns_x_player(self) -> None:
        _force_x_win(self.t.game)
        self.assertIs(self.t.get_winner_player(), self.t.players[0])

    def test_o_winner_returns_o_player(self) -> None:
        _force_o_win(self.t.game)
        self.assertIs(self.t.get_winner_player(), self.t.players[1])


class TestTournamentRotationOnXWin(unittest.TestCase):
    """When X wins: X stays as X, waiting replaces O, loser (O) sits out."""

    def setUp(self) -> None:
        self.t = Tournament()
        _force_x_win(self.t.game)
        self.t.advance_round()

    def test_winner_stays_as_x(self) -> None:
        """Player 1 (X winner) stays as X."""
        self.assertIs(self.t.get_x_player(), self.t.players[0])

    def test_waiting_becomes_o(self) -> None:
        """Player 3 (was waiting) now plays O."""
        self.assertIs(self.t.get_o_player(), self.t.players[2])

    def test_loser_sits_out(self) -> None:
        """Player 2 (O loser) now waits."""
        self.assertIs(self.t.get_waiting_player(), self.t.players[1])

    def test_winner_score_incremented(self) -> None:
        self.assertEqual(self.t.players[0].wins, 1)

    def test_loser_score_unchanged(self) -> None:
        self.assertEqual(self.t.players[1].wins, 0)

    def test_waiting_score_unchanged(self) -> None:
        self.assertEqual(self.t.players[2].wins, 0)

    def test_board_reset(self) -> None:
        self.assertFalse(self.t.game.game_over)
        self.assertIsNone(self.t.game.winner)

    def test_first_player_idx_updated(self) -> None:
        self.assertEqual(self.t.first_player_idx, self.t.x_player_idx)


class TestTournamentRotationOnOWin(unittest.TestCase):
    """When O wins: O becomes X (goes first), waiting becomes O, loser (X) sits out."""

    def setUp(self) -> None:
        self.t = Tournament()
        _force_o_win(self.t.game)
        self.t.advance_round()

    def test_o_winner_becomes_x(self) -> None:
        """Player 2 (O winner) now plays as X."""
        self.assertIs(self.t.get_x_player(), self.t.players[1])

    def test_waiting_becomes_o(self) -> None:
        """Player 3 (was waiting) now plays O."""
        self.assertIs(self.t.get_o_player(), self.t.players[2])

    def test_loser_sits_out(self) -> None:
        """Player 1 (X loser) now waits."""
        self.assertIs(self.t.get_waiting_player(), self.t.players[0])

    def test_winner_score_incremented(self) -> None:
        self.assertEqual(self.t.players[1].wins, 1)

    def test_loser_score_unchanged(self) -> None:
        self.assertEqual(self.t.players[0].wins, 0)

    def test_board_reset(self) -> None:
        self.assertFalse(self.t.game.game_over)

    def test_first_player_idx_updated(self) -> None:
        self.assertEqual(self.t.first_player_idx, self.t.x_player_idx)


class TestTournamentRotationOnDraw(unittest.TestCase):
    """On draw: first player (X) sits out, O stays (becomes X), waiting becomes O."""

    def setUp(self) -> None:
        self.t = Tournament()
        _force_draw(self.t.game)
        self.t.advance_round()

    def test_o_player_becomes_x(self) -> None:
        """Player 2 (was O) now plays as X."""
        self.assertIs(self.t.get_x_player(), self.t.players[1])

    def test_waiting_becomes_o(self) -> None:
        """Player 3 (was waiting) now plays O."""
        self.assertIs(self.t.get_o_player(), self.t.players[2])

    def test_first_player_sits_out(self) -> None:
        """Player 1 (went first / was X) now waits."""
        self.assertIs(self.t.get_waiting_player(), self.t.players[0])

    def test_no_scores_changed(self) -> None:
        for p in self.t.players:
            self.assertEqual(p.wins, 0)

    def test_board_reset(self) -> None:
        self.assertFalse(self.t.game.game_over)

    def test_first_player_idx_updated(self) -> None:
        self.assertEqual(self.t.first_player_idx, self.t.x_player_idx)


class TestTournamentScoreTracking(unittest.TestCase):
    """Ensure scores accumulate correctly over multiple rounds."""

    def test_two_consecutive_x_wins(self) -> None:
        t = Tournament()
        # Round 1: Player 1 (X) wins
        _force_x_win(t.game)
        t.advance_round()
        self.assertEqual(t.players[0].wins, 1)

        # Round 2: Player 1 is still X, wins again
        _force_x_win(t.game)
        t.advance_round()
        self.assertEqual(t.players[0].wins, 2)

    def test_alternating_winners(self) -> None:
        t = Tournament()
        # Round 1: X (Player 1) wins
        _force_x_win(t.game)
        t.advance_round()
        self.assertEqual(t.players[0].wins, 1)

        # Round 2: O (Player 3, who replaced Player 2) wins
        _force_o_win(t.game)
        t.advance_round()
        self.assertEqual(t.players[2].wins, 1)

    def test_draw_does_not_increment_scores(self) -> None:
        t = Tournament()
        _force_draw(t.game)
        t.advance_round()
        for p in t.players:
            self.assertEqual(p.wins, 0)


class TestTournamentRestartMatch(unittest.TestCase):
    """restart_match resets the board but keeps scores and player arrangement."""

    def setUp(self) -> None:
        self.t = Tournament()
        # Play a round, advance, then play a partial game
        _force_x_win(self.t.game)
        self.t.advance_round()
        # Now: X=Player1, O=Player3, Waiting=Player2, Player1 has 1 win
        self.t.game.make_move(0, 0)
        self.t.game.make_move(1, 1)
        # Restart mid-game
        self.t.restart_match()

    def test_board_is_cleared(self) -> None:
        for r in range(3):
            for c in range(3):
                self.assertIsNone(self.t.game.board[r][c])

    def test_game_not_over(self) -> None:
        self.assertFalse(self.t.game.game_over)

    def test_scores_preserved(self) -> None:
        self.assertEqual(self.t.players[0].wins, 1)

    def test_player_arrangement_preserved(self) -> None:
        self.assertIs(self.t.get_x_player(), self.t.players[0])
        self.assertIs(self.t.get_o_player(), self.t.players[2])
        self.assertIs(self.t.get_waiting_player(), self.t.players[1])

    def test_can_play_after_restart(self) -> None:
        self.assertTrue(self.t.game.make_move(0, 0))


class TestTournamentResetTournament(unittest.TestCase):
    """reset_tournament resets everything to the initial state."""

    def setUp(self) -> None:
        self.t = Tournament()
        _force_x_win(self.t.game)
        self.t.advance_round()
        _force_o_win(self.t.game)
        self.t.advance_round()
        self.t.reset_tournament()

    def test_all_scores_zero(self) -> None:
        for p in self.t.players:
            self.assertEqual(p.wins, 0)

    def test_initial_player_arrangement(self) -> None:
        self.assertEqual(self.t.x_player_idx, 0)
        self.assertEqual(self.t.o_player_idx, 1)
        self.assertEqual(self.t.waiting_idx, 2)

    def test_first_player_idx_reset(self) -> None:
        self.assertEqual(self.t.first_player_idx, 0)

    def test_board_cleared(self) -> None:
        self.assertFalse(self.t.game.game_over)
        self.assertIsNone(self.t.game.winner)
        for r in range(3):
            for c in range(3):
                self.assertIsNone(self.t.game.board[r][c])

    def test_can_play_after_full_reset(self) -> None:
        self.assertTrue(self.t.game.make_move(0, 0))
        self.assertEqual(self.t.game.board[0][0], "X")


class TestTournamentGetStatus(unittest.TestCase):
    """Tests for Tournament.get_status() messages."""

    def setUp(self) -> None:
        self.t = Tournament()

    def test_initial_status_shows_player_1_turn(self) -> None:
        status = self.t.get_status()
        self.assertIn("Player 1", status)
        self.assertIn("X", status)
        self.assertIn("turn", status)

    def test_status_after_one_move(self) -> None:
        self.t.game.make_move(0, 0)
        status = self.t.get_status()
        self.assertIn("Player 2", status)
        self.assertIn("O", status)

    def test_status_on_x_win(self) -> None:
        _force_x_win(self.t.game)
        status = self.t.get_status()
        self.assertIn("Player 1", status)
        self.assertIn("wins", status)

    def test_status_on_o_win(self) -> None:
        _force_o_win(self.t.game)
        status = self.t.get_status()
        self.assertIn("Player 2", status)
        self.assertIn("wins", status)

    def test_status_on_draw(self) -> None:
        _force_draw(self.t.game)
        status = self.t.get_status()
        self.assertEqual(status, "It's a draw!")

    def test_status_includes_player_symbol(self) -> None:
        status = self.t.get_status()
        # Player 1's original symbol is "X"
        self.assertIn("(X)", status)

    def test_status_shows_playing_as(self) -> None:
        """Status for active game should mention what board mark the player uses."""
        status = self.t.get_status()
        self.assertIn("playing as", status)


class TestTournamentMultipleRounds(unittest.TestCase):
    """Test rotation across several rounds to verify correctness."""

    def test_full_rotation_cycle(self) -> None:
        """After 3 games with specific outcomes, verify the full rotation."""
        t = Tournament()

        # Round 1: X (P1) wins. P1 stays X, P3 becomes O, P2 waits.
        _force_x_win(t.game)
        t.advance_round()
        self.assertIs(t.get_x_player(), t.players[0])
        self.assertIs(t.get_o_player(), t.players[2])
        self.assertIs(t.get_waiting_player(), t.players[1])

        # Round 2: O (P3) wins. P3 becomes X, P2 becomes O, P1 waits.
        _force_o_win(t.game)
        t.advance_round()
        self.assertIs(t.get_x_player(), t.players[2])
        self.assertIs(t.get_o_player(), t.players[1])
        self.assertIs(t.get_waiting_player(), t.players[0])

        # Round 3: Draw. First player (P3, X) sits out. P2 becomes X, P1 becomes O.
        _force_draw(t.game)
        t.advance_round()
        self.assertIs(t.get_x_player(), t.players[1])
        self.assertIs(t.get_o_player(), t.players[0])
        self.assertIs(t.get_waiting_player(), t.players[2])

    def test_scores_after_multiple_rounds(self) -> None:
        t = Tournament()

        # Round 1: X=P1, O=P2, Wait=P3. X (P1) wins.
        _force_x_win(t.game)
        t.advance_round()
        # Now: X=P1, O=P3, Wait=P2

        # Round 2: X (P1) wins again.
        _force_x_win(t.game)
        t.advance_round()
        # Now: X=P1, O=P2, Wait=P3

        # Round 3: O (P2) wins.
        _force_o_win(t.game)
        t.advance_round()

        self.assertEqual(t.players[0].wins, 2)  # P1 won rounds 1 & 2
        self.assertEqual(t.players[1].wins, 1)   # P2 won round 3
        self.assertEqual(t.players[2].wins, 0)   # P3 never won

    def test_draw_then_x_win(self) -> None:
        """After a draw rotation, the new X player should be able to win."""
        t = Tournament()
        # Draw: P1 sits out, P2 becomes X, P3 becomes O
        _force_draw(t.game)
        t.advance_round()

        # Now X is Player 2 — X wins
        _force_x_win(t.game)
        t.advance_round()
        self.assertEqual(t.players[1].wins, 1)
        # P2 stays X, P1 replaces P3 as O, P3 waits
        self.assertIs(t.get_x_player(), t.players[1])
        self.assertIs(t.get_o_player(), t.players[0])
        self.assertIs(t.get_waiting_player(), t.players[2])


class TestTournamentEdgeCases(unittest.TestCase):

    def test_reset_tournament_after_no_games(self) -> None:
        """Resetting before any games should be safe."""
        t = Tournament()
        t.reset_tournament()
        self.assertEqual(t.x_player_idx, 0)
        self.assertEqual(t.o_player_idx, 1)
        self.assertEqual(t.waiting_idx, 2)

    def test_restart_match_on_fresh_tournament(self) -> None:
        """Restarting without any moves should be safe."""
        t = Tournament()
        t.restart_match()
        self.assertFalse(t.game.game_over)

    def test_multiple_restarts_in_a_row(self) -> None:
        t = Tournament()
        t.game.make_move(0, 0)
        t.restart_match()
        t.restart_match()
        t.restart_match()
        self.assertFalse(t.game.game_over)
        self.assertIsNone(t.game.winner)

    def test_tournament_instances_are_independent(self) -> None:
        t1 = Tournament()
        t2 = Tournament()
        _force_x_win(t1.game)
        t1.advance_round()
        self.assertEqual(t1.players[0].wins, 1)
        self.assertEqual(t2.players[0].wins, 0)

    def test_advance_round_resets_board(self) -> None:
        """Board should be playable immediately after advance_round."""
        t = Tournament()
        _force_x_win(t.game)
        t.advance_round()
        self.assertTrue(t.game.make_move(0, 0))

    def test_player_indices_always_distinct(self) -> None:
        """After any rotation, x, o, waiting indices must all differ."""
        t = Tournament()
        for _ in range(5):
            _force_x_win(t.game)
            t.advance_round()
            indices = {t.x_player_idx, t.o_player_idx, t.waiting_idx}
            self.assertEqual(len(indices), 3, "Player indices must be distinct")

        for _ in range(5):
            _force_o_win(t.game)
            t.advance_round()
            indices = {t.x_player_idx, t.o_player_idx, t.waiting_idx}
            self.assertEqual(len(indices), 3, "Player indices must be distinct")

        for _ in range(5):
            _force_draw(t.game)
            t.advance_round()
            indices = {t.x_player_idx, t.o_player_idx, t.waiting_idx}
            self.assertEqual(len(indices), 3, "Player indices must be distinct")

    def test_all_indices_in_valid_range(self) -> None:
        """After many rotations, all indices should stay in [0, 1, 2]."""
        t = Tournament()
        for _ in range(10):
            _force_x_win(t.game)
            t.advance_round()
            for idx in [t.x_player_idx, t.o_player_idx, t.waiting_idx]:
                self.assertIn(idx, (0, 1, 2))


# ===========================================================================
# Custom Player Names tests (new)
# ===========================================================================

class TestTournamentCustomNames(unittest.TestCase):
    """Test that Tournament can be created with custom player names."""

    def test_custom_names_stored_correctly(self) -> None:
        """Tournament created with three custom names stores them on the players."""
        t = Tournament(names=["Alice", "Bob", "Charlie"])
        names = [p.name for p in t.players]
        self.assertEqual(names, ["Alice", "Bob", "Charlie"])

    def test_custom_names_preserve_symbols(self) -> None:
        """Custom names should not affect the default symbols."""
        t = Tournament(names=["Alice", "Bob", "Charlie"])
        symbols = [p.symbol for p in t.players]
        self.assertEqual(symbols, ["X", "O", "\u25B3"])

    def test_custom_names_wins_start_at_zero(self) -> None:
        """All players with custom names should start with zero wins."""
        t = Tournament(names=["Alice", "Bob", "Charlie"])
        for p in t.players:
            self.assertEqual(p.wins, 0)

    def test_default_names_when_no_argument(self) -> None:
        """When no player_names argument is given, defaults are used."""
        t = Tournament()
        names = [p.name for p in t.players]
        self.assertEqual(names, ["Player 1", "Player 2", "Player 3"])


class TestTournamentPartialCustomNames(unittest.TestCase):
    """Test Tournament with a mix of custom and default-like names."""

    def test_mixed_custom_and_default_names(self) -> None:
        """Some players have custom names, others keep defaults."""
        t = Tournament(names=["Alice", "Player 2", "Charlie"])
        self.assertEqual(t.players[0].name, "Alice")
        self.assertEqual(t.players[1].name, "Player 2")
        self.assertEqual(t.players[2].name, "Charlie")

    def test_only_first_name_custom(self) -> None:
        """Only the first player has a custom name."""
        t = Tournament(names=["Zara", "Player 2", "Player 3"])
        self.assertEqual(t.players[0].name, "Zara")
        self.assertEqual(t.players[1].name, "Player 2")
        self.assertEqual(t.players[2].name, "Player 3")

    def test_only_last_name_custom(self) -> None:
        """Only the third player has a custom name."""
        t = Tournament(names=["Player 1", "Player 2", "Zeke"])
        self.assertEqual(t.players[0].name, "Player 1")
        self.assertEqual(t.players[1].name, "Player 2")
        self.assertEqual(t.players[2].name, "Zeke")


class TestCustomNamesInGetStatus(unittest.TestCase):
    """Custom names should appear in get_status() output."""

    def test_status_shows_custom_name_on_turn(self) -> None:
        """Active player's custom name should appear in the turn status."""
        t = Tournament(names=["Alice", "Bob", "Charlie"])
        status = t.get_status()
        self.assertIn("Alice", status)
        self.assertNotIn("Player 1", status)

    def test_status_shows_second_player_custom_name(self) -> None:
        """After one move, the second player's custom name should appear."""
        t = Tournament(names=["Alice", "Bob", "Charlie"])
        t.game.make_move(0, 0)
        status = t.get_status()
        self.assertIn("Bob", status)
        self.assertNotIn("Player 2", status)

    def test_status_shows_custom_name_on_win(self) -> None:
        """Winner's custom name appears in the win status."""
        t = Tournament(names=["Alice", "Bob", "Charlie"])
        _force_x_win(t.game)
        status = t.get_status()
        self.assertIn("Alice", status)
        self.assertIn("wins", status)

    def test_status_shows_custom_name_on_o_win(self) -> None:
        """O winner's custom name appears in the win status."""
        t = Tournament(names=["Alice", "Bob", "Charlie"])
        _force_o_win(t.game)
        status = t.get_status()
        self.assertIn("Bob", status)
        self.assertIn("wins", status)

    def test_status_draw_unchanged_with_custom_names(self) -> None:
        """Draw message should not mention player names."""
        t = Tournament(names=["Alice", "Bob", "Charlie"])
        _force_draw(t.game)
        self.assertEqual(t.get_status(), "It's a draw!")


class TestCustomNamesPersistThroughRotation(unittest.TestCase):
    """Custom names should persist through advance_round rotations."""

    def test_names_persist_after_x_win_rotation(self) -> None:
        """After X wins and rotation, all player names remain."""
        t = Tournament(names=["Alice", "Bob", "Charlie"])
        _force_x_win(t.game)
        t.advance_round()
        names = {p.name for p in t.players}
        self.assertEqual(names, {"Alice", "Bob", "Charlie"})

    def test_names_persist_after_o_win_rotation(self) -> None:
        """After O wins and rotation, all player names remain."""
        t = Tournament(names=["Alice", "Bob", "Charlie"])
        _force_o_win(t.game)
        t.advance_round()
        names = {p.name for p in t.players}
        self.assertEqual(names, {"Alice", "Bob", "Charlie"})

    def test_names_persist_after_draw_rotation(self) -> None:
        """After draw and rotation, all player names remain."""
        t = Tournament(names=["Alice", "Bob", "Charlie"])
        _force_draw(t.game)
        t.advance_round()
        names = {p.name for p in t.players}
        self.assertEqual(names, {"Alice", "Bob", "Charlie"})

    def test_correct_custom_name_after_x_win_rotation(self) -> None:
        """After X wins, the winner (Alice) stays as X, status shows Alice."""
        t = Tournament(names=["Alice", "Bob", "Charlie"])
        _force_x_win(t.game)
        t.advance_round()
        # Alice (X winner) stays as X
        self.assertEqual(t.get_x_player().name, "Alice")
        # Charlie (was waiting) becomes O
        self.assertEqual(t.get_o_player().name, "Charlie")
        # Bob (loser) waits
        self.assertEqual(t.get_waiting_player().name, "Bob")

    def test_correct_custom_name_after_o_win_rotation(self) -> None:
        """After O wins, Bob becomes X, Charlie becomes O, Alice waits."""
        t = Tournament(names=["Alice", "Bob", "Charlie"])
        _force_o_win(t.game)
        t.advance_round()
        self.assertEqual(t.get_x_player().name, "Bob")
        self.assertEqual(t.get_o_player().name, "Charlie")
        self.assertEqual(t.get_waiting_player().name, "Alice")

    def test_custom_names_persist_through_multiple_rotations(self) -> None:
        """Names stay correct through 5 rounds of play."""
        t = Tournament(names=["Alice", "Bob", "Charlie"])
        for _ in range(5):
            _force_x_win(t.game)
            t.advance_round()
        names = {p.name for p in t.players}
        self.assertEqual(names, {"Alice", "Bob", "Charlie"})

    def test_status_uses_custom_name_after_rotation(self) -> None:
        """After rotation, get_status uses the rotated player's custom name."""
        t = Tournament(names=["Alice", "Bob", "Charlie"])
        _force_o_win(t.game)
        t.advance_round()
        # Bob is now X player
        status = t.get_status()
        self.assertIn("Bob", status)


class TestCustomNamesPersistThroughResets(unittest.TestCase):
    """Custom names should persist through restart_match and reset_tournament."""

    def test_names_persist_after_restart_match(self) -> None:
        """restart_match should not affect player names."""
        t = Tournament(names=["Alice", "Bob", "Charlie"])
        t.game.make_move(0, 0)
        t.restart_match()
        names = [p.name for p in t.players]
        self.assertEqual(names, ["Alice", "Bob", "Charlie"])

    def test_names_persist_after_reset_tournament(self) -> None:
        """reset_tournament should not affect player names."""
        t = Tournament(names=["Alice", "Bob", "Charlie"])
        _force_x_win(t.game)
        t.advance_round()
        t.reset_tournament()
        names = [p.name for p in t.players]
        self.assertEqual(names, ["Alice", "Bob", "Charlie"])

    def test_scores_reset_but_names_kept_after_reset_tournament(self) -> None:
        """Scores go to zero but names remain after reset_tournament."""
        t = Tournament(names=["Alice", "Bob", "Charlie"])
        _force_x_win(t.game)
        t.advance_round()
        t.reset_tournament()
        for p in t.players:
            self.assertEqual(p.wins, 0)
        self.assertEqual(t.players[0].name, "Alice")
        self.assertEqual(t.players[1].name, "Bob")
        self.assertEqual(t.players[2].name, "Charlie")

    def test_arrangement_reset_but_names_kept(self) -> None:
        """Player arrangement resets but names stay after reset_tournament."""
        t = Tournament(names=["Alice", "Bob", "Charlie"])
        _force_o_win(t.game)
        t.advance_round()
        t.reset_tournament()
        self.assertEqual(t.get_x_player().name, "Alice")
        self.assertEqual(t.get_o_player().name, "Bob")
        self.assertEqual(t.get_waiting_player().name, "Charlie")

    def test_multiple_restart_match_preserves_names(self) -> None:
        """Multiple restart_match calls do not lose custom names."""
        t = Tournament(names=["Alice", "Bob", "Charlie"])
        for _ in range(5):
            t.game.make_move(0, 0)
            t.restart_match()
        names = [p.name for p in t.players]
        self.assertEqual(names, ["Alice", "Bob", "Charlie"])


class TestCustomNamesEdgeCases(unittest.TestCase):
    """Edge cases for custom player names."""

    def test_empty_string_names(self) -> None:
        """Empty string names should be accepted and stored."""
        t = Tournament(names=["", "", ""])
        for p in t.players:
            self.assertEqual(p.name, "")

    def test_very_long_names(self) -> None:
        """Very long names should be accepted and stored."""
        long_name = "A" * 1000
        t = Tournament(names=[long_name, "Bob", "Charlie"])
        self.assertEqual(t.players[0].name, long_name)
        self.assertEqual(len(t.players[0].name), 1000)

    def test_special_characters_in_names(self) -> None:
        """Names with special characters should be accepted."""
        t = Tournament(names=["O'Brien", "Dr. No", "Player #3!"])
        self.assertEqual(t.players[0].name, "O'Brien")
        self.assertEqual(t.players[1].name, "Dr. No")
        self.assertEqual(t.players[2].name, "Player #3!")

    def test_unicode_names(self) -> None:
        """Unicode names should be accepted and stored."""
        t = Tournament(names=["\u00C9milie", "\u5F35\u4E09", "\u041F\u0435\u0442\u0440"])
        self.assertEqual(t.players[0].name, "\u00C9milie")
        self.assertEqual(t.players[1].name, "\u5F35\u4E09")
        self.assertEqual(t.players[2].name, "\u041F\u0435\u0442\u0440")

    def test_whitespace_only_names(self) -> None:
        """Whitespace-only names should be accepted (no validation required)."""
        t = Tournament(names=["   ", "\t", "\n"])
        self.assertEqual(t.players[0].name, "   ")
        self.assertEqual(t.players[1].name, "\t")
        self.assertEqual(t.players[2].name, "\n")

    def test_duplicate_names_allowed(self) -> None:
        """Duplicate names should be accepted (players are distinguished by symbol)."""
        t = Tournament(names=["Sam", "Sam", "Sam"])
        for p in t.players:
            self.assertEqual(p.name, "Sam")
        # Symbols should still be distinct
        symbols = [p.symbol for p in t.players]
        self.assertEqual(len(set(symbols)), 3)

    def test_names_with_parentheses(self) -> None:
        """Names containing parentheses should work in get_status()."""
        t = Tournament(names=["Player (1)", "Player (2)", "Player (3)"])
        status = t.get_status()
        self.assertIn("Player (1)", status)

    def test_special_chars_in_status_on_win(self) -> None:
        """Names with special chars should display correctly in win status."""
        t = Tournament(names=["O'Brien", "Dr. No", "Player #3!"])
        _force_x_win(t.game)
        status = t.get_status()
        self.assertIn("O'Brien", status)
        self.assertIn("wins", status)


# ===========================================================================
# Win Target tests (new)
# ===========================================================================

class TestWinTargetDefault(unittest.TestCase):
    """Test that win_target defaults to 3."""

    def test_default_win_target_is_3(self) -> None:
        """Tournament with no win_target argument should default to 3."""
        t = Tournament()
        self.assertEqual(t.win_target, 3)

    def test_default_win_target_with_custom_names(self) -> None:
        """Tournament with custom names but no win_target should default to 3."""
        t = Tournament(names=["Alice", "Bob", "Charlie"])
        self.assertEqual(t.win_target, 3)


class TestWinTargetCustomValues(unittest.TestCase):
    """Test that custom win_target values are stored correctly."""

    def test_win_target_of_1(self) -> None:
        t = Tournament(win_target=1)
        self.assertEqual(t.win_target, 1)

    def test_win_target_of_5(self) -> None:
        t = Tournament(win_target=5)
        self.assertEqual(t.win_target, 5)

    def test_win_target_of_10(self) -> None:
        t = Tournament(win_target=10)
        self.assertEqual(t.win_target, 10)

    def test_win_target_with_names_and_target(self) -> None:
        """Both custom names and custom win_target should work together."""
        t = Tournament(names=["Alice", "Bob", "Charlie"], win_target=7)
        self.assertEqual(t.win_target, 7)
        self.assertEqual(t.players[0].name, "Alice")


class TestGetTournamentWinnerNone(unittest.TestCase):
    """Test get_tournament_winner returns None when no one has reached the target."""

    def test_no_winner_at_start(self) -> None:
        """Fresh tournament should have no tournament winner."""
        t = Tournament()
        self.assertIsNone(t.get_tournament_winner())

    def test_no_winner_after_one_win(self) -> None:
        """With default target of 3, one win is not enough."""
        t = Tournament()
        _force_x_win(t.game)
        t.advance_round()
        self.assertIsNone(t.get_tournament_winner())

    def test_no_winner_after_two_wins(self) -> None:
        """With default target of 3, two wins is not enough."""
        t = Tournament()
        _force_x_win(t.game)
        t.advance_round()
        _force_x_win(t.game)
        t.advance_round()
        self.assertEqual(t.players[0].wins, 2)
        self.assertIsNone(t.get_tournament_winner())

    def test_no_winner_with_draws_only(self) -> None:
        """Draws never produce a tournament winner."""
        t = Tournament()
        for _ in range(5):
            _force_draw(t.game)
            t.advance_round()
        self.assertIsNone(t.get_tournament_winner())


class TestGetTournamentWinnerCorrectPlayer(unittest.TestCase):
    """Test get_tournament_winner returns the correct player at win_target."""

    def test_player_reaches_default_target_of_3(self) -> None:
        """Player 1 wins 3 games and becomes tournament winner."""
        t = Tournament()
        for _ in range(3):
            _force_x_win(t.game)
            t.advance_round()
        self.assertEqual(t.players[0].wins, 3)
        winner = t.get_tournament_winner()
        self.assertIsNotNone(winner)
        self.assertIs(winner, t.players[0])

    def test_o_player_reaches_target(self) -> None:
        """Player 2 (O) wins enough games to reach the target."""
        t = Tournament(win_target=2)
        # Round 1: O (Player 2) wins
        _force_o_win(t.game)
        t.advance_round()
        self.assertIsNone(t.get_tournament_winner())
        # Round 2: Player 2 is now X, wins again
        _force_x_win(t.game)
        t.advance_round()
        self.assertEqual(t.players[1].wins, 2)
        winner = t.get_tournament_winner()
        self.assertIsNotNone(winner)
        self.assertIs(winner, t.players[1])

    def test_winner_name_matches(self) -> None:
        """Tournament winner should have the expected name."""
        t = Tournament(names=["Alice", "Bob", "Charlie"], win_target=1)
        _force_x_win(t.game)
        t.advance_round()
        winner = t.get_tournament_winner()
        self.assertIsNotNone(winner)
        self.assertEqual(winner.name, "Alice")


class TestTournamentWinnerExactlyAtTarget(unittest.TestCase):
    """Test tournament winner after exactly win_target wins."""

    def test_exactly_at_target_1(self) -> None:
        t = Tournament(win_target=1)
        _force_x_win(t.game)
        t.advance_round()
        self.assertEqual(t.players[0].wins, 1)
        self.assertIsNotNone(t.get_tournament_winner())

    def test_exactly_at_target_3(self) -> None:
        t = Tournament(win_target=3)
        for _ in range(3):
            _force_x_win(t.game)
            t.advance_round()
        self.assertEqual(t.players[0].wins, 3)
        self.assertIsNotNone(t.get_tournament_winner())

    def test_exactly_at_target_5(self) -> None:
        t = Tournament(win_target=5)
        for _ in range(5):
            _force_x_win(t.game)
            t.advance_round()
        self.assertEqual(t.players[0].wins, 5)
        self.assertIsNotNone(t.get_tournament_winner())

    def test_no_winner_one_below_target(self) -> None:
        """With target=3, after 2 wins there should be no tournament winner."""
        t = Tournament(win_target=3)
        for _ in range(2):
            _force_x_win(t.game)
            t.advance_round()
        self.assertEqual(t.players[0].wins, 2)
        self.assertIsNone(t.get_tournament_winner())


class TestWinTargetPersistsThroughRestartMatch(unittest.TestCase):
    """Win target should not change when restart_match is called."""

    def test_win_target_unchanged_after_restart(self) -> None:
        t = Tournament(win_target=7)
        t.game.make_move(0, 0)
        t.restart_match()
        self.assertEqual(t.win_target, 7)

    def test_win_target_unchanged_after_multiple_restarts(self) -> None:
        t = Tournament(win_target=5)
        for _ in range(3):
            t.game.make_move(0, 0)
            t.restart_match()
        self.assertEqual(t.win_target, 5)

    def test_tournament_winner_still_works_after_restart(self) -> None:
        """Win accumulation and target checking should work across restarts."""
        t = Tournament(win_target=2)
        _force_x_win(t.game)
        t.advance_round()
        t.restart_match()  # restart mid-game
        _force_x_win(t.game)
        t.advance_round()
        self.assertIsNotNone(t.get_tournament_winner())


class TestWinTargetPersistsThroughResetTournament(unittest.TestCase):
    """Win target should not change when reset_tournament is called."""

    def test_win_target_unchanged_after_reset(self) -> None:
        t = Tournament(win_target=7)
        _force_x_win(t.game)
        t.advance_round()
        t.reset_tournament()
        self.assertEqual(t.win_target, 7)

    def test_tournament_winner_none_after_reset(self) -> None:
        """After reset_tournament, no one should be tournament winner (scores are 0)."""
        t = Tournament(win_target=2)
        _force_x_win(t.game)
        t.advance_round()
        _force_x_win(t.game)
        t.advance_round()
        self.assertIsNotNone(t.get_tournament_winner())
        t.reset_tournament()
        self.assertIsNone(t.get_tournament_winner())

    def test_can_reach_target_again_after_reset(self) -> None:
        """After reset, a player can win enough games to reach win_target again."""
        t = Tournament(win_target=1)
        _force_x_win(t.game)
        t.advance_round()
        self.assertIsNotNone(t.get_tournament_winner())
        t.reset_tournament()
        self.assertIsNone(t.get_tournament_winner())
        _force_x_win(t.game)
        t.advance_round()
        self.assertIsNotNone(t.get_tournament_winner())


class TestWinTargetOfOne(unittest.TestCase):
    """Win target of 1 means the tournament is won after the first win."""

    def test_x_wins_first_game_wins_tournament(self) -> None:
        t = Tournament(win_target=1)
        _force_x_win(t.game)
        t.advance_round()
        winner = t.get_tournament_winner()
        self.assertIsNotNone(winner)
        self.assertIs(winner, t.players[0])

    def test_o_wins_first_game_wins_tournament(self) -> None:
        t = Tournament(win_target=1)
        _force_o_win(t.game)
        t.advance_round()
        winner = t.get_tournament_winner()
        self.assertIsNotNone(winner)
        self.assertIs(winner, t.players[1])

    def test_draw_first_then_win_tournament(self) -> None:
        """A draw does not win; the first actual win should win the tournament."""
        t = Tournament(win_target=1)
        _force_draw(t.game)
        t.advance_round()
        self.assertIsNone(t.get_tournament_winner())
        _force_x_win(t.game)
        t.advance_round()
        self.assertIsNotNone(t.get_tournament_winner())


class TestMultiplePlayersCloseToTarget(unittest.TestCase):
    """Only the player who reaches the target should be the tournament winner."""

    def test_one_player_ahead_others_behind(self) -> None:
        """With target=3, one player at 2 wins and another at 1 — no winner yet."""
        t = Tournament(win_target=3)
        # Player 1 wins twice as X
        _force_x_win(t.game)
        t.advance_round()
        _force_x_win(t.game)
        t.advance_round()
        self.assertEqual(t.players[0].wins, 2)
        # Now O wins (a different player)
        _force_o_win(t.game)
        t.advance_round()
        # Player 0 still at 2, another player at 1
        self.assertIsNone(t.get_tournament_winner())

    def test_first_to_reach_target_wins(self) -> None:
        """The first player to reach win_target is the tournament winner."""
        t = Tournament(win_target=2)
        # Round 1: X (Player 1) wins -> P1: 1 win
        _force_x_win(t.game)
        t.advance_round()
        # Round 2: O wins (Player 3 now O) -> some other player gets 1 win
        _force_o_win(t.game)
        t.advance_round()
        # At this point P1=1, P3=1
        self.assertIsNone(t.get_tournament_winner())
        # Now let the current X player win to reach 2
        current_x_player = t.players[t.x_player_idx]
        _force_x_win(t.game)
        t.advance_round()
        winner = t.get_tournament_winner()
        self.assertIsNotNone(winner)
        self.assertEqual(winner.wins, 2)

    def test_two_players_at_target_minus_one(self) -> None:
        """Two players both at target-1, then one wins — only that one is winner."""
        t = Tournament(win_target=2)
        # P1 wins round 1
        _force_x_win(t.game)
        t.advance_round()  # P1=1
        # O wins round 2 (Player 3 is now O after X win rotation)
        _force_o_win(t.game)
        t.advance_round()  # P1=1, P3=1 (was Player 3 who became O)
        # Find which player has 1 win besides P1
        self.assertEqual(t.players[0].wins, 1)
        # Now let P1 win again to reach target
        # We need P1 to be X. Let's check and play accordingly.
        # Force whoever is X to win
        _force_x_win(t.game)
        t.advance_round()
        winner = t.get_tournament_winner()
        self.assertIsNotNone(winner)
        self.assertGreaterEqual(winner.wins, 2)


class TestWinTargetWithCustomNames(unittest.TestCase):
    """Win target should work correctly with custom player names."""

    def test_custom_names_and_win_target(self) -> None:
        t = Tournament(names=["Alice", "Bob", "Charlie"], win_target=2)
        self.assertEqual(t.win_target, 2)
        self.assertEqual(t.players[0].name, "Alice")

    def test_tournament_winner_has_custom_name(self) -> None:
        t = Tournament(names=["Alice", "Bob", "Charlie"], win_target=1)
        _force_x_win(t.game)
        t.advance_round()
        winner = t.get_tournament_winner()
        self.assertIsNotNone(winner)
        self.assertEqual(winner.name, "Alice")

    def test_unicode_names_with_win_target(self) -> None:
        t = Tournament(names=["\u00C9milie", "\u5F35\u4E09", "\u041F\u0435\u0442\u0440"], win_target=1)
        _force_x_win(t.game)
        t.advance_round()
        winner = t.get_tournament_winner()
        self.assertIsNotNone(winner)
        self.assertEqual(winner.name, "\u00C9milie")

    def test_special_char_names_with_win_target(self) -> None:
        t = Tournament(names=["O'Brien", "Dr. No", "Player #3!"], win_target=2)
        _force_x_win(t.game)
        t.advance_round()
        _force_x_win(t.game)
        t.advance_round()
        winner = t.get_tournament_winner()
        self.assertIsNotNone(winner)
        self.assertEqual(winner.name, "O'Brien")


# ===========================================================================
# WinningLine tests
# ===========================================================================

class TestWinningLine(unittest.TestCase):
    """Tests for the winning_line attribute on TicTacToeGame."""

    def setUp(self) -> None:
        self.game = TicTacToeGame()

    # -- initial / mid-game / draw: winning_line is None --

    def test_winning_line_is_none_initially(self) -> None:
        """winning_line should be None on a fresh game."""
        self.assertIsNone(self.game.winning_line)

    def test_winning_line_is_none_during_gameplay(self) -> None:
        """winning_line should remain None while the game is in progress."""
        self.game.make_move(0, 0)  # X
        self.assertIsNone(self.game.winning_line)
        self.game.make_move(1, 1)  # O
        self.assertIsNone(self.game.winning_line)

    def test_winning_line_is_none_on_draw(self) -> None:
        """winning_line should be None when the game ends in a draw."""
        _force_draw(self.game)
        self.assertTrue(self.game.game_over)
        self.assertIsNone(self.game.winner)
        self.assertIsNone(self.game.winning_line)

    # -- X wins via row 0 --

    def test_x_wins_row_0(self) -> None:
        """X wins top row; winning_line should be [(0,0), (0,1), (0,2)]."""
        # X(0,0), O(1,0), X(0,1), O(1,1), X(0,2)
        _force_x_win(self.game)
        self.assertEqual(self.game.winner, "X")
        self.assertEqual(self.game.winning_line, [(0, 0), (0, 1), (0, 2)])

    # -- O wins via column 1 --

    def test_o_wins_col_1(self) -> None:
        """O wins column 1; winning_line should be [(0,1), (1,1), (2,1)]."""
        # X(0,0), O(0,1), X(2,0), O(1,1), X(2,2), O(2,1)
        _play_moves(self.game, [(0, 0), (0, 1), (2, 0), (1, 1), (2, 2), (2, 1)])
        self.assertEqual(self.game.winner, "O")
        self.assertEqual(self.game.winning_line, [(0, 1), (1, 1), (2, 1)])

    # -- X wins via main diagonal --

    def test_x_wins_diagonal(self) -> None:
        """X wins main diagonal; winning_line should be [(0,0), (1,1), (2,2)]."""
        # X(0,0), O(0,1), X(1,1), O(0,2), X(2,2)
        _play_moves(self.game, [(0, 0), (0, 1), (1, 1), (0, 2), (2, 2)])
        self.assertEqual(self.game.winner, "X")
        self.assertEqual(self.game.winning_line, [(0, 0), (1, 1), (2, 2)])

    # -- X wins via anti-diagonal --

    def test_x_wins_anti_diagonal(self) -> None:
        """X wins anti-diagonal; winning_line should be [(0,2), (1,1), (2,0)]."""
        # X(0,2), O(0,0), X(1,1), O(1,0), X(2,0)
        _play_moves(self.game, [(0, 2), (0, 0), (1, 1), (1, 0), (2, 0)])
        self.assertEqual(self.game.winner, "X")
        self.assertEqual(self.game.winning_line, [(0, 2), (1, 1), (2, 0)])

    # -- reset clears winning_line --

    def test_winning_line_resets_to_none(self) -> None:
        """After a win, reset() should clear winning_line back to None."""
        _force_x_win(self.game)
        self.assertIsNotNone(self.game.winning_line)
        self.game.reset()
        self.assertIsNone(self.game.winning_line)

    # -- winning_line matches WINNING_LINES constant --

    def test_winning_line_matches_winning_lines_constant(self) -> None:
        """The returned winning_line should be one of the entries in WINNING_LINES."""
        _force_x_win(self.game)
        self.assertIn(self.game.winning_line, WINNING_LINES)

    def test_each_winning_line_entry_is_reachable(self) -> None:
        """Verify that every entry in WINNING_LINES can appear as winning_line."""
        # Build move sequences that win along each of the 8 lines.
        # Each sequence: X plays the 3 cells of the line, O fills non-conflicting cells.
        win_sequences = {
            # Rows
            0: [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)],          # row 0
            1: [(1, 0), (0, 0), (1, 1), (0, 1), (1, 2)],          # row 1
            2: [(2, 0), (0, 0), (2, 1), (0, 1), (2, 2)],          # row 2
            # Columns
            3: [(0, 0), (0, 1), (1, 0), (0, 2), (2, 0)],          # col 0
            4: [(0, 1), (0, 0), (1, 1), (1, 0), (2, 1)],          # col 1
            5: [(0, 2), (0, 0), (1, 2), (1, 0), (2, 2)],          # col 2
            # Diagonals
            6: [(0, 0), (0, 1), (1, 1), (0, 2), (2, 2)],          # main diag
            7: [(0, 2), (0, 0), (1, 1), (1, 0), (2, 0)],          # anti diag
        }
        for idx, moves in win_sequences.items():
            with self.subTest(winning_line_index=idx):
                game = TicTacToeGame()
                _play_moves(game, moves)
                self.assertEqual(game.winner, "X")
                self.assertEqual(game.winning_line, WINNING_LINES[idx])


# ===========================================================================
# N-player Tournament tests
# ===========================================================================

class TestTournamentValidation(unittest.TestCase):
    """Tests for player count validation."""

    def test_zero_players_raises(self) -> None:
        with self.assertRaises(ValueError):
            Tournament(names=[])

    def test_one_player_raises(self) -> None:
        with self.assertRaises(ValueError):
            Tournament(names=["Solo"])

    def test_six_players_raises(self) -> None:
        with self.assertRaises(ValueError):
            Tournament(names=["A", "B", "C", "D", "E", "F"])

    def test_two_players_ok(self) -> None:
        t = Tournament(names=["A", "B"])
        self.assertEqual(len(t.players), 2)

    def test_five_players_ok(self) -> None:
        t = Tournament(names=["A", "B", "C", "D", "E"])
        self.assertEqual(len(t.players), 5)


class TestTournament2Players(unittest.TestCase):
    """Tests for 2-player tournament (no waiting queue)."""

    def setUp(self) -> None:
        self.t = Tournament(names=["Alice", "Bob"])

    def test_initial_setup(self) -> None:
        self.assertEqual(self.t.x_player_idx, 0)
        self.assertEqual(self.t.o_player_idx, 1)
        self.assertEqual(self.t.waiting_queue, [])

    def test_symbols(self) -> None:
        self.assertEqual(self.t.players[0].symbol, "X")
        self.assertEqual(self.t.players[1].symbol, "O")

    def test_x_wins_stays_x(self) -> None:
        _force_x_win(self.t.game)
        self.t.advance_round()
        self.assertEqual(self.t.players[0].wins, 1)
        self.assertEqual(self.t.x_player_idx, 0)
        self.assertEqual(self.t.o_player_idx, 1)

    def test_o_wins_becomes_x(self) -> None:
        _force_o_win(self.t.game)
        self.t.advance_round()
        self.assertEqual(self.t.players[1].wins, 1)
        self.assertEqual(self.t.x_player_idx, 1)
        self.assertEqual(self.t.o_player_idx, 0)

    def test_draw_swaps(self) -> None:
        _force_draw(self.t.game)
        self.t.advance_round()
        self.assertEqual(self.t.x_player_idx, 1)
        self.assertEqual(self.t.o_player_idx, 0)

    def test_reset_tournament(self) -> None:
        _force_x_win(self.t.game)
        self.t.advance_round()
        self.t.reset_tournament()
        self.assertEqual(self.t.x_player_idx, 0)
        self.assertEqual(self.t.o_player_idx, 1)
        self.assertEqual(self.t.waiting_queue, [])
        self.assertEqual(self.t.players[0].wins, 0)


class TestTournament4Players(unittest.TestCase):
    """Tests for 4-player tournament."""

    def setUp(self) -> None:
        self.t = Tournament(names=["A", "B", "C", "D"])

    def test_initial_queue(self) -> None:
        self.assertEqual(self.t.waiting_queue, [2, 3])

    def test_symbols(self) -> None:
        symbols = [p.symbol for p in self.t.players]
        self.assertEqual(symbols, ["X", "O", "\u25B3", "\u25CF"])

    def test_x_wins_rotation(self) -> None:
        """X wins: loser goes to back of queue, next in queue becomes O."""
        _force_x_win(self.t.game)
        self.t.advance_round()
        self.assertEqual(self.t.x_player_idx, 0)  # winner stays
        self.assertEqual(self.t.o_player_idx, 2)   # from queue
        self.assertEqual(self.t.waiting_queue, [3, 1])  # loser at back

    def test_o_wins_rotation(self) -> None:
        """O wins: loser goes to back of queue, winner becomes X."""
        _force_o_win(self.t.game)
        self.t.advance_round()
        self.assertEqual(self.t.x_player_idx, 1)  # winner
        self.assertEqual(self.t.o_player_idx, 2)   # from queue
        self.assertEqual(self.t.waiting_queue, [3, 0])  # loser at back

    def test_queue_order_after_multiple_rounds(self) -> None:
        """Verify FIFO queue order through multiple X wins."""
        # Round 1: X(0) wins, loser(1) -> back, queue was [2,3] -> O=2, queue=[3,1]
        _force_x_win(self.t.game)
        self.t.advance_round()
        self.assertEqual(self.t.waiting_queue, [3, 1])

        # Round 2: X(0) wins again, loser(2) -> back, queue was [3,1] -> O=3, queue=[1,2]
        _force_x_win(self.t.game)
        self.t.advance_round()
        self.assertEqual(self.t.waiting_queue, [1, 2])

    def test_get_waiting_players(self) -> None:
        waiting = self.t.get_waiting_players()
        self.assertEqual(len(waiting), 2)
        self.assertEqual(waiting[0].name, "C")
        self.assertEqual(waiting[1].name, "D")

    def test_reset_tournament(self) -> None:
        _force_x_win(self.t.game)
        self.t.advance_round()
        self.t.reset_tournament()
        self.assertEqual(self.t.waiting_queue, [2, 3])
        self.assertEqual(self.t.x_player_idx, 0)
        self.assertEqual(self.t.o_player_idx, 1)


class TestTournament5Players(unittest.TestCase):
    """Tests for 5-player tournament."""

    def setUp(self) -> None:
        self.t = Tournament(names=["A", "B", "C", "D", "E"])

    def test_initial_queue(self) -> None:
        self.assertEqual(self.t.waiting_queue, [2, 3, 4])

    def test_symbols(self) -> None:
        symbols = [p.symbol for p in self.t.players]
        self.assertEqual(symbols, ["X", "O", "\u25B3", "\u25CF", "\u25A0"])

    def test_full_rotation_x_wins(self) -> None:
        """If X keeps winning, every other player should cycle through O position."""
        seen_as_o = []
        for _ in range(4):
            seen_as_o.append(self.t.o_player_idx)
            _force_x_win(self.t.game)
            self.t.advance_round()
        # Player 0 always X, everyone else should have been O
        self.assertEqual(sorted(seen_as_o), [1, 2, 3, 4])

    def test_draw_rotation(self) -> None:
        """Draw: first player goes to back of queue."""
        _force_draw(self.t.game)
        self.t.advance_round()
        self.assertEqual(self.t.x_player_idx, 1)   # stayed
        self.assertEqual(self.t.o_player_idx, 2)    # from queue
        self.assertEqual(self.t.waiting_queue, [3, 4, 0])  # first went to back

    def test_get_waiting_players(self) -> None:
        waiting = self.t.get_waiting_players()
        self.assertEqual(len(waiting), 3)
        names = [p.name for p in waiting]
        self.assertEqual(names, ["C", "D", "E"])


if __name__ == "__main__":
    unittest.main()

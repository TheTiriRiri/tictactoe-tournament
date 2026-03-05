"""Tests for player registration and login."""

import unittest

from src.auth import AuthManager


class TestRegister(unittest.TestCase):
    """Tests for user registration."""

    def setUp(self) -> None:
        self.auth = AuthManager(db_path=":memory:")

    def tearDown(self) -> None:
        self.auth.close()

    def test_register_success(self) -> None:
        ok, msg = self.auth.register("alice", "pass123")
        self.assertTrue(ok)
        self.assertEqual(msg, "Registration successful")

    def test_register_duplicate(self) -> None:
        self.auth.register("alice", "pass123")
        ok, msg = self.auth.register("alice", "other")
        self.assertFalse(ok)
        self.assertEqual(msg, "Username already exists")

    def test_register_empty_username(self) -> None:
        ok, msg = self.auth.register("", "pass123")
        self.assertFalse(ok)
        self.assertIn("empty", msg.lower())

    def test_register_whitespace_username(self) -> None:
        ok, msg = self.auth.register("   ", "pass123")
        self.assertFalse(ok)
        self.assertIn("empty", msg.lower())

    def test_register_empty_password(self) -> None:
        ok, msg = self.auth.register("alice", "")
        self.assertFalse(ok)
        self.assertIn("empty", msg.lower())

    def test_salt_uniqueness(self) -> None:
        """Two users with the same password should have different salts."""
        self.auth.register("alice", "same_pass")
        self.auth.register("bob", "same_pass")
        rows = self.auth._conn.execute(
            "SELECT salt FROM users ORDER BY username"
        ).fetchall()
        self.assertNotEqual(rows[0][0], rows[1][0])


class TestLogin(unittest.TestCase):
    """Tests for user login."""

    def setUp(self) -> None:
        self.auth = AuthManager(db_path=":memory:")
        self.auth.register("alice", "pass123")

    def tearDown(self) -> None:
        self.auth.close()

    def test_login_success(self) -> None:
        ok, msg = self.auth.login("alice", "pass123")
        self.assertTrue(ok)
        self.assertEqual(msg, "Login successful")

    def test_login_wrong_password(self) -> None:
        ok, msg = self.auth.login("alice", "wrong")
        self.assertFalse(ok)
        self.assertEqual(msg, "Wrong password")

    def test_login_nonexistent_user(self) -> None:
        ok, msg = self.auth.login("nobody", "pass123")
        self.assertFalse(ok)
        self.assertEqual(msg, "User not found")

    def test_login_empty_username(self) -> None:
        ok, msg = self.auth.login("", "pass123")
        self.assertFalse(ok)

    def test_login_empty_password(self) -> None:
        ok, msg = self.auth.login("alice", "")
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()

import unittest

from pyjarowinkler.comparative import Comparative

__author__ = "Jean-Bernard Ratte - jean.bernard.ratte@unary.ca"


class TestComparative(unittest.TestCase):
    def test_sanitize_exception(self) -> None:
        with self.assertRaises(ValueError):
            Comparative(None, None)  # type: ignore

    def test_sanitize_exception_args(self) -> None:
        with self.assertRaises(ValueError):
            Comparative("4", 333)  # type: ignore

    def test_sanitize_spaces(self) -> None:
        comparative: Comparative = Comparative("   asdf ", "asdf     ")
        self.assertEqual([comparative.first, comparative.second], ["asdf", "asdf"])

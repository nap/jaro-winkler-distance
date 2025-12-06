"""Utilities for preparing and sanitizing string pairs for Jaro-Winkler distance calculations."""

from typing import Final
from unicodedata import normalize

from .glyph import AMBIGUOUS


class Comparative(object):
    """
    Helper container that sanitizes and stores two strings prepared for Jaro-Winkler calculations. See [ruff/rules/confusables](https://github.com/astral-sh/ruff/blob/69ace002102c7201f4514ffad87b87ce6a0d604f/crates/ruff_linter/src/rules/ruff/rules/confusables.rs#L5).

    Attributes:
        first (str): Sanitized first string (shortest) after normalization.
        second (str): Sanitized second string (longest) after normalization.

    """

    __ASCII_MAX__: Final[int] = 0x80

    def __init__(self, first: str, second: str, norm_case: bool = False, norm_utf8: bool = True, norm_ambiguous: bool = True):
        """
        Initialize Comparative with two input strings, optionally casefolding them if norm_case is True.

        Args:
            first (str): Original first input string.
            second (str): Original second input string.
            norm_case (bool, optional): If True, both strings are
                converted with casefold for case-insensitive comparison.
            norm_utf8 (bool, optional): If True, both strings are
                normalized from C (NFC).
            norm_ambiguous (bool, optional): Normalize ambiguous glyph.

        """
        self.first: str = self._sanitize(first, norm_case=norm_case, norm_utf8=norm_utf8, norm_ambiguous=norm_ambiguous)
        self.second: str = self._sanitize(second, norm_case=norm_case, norm_utf8=norm_utf8, norm_ambiguous=norm_ambiguous)

        if len(self.first) > len(self.second):
            self.first, self.second = self.second, self.first

    def _sanitize(self, word: str, norm_case: bool = False, norm_utf8: bool = True, norm_ambiguous: bool = False) -> str:
        """
        Sanitize input string.

        Args:
            word (str): Input string to sanitize.
            norm_case (bool, optional): If True, string is converted with casefold.
            norm_utf8 (bool, optional): If True, string is normalized using NFC form.
            norm_ambiguous (bool, optional): Normalize ambiguous glyphs.

        Returns:
            str: Sanitized string.

        """
        if not isinstance(word, str):
            raise ValueError("Argument must be a string.")

        word = word.strip()

        if norm_utf8:
            word = normalize("NFC", word)

        if norm_ambiguous:
            word = word.translate(AMBIGUOUS)

        if norm_case:
            word = word.casefold()

        return word

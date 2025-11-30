"""Utilities for preparing and sanitizing string pairs for Jaro-Winkler distance calculations."""

import unicodedata


class Comparative(object):
    """
    Helper container that sanitizes and stores two strings prepared for Jaro-Winkler calculations. See [ruff/rules/confusables](https://github.com/astral-sh/ruff/blob/69ace002102c7201f4514ffad87b87ce6a0d604f/crates/ruff_linter/src/rules/ruff/rules/confusables.rs#L5).

    Attributes:
        first (str): Sanitized first string after normalization.
        second (str): Sanitized second string after normalization.
        norm_case (bool): Normalize words with casefold.
        norm_utf8 (bool): Normalize UTF-8 glyph.

    """

    def __init__(self, first: str, second: str, norm_case: bool = False, norm_utf8: bool = True):
        """
        Initialize Comparative with two input strings, optionally casefolding them if norm_case is True.

        Args:
            first (str): Original first input string.
            second (str): Original second input string.
            norm_case (bool, optional): If True, both strings are
                converted with casefold for case-insensitive comparison.
            norm_utf8 (bool, optional): If True, both strings are
                normalized from C (NFC).

        """
        self.first: str = first
        self.second: str = second
        self.first, self.second = self._sanitize(self.first, self.second, norm_case=norm_case, norm_utf8=norm_utf8)

    def _sanitize(self, first: str, second: str, norm_case: bool = False, norm_utf8: bool = True) -> list[str]:
        if not isinstance(first, str) or not isinstance(second, str):
            raise ValueError("Both arguments must be strings.")

        if norm_utf8:
            first = unicodedata.normalize("NFC", first)
            second = unicodedata.normalize("NFC", second)

        first, second = first.strip(), second.strip()
        if len(first) > len(second):
            first, second = second, first

        if norm_case:
            first = first.casefold()
            second = second.casefold()

        return [first, second]

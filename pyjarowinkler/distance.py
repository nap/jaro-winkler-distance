"""Finds a non-euclidean distance or similarity between two strings."""

from typing import Final

from pyjarowinkler import JaroDistanceError
from pyjarowinkler.comparative import Comparative

__author__: Final[str] = "Jean-Bernard Ratte - jean.bernard.ratte@unary.ca"

__DEFAULT_DECIMALS__: Final[int] = 2
__DEFAULT_SCALING__: Final[float] = 0.1
__MAX_PREFIX_LENGTH__: Final[int] = 4
__MAX_SCALING__: Final[float] = 0.25


def _get_prefix(short: str, long: str) -> int:
    if short[:__MAX_PREFIX_LENGTH__] == long[:__MAX_PREFIX_LENGTH__]:
        return len(short[:__MAX_PREFIX_LENGTH__])

    prefix: int = 0
    for left, right in zip(short[:__MAX_PREFIX_LENGTH__], long[:__MAX_PREFIX_LENGTH__], strict=False):
        if left != right:
            break

        prefix += 1

    return min(prefix, __MAX_PREFIX_LENGTH__)


def _get_limit(long: list[str]) -> int:
    return max(0, len(long) // 2 - 1)


def _clean(assigned: list[str]) -> None:
    assigned[:] = [x for x in assigned if x]


def _get_transpositions(first: list[str], second: list[str]) -> int:
    return sum(left != right for left, right in zip(first, second, strict=True)) // 2


def _get_matches_and_transpositions(short: list[str], long: list[str]) -> tuple[int, int]:
    assigned_short: list[str] = [""] * len(short)
    assigned_long: list[str] = [""] * len(long)

    limit: int = _get_limit(long)
    for position, character in enumerate(short):
        left: int = max(0, position - limit)
        right: int = min(len(long), position + limit + 1)

        try:
            index: int = long.index(character, left, right)
            assigned_short[position] = assigned_long[index] = character
            long[index] = ""

        except ValueError:
            continue

    _clean(assigned_short)
    _clean(assigned_long)

    return len(assigned_short), _get_transpositions(assigned_short, assigned_long)


def _similarity(short: str, long: str) -> float:
    if short == long:
        return 1.0

    if len(short) < 1 or len(long) < 1:
        return 0.0

    matches, transpositions = _get_matches_and_transpositions(list(short), list(long))
    if matches == 0:
        return 0.0

    return (matches / len(short) + matches / len(long) + (matches - transpositions) / matches) / 3


def get_jaro_similarity(
    first: str,
    second: str,
    decimals: int = __DEFAULT_DECIMALS__,
    norm_case: bool = False,
    norm_utf8: bool = False,
    norm_ambiguous: bool = False,
) -> float:
    """
    Return the Jaro similarity of two strings.

    Args:
        first (str): String to calculate Jaro similarity for.
        second (str): String to calculate Jaro similarity with.
        norm_case (bool, optional): Convert string to uppercase characters.
        norm_utf8 (bool, optional): If True, both strings are normalized from C (NFC).
        norm_ambiguous (bool, optional): Normalize ambiguous glyphs.
        decimals (int, optional): Number of decimals to allow in result, defaults to 2.

    Raises:
        JaroDistanceError: If provided arguments aren't strings.

    Returns:
        float: Similarity between the two provided strings.

    """
    comparative: Comparative = Comparative(first, second, norm_case=norm_case, norm_utf8=norm_utf8, norm_ambiguous=norm_ambiguous)

    return round(_similarity(comparative.first, comparative.second), decimals)


def get_jaro_distance(
    first: str,
    second: str,
    decimals: int = __DEFAULT_DECIMALS__,
    norm_case: bool = False,
    norm_utf8: bool = False,
    norm_ambiguous: bool = False,
) -> float:
    """
    Return the Jaro distance (`1 - jaro_similarity`) of two strings.

    Args:
        first (str): String to calculate Jaro distance for.
        second (str): String to calculate Jaro distance with.
        norm_case (bool, optional): Convert string to uppercase characters.
        norm_utf8 (bool, optional): If True, both strings are normalized from C (NFC).
        norm_ambiguous (bool, optional): Normalize ambiguous glyphs.
        decimals (int, optional): Number of decimals to allow in result, defaults to 2.

    Raises:
        JaroDistanceError: If provided arguments aren't strings.

    Returns:
        float: Distance between the two provided strings.

    """
    try:
        comparative: Comparative = Comparative(
            first, second, norm_case=norm_case, norm_utf8=norm_utf8, norm_ambiguous=norm_ambiguous
        )
        return round(1 - _similarity(comparative.first, comparative.second), decimals)

    except ValueError as e:
        raise JaroDistanceError from e


def get_jaro_winkler_similarity(
    first: str,
    second: str,
    scaling: float = __DEFAULT_SCALING__,
    decimals: int = __DEFAULT_DECIMALS__,
    norm_case: bool = False,
    norm_utf8: bool = False,
    norm_ambiguous: bool = False,
) -> float:
    """
    Return the Jaro Winkler similarity of two strings.

    Args:
        first (str): String to calculate similarity for.
        second (str): String to calculate similarity with.
        scaling (float, optional): Scaling factor of the prefix of the compared strings, typically between 0.0 and 0.25,
            defaults to 0.1.
        decimals (int, optional): Number of decimals to allow in result.
        norm_case (bool, optional): Convert string to uppercase characters.
        norm_utf8 (bool, optional): If True, both strings are normalized from C (NFC).
        norm_ambiguous (bool, optional): Normalize ambiguous glyphs.

    Raises:
        JaroDistanceError: If provided arguments aren't strings.

    Returns:
        float: Jaro Winkler similarity score.

    """
    if scaling > __MAX_SCALING__ or scaling < 0:
        raise JaroDistanceError("Provided value for scaling factor is invalid.")

    try:
        comparative: Comparative = Comparative(
            first, second, norm_case=norm_case, norm_utf8=norm_utf8, norm_ambiguous=norm_ambiguous
        )
        similarity: float = _similarity(comparative.first, comparative.second)

        return round(similarity + (_get_prefix(comparative.first, comparative.second) * scaling * (1 - similarity)), decimals)

    except ValueError as e:
        raise JaroDistanceError from e


def get_jaro_winkler_distance(
    first: str,
    second: str,
    scaling: float = __DEFAULT_SCALING__,
    decimals: int = __DEFAULT_DECIMALS__,
    norm_case: bool = False,
    norm_utf8: bool = False,
    norm_ambiguous: bool = False,
) -> float:
    """
    Return the Jaro Winkler distance (`1 - jaro_winkler_similarity`) of two strings.

    Args:
        first (str): String to calculate distance for.
        second (str): String to calculate distance with.
        scaling (float, optional): Scaling factor of the prefix of the compared strings, typically between 0.0 and 0.25,
            defaults to 0.1.
        decimals (int, optional): Number of decimals to allow in result.
        norm_case (bool, optional): Convert string to uppercase characters.
        norm_utf8 (bool, optional): If True, both strings are normalized from C (NFC).
        norm_ambiguous (bool, optional): Normalize ambiguous glyphs.

    Raises:
        JaroDistanceError: If provided arguments aren't strings.

    Returns:
        float: Jaro Winkler distance score.

    """
    if scaling > __MAX_SCALING__ or scaling < 0:
        raise JaroDistanceError("Provided value for scaling factor is invalid.")

    try:
        comparative: Comparative = Comparative(
            first, second, norm_case=norm_case, norm_utf8=norm_utf8, norm_ambiguous=norm_ambiguous
        )
        similarity: float = _similarity(comparative.first, comparative.second)

        return round(
            1 - (similarity + (_get_prefix(comparative.first, comparative.second) * scaling * (1 - similarity))),
            decimals,
        )

    except ValueError as e:
        raise JaroDistanceError from e

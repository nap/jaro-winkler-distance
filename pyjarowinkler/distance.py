from pyjarowinkler import JaroDistanceError

__author__ = "Jean-Bernard Ratte - jean.bernard.ratte@unary.ca"

__DEFAULT_DECIMALS__: int = 2
__DEFAULT_SCALING__: float = 0.1
__MAX_PREFIX_LENGTH__: int = 4


def _get_prefix(short: str, long: str) -> int:
    if short[:__MAX_PREFIX_LENGTH__] == long[:__MAX_PREFIX_LENGTH__]:
        return len(short[:__MAX_PREFIX_LENGTH__])

    prefix: int = 0
    for left, right in zip(short[:__MAX_PREFIX_LENGTH__], long[:__MAX_PREFIX_LENGTH__]):
        if left != right:
            break

        prefix += 1

    return min(prefix, __MAX_PREFIX_LENGTH__)


def _get_limit(long: list[str]) -> int:
    return max(0, len(long) // 2 - 1)


def _clean(assigned: list[str]) -> None:
    for _ in range(assigned.count("")):
        assigned.remove("")


def _get_transpositions(first: list[str], second: list[str]) -> int:
    return sum(left != right for left, right in zip(first, second)) // 2


def _sanitize(first: str, second: str, *, ignore_case: bool = False) -> list[str]:
    if not isinstance(first, str) or not isinstance(second, str):
        message: str = "Cannot calculate distance from provided values."
        raise JaroDistanceError(message)

    first, second = first.strip(), second.strip()
    if len(first) > len(second):
        first, second = second, first

    if ignore_case:
        first = first.upper()
        second = second.upper()

    return [first, second]


def _get_matches_and_transpositions(short: list[str], long: list[str]) -> tuple[int, int]:
    assigned_short: list[str] = [""] * len(short)
    assigned_long: list[str] = [""] * len(long)

    limit: int = _get_limit(long)
    for position, character in enumerate(short):
        left: int = max(0, position - limit)
        right: int = min(len(long), position + limit + 1)

        if character in long[left:right]:
            index: int = long.index(character, left, right)
            assigned_short[position] = assigned_long[index] = character
            long[index] = ""

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
    first: str, second: str, *, decimals: int = __DEFAULT_DECIMALS__, ignore_case: bool = False
) -> float:
    """
    Return the Jaro similarity of two strings.

    :param first: String to calculate Jaro similarity for.
    :param second: String to calculate Jaro similarity with.
    :param ignore_case: Convert string to uppercase characters.
    :param decimals: Number of decimals to allow in result, defaults to :data:`2`.
    :raises JaroDistanceError: Raises an exception if provided arguments aren't strings.
    :return: Similarity between the two provided strings.
    """
    short, long = _sanitize(first, second, ignore_case=ignore_case)
    return round(_similarity(short, long), decimals)


def get_jaro_distance(
    first: str, second: str, *, decimals: int = __DEFAULT_DECIMALS__, ignore_case: bool = False
) -> float:
    """
    Return the Jaro distance (``1 - jaro_simiarity``) of two strings.

    :param first: String to calculate Jaro distance for.
    :param second: String to calculate Jaro distance with.
    :param ignore_case: Convert string to uppercase characters.
    :param decimals: Number of decimals to allow in result, defaults to :data:`2`.
    :raises JaroDistanceError: Raises an exception if provided arguments aren't strings.
    :return: Similarity between the two provided strings.
    """
    short, long = _sanitize(first, second, ignore_case=ignore_case)
    return round(1 - _similarity(short, long), decimals)


def get_jaro_winkler_similarity(
    first: str,
    second: str,
    *,
    scaling: float = __DEFAULT_SCALING__,
    decimals: int = __DEFAULT_DECIMALS__,
    ignore_case: bool = False,
) -> float:
    """
    Return the Jaro Winkler similarity of two strings.

    :param first: String to calculate distance for.
    :param second: String to calculate distance with.
    :param ignore_case: Convert string to uppercase characters.
    :param decimals: Number of decimals to allow in result.
    :param winkler: Adds Winkler adjustment factor to the similarity calculation.
    :param scaling: Scaling factor of the prefix of the compared strings, typically
        between :data:`0.0` and :data:`0.25`, defaults to :data:`0.1`.
    :raises JaroDistanceError: Raises an exception if provided arguments aren't strings.
    :return: Distance with or without the scaled similarity.
    """
    short, long = _sanitize(first, second, ignore_case=ignore_case)
    similarity: float = _similarity(short, long)
    return round(similarity + (_get_prefix(short, long) * scaling * (1 - similarity)), decimals)


def get_jaro_winkler_distance(
    first: str,
    second: str,
    *,
    scaling: float = __DEFAULT_SCALING__,
    decimals: int = __DEFAULT_DECIMALS__,
    ignore_case: bool = False,
) -> float:
    """
    Return the Jaro Winkler distance (``1 - jaro_winkler_simiarity``) of two strings.

    :param first: String to calculate distance for.
    :param second: String to calculate distance with.
    :param ignore_case: Convert string to uppercase characters.
    :param decimals: Number of decimals to allow in result.
    :param winkler: Adds Winkler adjustment factor to the similarity calculation.
    :param scaling: Scaling factor of the prefix of the compared strings, typically
        between :data:`0.0` and :data:`0.25`, defaults to :data:`0.1`.
    :raises JaroDistanceError: Raises an exception if provided arguments aren't strings.
    :return: Distance with or without the scaled similarity.
    """
    short, long = _sanitize(first, second, ignore_case=ignore_case)
    similarity: float = _similarity(short, long)
    return round(1 - (similarity + (_get_prefix(short, long) * scaling * (1 - similarity))), decimals)

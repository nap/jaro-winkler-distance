"""
Finds the Jaro Winkler Distance indicating a distance or similarity score between two strings.

:copyright: (c) 2015 by Jean-Bernard Ratte.
:license: Apache 2.0, see :file:`LICENSE` for more details.
"""

__author__: str = "Jean-Bernard Ratte - jean.bernard.ratte@unary.ca"


class JaroDistanceError(ValueError):
    """
    Exception raised for errors encountered during Jaro-Winkler distance calculations.

    Args:
        message (str): Explanation of the error.

    """

    def __init__(self, message: str) -> None:
        """
        Initialize the JaroDistanceError exception.

        Args:
            message (str): Explanation of the error.

        """
        super(ValueError, self).__init__(message)

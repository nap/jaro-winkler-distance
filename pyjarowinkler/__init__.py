"""
Finds the Jaro Winkler Distance indicating a distance or similarity score between two strings.

:copyright: (c) 2015 by Jean-Bernard Ratte.
:license: Apache 2.0, see :file:`LICENSE` for more details.
"""

__author__ = "Jean-Bernard Ratte - jean.bernard.ratte@unary.ca"


class JaroDistanceError(Exception):
    """
    Exception raised for errors encountered during Jaro-Winkler distance calculations.

    param: message (str): Explanation of the error.
    """

    def __init__(self, message) -> None:
        """
        Initialize the JaroDistanceError exception.

        param: message (str): Explanation of the error.
        """
        super(Exception, self).__init__(message)

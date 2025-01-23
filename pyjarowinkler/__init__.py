"""
Finds the Jaro Winkler Distance indicating a distance or similarity score between two strings.

:copyright: (c) 2015 by Jean-Bernard Ratte.
:license: Apache 2.0, see :file:`LICENSE` for more details.
"""

__author__ = "Jean-Bernard Ratte - jean.bernard.ratte@unary.ca"


class JaroDistanceError(Exception):
    def __init__(self, message) -> None:
        super(Exception, self).__init__(message)

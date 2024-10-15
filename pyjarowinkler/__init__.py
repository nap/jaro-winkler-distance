"""Find the Jaro Winkler Distance which indicates the similarity score between two strings.

The Jaro measure is the weighted sum of percentage of matched characters and transposed
characters. Winkler increased this measure for matching prefix characters.
This implementation is based on the Jaro Winkler similarity algorithm
from [Wikipedia article](http://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance).
The validation is based on the (Apache ``commons-text``)[https://github.com/apache/commons-text/blob/2f45b62a4e3c0953c3fc14982006a22c1a8a1ca8/src/main/java/org/apache/commons/text/similarity/JaroWinklerSimilarity.java] implementation.

:copyright: (c) 2015 by Jean-Bernard Ratte.
:license: Apache 2.0, see :file:`LICENSE` for more details.
"""  # noqa: E501

__author__ = "Jean-Bernard Ratte - jean.bernard.ratte@unary.ca"


class JaroDistanceError(Exception):
    def __init__(self, message) -> None:
        super(Exception, self).__init__(message)

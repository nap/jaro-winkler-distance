#cython: language_level=3
from cpython cimport array
import array

import math

__all__ = ['get_jaro_distance']
__author__ = 'Jean-Bernard Ratte - jean.bernard.ratte@unary.ca'

""" Find the Jaro Winkler Distance which indicates the similarity score between two Strings.
    The Jaro measure is the weighted sum of percentage of matched characters from each file and transposed characters.
    Winkler increased this measure for matching initial characters.

    This implementation is based on the Jaro Winkler similarity algorithm from
    http://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance

    This Python implementation is based on the Apache StringUtils implementation from
    http://commons.apache.org/proper/commons-lang/apidocs/src-html/org/apache/commons/lang3/StringUtils.html#line.7141
"""


cpdef float get_jaro_distance(str first, str second, bint winkler=True, bint winkler_ajustment=True, float scaling=0.1):
    cdef float jaro = _score(first, second)
    cdef int cl = min(len(_get_prefix(first, second)), 4)

    if all([winkler, winkler_ajustment]):  # 0.1 as scaling factor
        return round((jaro + (scaling * cl * (1.0 - jaro))) * 100.0) / 100.0

    return jaro

cpdef list get_jaro_distance_array(str first, list second, bint winkler=True, bint winkler_ajustment=True, float scaling=0.1):
    cdef list jaro = [get_jaro_distance(first, i, winkler, winkler_ajustment, scaling) for i in second]
    return jaro

cdef float _score(first, second):
    cdef str shorter = first.lower()
    cdef str longer =  second.lower()

    if len(first) > len(second):
        longer, shorter = shorter, longer

    cdef str m1 = _get_matching_characters(shorter, longer)
    cdef str m2 = _get_matching_characters(longer, shorter)

    if len(m1) == 0 or len(m2) == 0:
        return 0.0

    return (float(len(m1)) / len(shorter) +
            float(len(m2)) / len(longer) +
            float(len(m1) - _transpositions(m1, m2)) / len(m1)) / 3.0

cdef int _get_diff_index(str first, str second):
    if first == second:
        return -1

    if not first or not second:
        return 0

    cdef int max_len = min(len(first), len(second))
    for i in range(0, max_len):
        if not first[i] == second[i]:
            return i

    return max_len

cdef str _get_prefix(str first, str second):
    if not first or not second:
        return ""

    cdef int index = _get_diff_index(first, second)
    if index == -1:
        return first

    elif index == 0:
        return ""

    else:
        return first[0:index]

cdef str _get_matching_characters(str first, str second):
    cdef array.array common = array.array('u', [])
    cdef int limit = math.floor(min(len(first), len(second)) / 2)
    cdef int left
    cdef int right
    for i, l in enumerate(first):
        left = int(max(0, i - limit)) 
        right = int(min(i + limit + 1, len(second)))
        if l in second[left:right]:
            common.append(l)
            second = second[0:second.index(l)] + '*' + second[second.index(l) + 1:]

    return ''.join(common)

cdef int _transpositions(str first, str second):
    return math.floor(len([(f, s) for f, s in zip(first, second) if not f == s]) / 2.0)

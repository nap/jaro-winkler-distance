Jaro Winkler Distance
=====================

.. image:: https://travis-ci.org/nap/jaro-winkler-distance.svg?branch=master
    :target: https://travis-ci.org/nap/jaro-winkler-distance
.. image:: https://coveralls.io/repos/nap/jaro-winkler-distance/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/nap/jaro-winkler-distance?branch=master
.. image:: https://img.shields.io/github/license/nap/jaro-winkler-distance.svg
    :target: https://raw.githubusercontent.com/nap/jaro-winkler-distance/master/LICENSE
.. image:: https://img.shields.io/pypi/pyversions/pyjarowinkler.svg
    :target: https://pypi.python.org/pypi/pyjarowinkler

Find the Jaro Winkler Distance which indicates the similarity score between two Strings.
The Jaro measure is the weighted sum of percentage of matched characters from each file
and transposed characters. Winkler increased this measure for matching initial characters.

The Implementation
------------------
The original implementation is based on the `Jaro Winkler Similarity Algorithm <http://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance>`_ article that can be found on `Wikipedia <http://wikipedia.org>`_.
This Python version of the original implementation is based on the `Apache StringUtils <http://commons.apache.org/proper/commons-lang/apidocs/src-html/org/apache/commons/lang3/StringUtils.html#line.7141>`_ library.

Correctness
-----------
Unittest similar to what you will find in the ``StringUtils`` library were used to validate implementation.

Example
-------

::

    >>> from pyjarowinkler import distance
    >>> print distance.get_jaro_distance("hello", "haloa", winkler_ajustment=True)
    0.76
    >>> print distance.get_jaro_distance("hello", "haloa", winkler_ajustment=False)
    0.733333333333

:Version: 1.4 of 2015-08-30

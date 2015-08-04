Jaro Winkler Distance
=====================

.. image:: https://travis-ci.org/nap/jaro-winkler-distance.svg?branch=master
    :target: https://travis-ci.org/nap/jaro-winkler-distance

.. image:: https://coveralls.io/repos/nap/jaro-winkler-distance/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/nap/jaro-winkler-distance?branch=master


**Require python >= 2.7**

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
    >>> print distance.get_jaro_distance("hello", "haloa")
    0.76

:Version: 0.1.1 of 2015-08-02

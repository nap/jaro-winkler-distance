"""
Example for using :func:`distance.get_jaro_distance` of the ``pyjarowinkler`` module.
"""
__author__ = "Jean-Bernard Ratte - jean.bernard.ratte@unary.ca"

from pyjarowinkler import distance

if __name__ == "__main__":
    dist: float = distance.get_jaro_distance("hello", "haloa")
    print(f"The words 'hello' and 'haloa' matches at {dist:.1%}.")

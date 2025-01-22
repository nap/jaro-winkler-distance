"""Example for using :func:`distance.get_jaro_distance` of the ``pyjarowinkler`` module."""

__author__ = "Jean-Bernard Ratte - jean.bernard.ratte@unary.ca"

from pyjarowinkler import distance

if __name__ == "__main__":
    dist: float = distance.get_jaro_distance("faremviel", "farmville")
    print(f"The words 'farmville' and 'faremviel' matches at {dist:.1%}.")

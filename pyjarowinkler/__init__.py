from sys import version_info
from pyjarowinkler import distance
if version_info[:2] > (2, 7):
    from pyjarowinkler import cydistance
__author__ = 'Jean-Bernard Ratte - jean.bernard.ratte@unary.ca'

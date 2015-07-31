__author__ = 'Jean-Bernard Ratte - jean.bernard.ratte@unary.ca'

from jarowinkler.jarowinkler import get_jaro_distance

if __name__ == "__main__":
    first = "hello"
    second = "haloa"
    print "The words '{0}' and '{1}' matches at {2}%".format(first, second, get_jaro_distance(first, second))

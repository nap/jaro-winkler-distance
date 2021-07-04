import sys
from pyjarowinkler import distance
if sys.version_info[:2] > (2, 7):
    from pyjarowinkler import cydistance
import unittest

__author__ = 'Jean-Bernard Ratte - jean.bernard.ratte@unary.ca'


class TestDistance(unittest.TestCase):
    def test_get_jaro_distance(self):
        self.assertEqual(0.0, distance.get_jaro_distance("fly", "ant"))
        self.assertEqual(0.44, distance.get_jaro_distance("elephant", "hippo"))
        self.assertEqual(0.91, distance.get_jaro_distance("ABC Corporation", "ABC Corp"))
        self.assertEqual(0.9, distance.get_jaro_distance("PENNSYLVANIA", "PENNCISYLVNIA"))
        self.assertEqual(0.93, distance.get_jaro_distance("D N H Enterprises Inc", "D & H Enterprises, Inc."))
        self.assertEqual(0.94, distance.get_jaro_distance("My Gym Children's Fitness Center",
                                                          "My Gym. Childrens Fitness"))

    def test_get_jaro_cydistance(self):
        if sys.version_info[:2] > (2, 7):
            self.assertEqual(0.0, round(cydistance.get_jaro_distance("fly", "ant"), 3))
            self.assertEqual(0.44, round(cydistance.get_jaro_distance("elephant", "hippo"), 3))
            self.assertEqual(0.91, round(cydistance.get_jaro_distance("ABC Corporation", "ABC Corp"), 3))
            self.assertEqual(0.9, round(cydistance.get_jaro_distance("PENNSYLVANIA", "PENNCISYLVNIA"), 3))
            self.assertEqual(0.93, round(cydistance.get_jaro_distance("D N H Enterprises Inc",
                                                                      "D & H Enterprises, Inc."), 3))
            self.assertEqual(0.94, round(cydistance.get_jaro_distance("My Gym Children's Fitness Center",
                                                                      "My Gym. Childrens Fitness"), 3))

    def test_get_jaro_distance_raises(self):
        self.assertRaises(distance.JaroDistanceException, distance.get_jaro_distance, None, None)
        self.assertRaises(distance.JaroDistanceException, distance.get_jaro_distance, " ", None)
        self.assertRaises(distance.JaroDistanceException, distance.get_jaro_distance, None, "")

    def test_transposition(self):
        self.assertEqual(distance._transpositions("", ""), 0)
        self.assertEqual(distance._transpositions("PENNSYLVANIA", "PENNCISYLVNIA"), 4)

    def test_get_diff_index(self):
        self.assertEqual(distance._get_diff_index(None, None), -1)
        self.assertEqual(distance._get_diff_index("", ""), -1)
        self.assertEqual(distance._get_diff_index("", "abc"), 0)
        self.assertEqual(distance._get_diff_index("abc", ""), 0)
        self.assertEqual(distance._get_diff_index("abc", "abc"), -1)
        self.assertEqual(distance._get_diff_index("ab", "abxyz"), 2)
        self.assertEqual(distance._get_diff_index("abcde", "xyz"), 0)
        self.assertEqual(distance._get_diff_index("abcde", "abxyz"), 2)

    def test_get_matching_characters(self):
        self.assertEqual(distance._get_matching_characters("hello", "halloa"), "hllo")
        self.assertEqual(distance._get_matching_characters("ABC Corporation",
                                                           "ABC Corp"), "ABC Corp")
        self.assertEqual(distance._get_matching_characters("PENNSYLVANIA",
                                                           "PENNCISYLVNIA"), "PENNSYLVANI")
        self.assertEqual(distance._get_matching_characters("My Gym Children's Fitness Center",
                                                           "My Gym. Childrens Fitness"), "My Gym Childrens Fitness")
        self.assertEqual(distance._get_matching_characters("D N H Enterprises Inc",
                                                           "D & H Enterprises, Inc."), "D  H Enterprises Inc")

    def test_get_prefix(self):
        self.assertEqual(distance._get_prefix(None, None), "")
        self.assertEqual(distance._get_prefix("", ""), "")
        self.assertEqual(distance._get_prefix("", None), "")
        self.assertEqual(distance._get_prefix("", "abc"), "")
        self.assertEqual(distance._get_prefix("abc", ""), "")
        self.assertEqual(distance._get_prefix("abc", "abc"), "abc")
        self.assertEqual(distance._get_prefix("abc", "a"), "a")
        self.assertEqual(distance._get_prefix("ab", "abxyz"), "ab")
        self.assertEqual(distance._get_prefix("abcde", "abxyz"), "ab")
        self.assertEqual(distance._get_prefix("abcde", "xyz"), "")
        self.assertEqual(distance._get_prefix("xyz", "abcde"), "")
        self.assertEqual(distance._get_prefix("i am a machine", "i am a robot"), "i am a ")

    def test_score(self):
        self.assertEqual(distance._score("", ""), 0.0)
        self.assertEqual(distance._score("", "a"), 0.0)
        self.assertEqual(distance._score("ZDVSXA", "ZWEIUHFSAD"), 0.5111111111111111)
        self.assertEqual(distance._score("aaapppp", ""), 0.0)
        self.assertEqual(distance._score("fly", "ant"), 0.0)
        self.assertEqual(distance._score("elephant", "hippo"), 0.44166666666666665)
        self.assertEqual(distance._score("hippo", "elephant"), 0.44166666666666665)
        self.assertEqual(distance._score("hippo", "zzzzzzzz"), 0.0)
        self.assertEqual(distance._score("hello", "hallo"), 0.8666666666666667)
        self.assertEqual(distance._score("ABC Corporation", "ABC Corp"), 0.8444444444444444)
        self.assertEqual(distance._score("PENNSYLVANIA", "PENNCISYLVNIA"), 0.8300310800310801)
        self.assertEqual(distance._score("My Gym Children's Fitness Center",
                                         "My Gym. Childrens Fitness"), 0.9033333333333333)
        self.assertEqual(distance._score("D N H Enterprises Inc", "D & H Enterprises, Inc."), 0.9073153899240856)

    def test_get_jaro_without_winkler(self):
        self.assertEqual(distance.get_jaro_distance("ZDVSXA", "ZWEIUHFSAD",
                                                    winkler_ajustment=False), 0.5111111111111111)
        self.assertEqual(distance.get_jaro_distance("frog", "fog",
                                                    winkler_ajustment=False), 0.9166666666666666)
        self.assertEqual(distance.get_jaro_distance("fly", "ant",
                                                    winkler_ajustment=False), 0.0)
        self.assertEqual(distance.get_jaro_distance("elephant", "hippo",
                                                    winkler_ajustment=False), 0.44166666666666665)
        self.assertEqual(distance.get_jaro_distance("hippo", "elephant",
                                                    winkler_ajustment=False), 0.44166666666666665)
        self.assertEqual(distance.get_jaro_distance("hippo", "zzzzzzzz",
                                                    winkler_ajustment=False), 0.0)
        self.assertEqual(distance.get_jaro_distance("hello", "hallo",
                                                    winkler_ajustment=False), 0.8666666666666667)
        self.assertEqual(distance.get_jaro_distance("ABC Corporation", "ABC Corp",
                                                    winkler_ajustment=False), 0.8444444444444444)
        self.assertEqual(distance.get_jaro_distance("PENNSYLVANIA", "PENNCISYLVNIA",
                                                    winkler_ajustment=False), 0.8300310800310801)
        self.assertEqual(distance.get_jaro_distance("My Gym Children's Fitness Center",
                                                    "My Gym. Childrens Fitness",
                                                    winkler_ajustment=False), 0.9033333333333333)
        self.assertEqual(distance.get_jaro_distance("D N H Enterprises Inc",
                                                    "D & H Enterprises, Inc.",
                                                    winkler_ajustment=False), 0.9073153899240856)

    def test_get_jaro_without_winkler_cy(self):
        if sys.version_info[:2] > (2, 7):
            self.assertEqual(round(cydistance.get_jaro_distance("ZDVSXA", "ZWEIUHFSAD",
                                                                winkler_ajustment=False), 3),
                             round(0.5111111402511597, 3))
            self.assertEqual(round(cydistance.get_jaro_distance("frog", "fog",
                                                                winkler_ajustment=False), 3),
                             round(0.9166666666666666, 3))
            self.assertEqual(round(cydistance.get_jaro_distance("fly", "ant",
                                                                winkler_ajustment=False), 3),
                             round(0.0, 3))
            self.assertEqual(round(cydistance.get_jaro_distance("elephant", "hippo",
                                                                winkler_ajustment=False), 3),
                             round(0.44166666666666665, 3))
            self.assertEqual(round(cydistance.get_jaro_distance("hippo", "elephant",
                                                                winkler_ajustment=False), 3),
                             round(0.44166666666666665, 3))
            self.assertEqual(round(cydistance.get_jaro_distance("hippo", "zzzzzzzz",
                                                                winkler_ajustment=False), 3),
                             round(0.0, 3))
            self.assertEqual(round(cydistance.get_jaro_distance("hello", "hallo",
                                                                winkler_ajustment=False), 3),
                             round(0.8666666666666667, 3))
            self.assertEqual(round(cydistance.get_jaro_distance("ABC Corporation", "ABC Corp",
                                                                winkler_ajustment=False), 3),
                             round(0.8444444444444444, 3))
            self.assertEqual(round(cydistance.get_jaro_distance("PENNSYLVANIA", "PENNCISYLVNIA",
                                                                winkler_ajustment=False), 3),
                             round(0.8300310800310801, 3))
            self.assertEqual(round(cydistance.get_jaro_distance("My Gym Children's Fitness Center",
                                                                "My Gym. Childrens Fitness",
                                                                winkler_ajustment=False), 3),
                             round(0.9033333333333333, 3))
            self.assertEqual(round(cydistance.get_jaro_distance("D N H Enterprises Inc",
                                                                "D & H Enterprises, Inc.",
                                                                winkler_ajustment=False), 3),
                             round(0.9073153899240856, 3))


if __name__ == '__main__':
    unittest.main()

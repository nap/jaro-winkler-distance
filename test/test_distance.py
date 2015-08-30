from pyjarowinkler import distance
import unittest

__author__ = 'Jean-Bernard Ratte - jean.bernard.ratte@unary.ca'


class TestDistance(unittest.TestCase):
    def test_get_jaro_distance(self):
        self.assertEquals(0.0, distance.get_jaro_distance("fly", "ant"))
        self.assertEquals(0.44, distance.get_jaro_distance("elephant", "hippo"))
        self.assertEquals(0.91, distance.get_jaro_distance("ABC Corporation", "ABC Corp"))
        self.assertEquals(0.9, distance.get_jaro_distance("PENNSYLVANIA", "PENNCISYLVNIA"))
        self.assertEquals(0.93, distance.get_jaro_distance("D N H Enterprises Inc", "D & H Enterprises, Inc."))
        self.assertEquals(0.94, distance.get_jaro_distance("My Gym Children's Fitness Center",
                                                           "My Gym. Childrens Fitness"))

    def test_get_jaro_distance_raises(self):
        self.assertRaises(distance.JaroDistanceException, distance.get_jaro_distance, None, None)
        self.assertRaises(distance.JaroDistanceException, distance.get_jaro_distance, " ", None)
        self.assertRaises(distance.JaroDistanceException, distance.get_jaro_distance, None, "")

    def test_transposition(self):
        self.assertEqual(distance._transpositions("", ""), 0)
        self.assertEqual(distance._transpositions("PENNSYLVANIA", "PENNCISYLVNIA"), 4)

    def test_get_diff_index(self):
        self.assertEquals(distance._get_diff_index(None, None), -1)
        self.assertEquals(distance._get_diff_index("", ""), -1)
        self.assertEquals(distance._get_diff_index("", "abc"), 0)
        self.assertEquals(distance._get_diff_index("abc", ""), 0)
        self.assertEquals(distance._get_diff_index("abc", "abc"), -1)
        self.assertEquals(distance._get_diff_index("ab", "abxyz"), 2)
        self.assertEquals(distance._get_diff_index("abcde", "xyz"), 0)
        self.assertEquals(distance._get_diff_index("abcde", "abxyz"), 2)

    def test_get_matching_characters(self):
        self.assertEqual(distance._get_matching_characters("hello", "halloa"), "hllo")
        self.assertEquals(distance._get_matching_characters("ABC Corporation",
                                                            "ABC Corp"), "ABC Corp")
        self.assertEquals(distance._get_matching_characters("PENNSYLVANIA",
                                                            "PENNCISYLVNIA"), "PENNSYLVANI")
        self.assertEquals(distance._get_matching_characters("My Gym Children's Fitness Center",
                                                            "My Gym. Childrens Fitness"), "My Gym Childrens Fitness")
        self.assertEquals(distance._get_matching_characters("D N H Enterprises Inc",
                                                            "D & H Enterprises, Inc."), "D  H Enterprises Inc")

    def test_get_prefix(self):
        self.assertEquals(distance._get_prefix(None, None), "")
        self.assertEquals(distance._get_prefix("", ""), "")
        self.assertEquals(distance._get_prefix("", None), "")
        self.assertEquals(distance._get_prefix("", "abc"), "")
        self.assertEquals(distance._get_prefix("abc", ""), "")
        self.assertEquals(distance._get_prefix("abc", "abc"), "abc")
        self.assertEquals(distance._get_prefix("abc", "a"), "a")
        self.assertEquals(distance._get_prefix("ab", "abxyz"), "ab")
        self.assertEquals(distance._get_prefix("abcde", "abxyz"), "ab")
        self.assertEquals(distance._get_prefix("abcde", "xyz"), "")
        self.assertEquals(distance._get_prefix("xyz", "abcde"), "")
        self.assertEquals(distance._get_prefix("i am a machine", "i am a robot"), "i am a ")

    def test_score(self):
        self.assertEquals(distance._score("", ""), 0.0)
        self.assertEquals(distance._score("", "a"), 0.0)
        self.assertEquals(distance._score("ZDVSXA", "ZWEIUHFSAD"), 0.0)
        self.assertEquals(distance._score("aaapppp", ""), 0.0)
        self.assertEquals(distance._score("fly", "ant"), 0.0)
        self.assertEquals(distance._score("elephant", "hippo"), 0.44166666666666665)
        self.assertEquals(distance._score("hippo", "elephant"), 0.44166666666666665)
        self.assertEquals(distance._score("hippo", "zzzzzzzz"), 0.0)
        self.assertEquals(distance._score("hello", "hallo"), 0.8666666666666667)
        self.assertEquals(distance._score("ABC Corporation", "ABC Corp"), 0.8444444444444444)
        self.assertEquals(distance._score("PENNSYLVANIA", "PENNCISYLVNIA"), 0.8300310800310801)
        self.assertEquals(distance._score("My Gym Children's Fitness Center",
                                          "My Gym. Childrens Fitness"), 0.9033333333333333)
        self.assertEquals(distance._score("D N H Enterprises Inc", "D & H Enterprises, Inc."), 0.9073153899240856)

    def test_get_jaro_without_winkler(self):
        self.assertEquals(distance.get_jaro_distance("ZDVSXA", "ZWEIUHFSAD",
                                                     winkler_ajustment=False), 0.0)
        self.assertEquals(distance.get_jaro_distance("frog", "fog",
                                                     winkler_ajustment=False), 0.9166666666666666)
        self.assertEquals(distance.get_jaro_distance("fly", "ant",
                                                     winkler_ajustment=False), 0.0)
        self.assertEquals(distance.get_jaro_distance("elephant", "hippo",
                                                     winkler_ajustment=False), 0.44166666666666665)
        self.assertEquals(distance.get_jaro_distance("hippo", "elephant",
                                                     winkler_ajustment=False), 0.44166666666666665)
        self.assertEquals(distance.get_jaro_distance("hippo", "zzzzzzzz",
                                                     winkler_ajustment=False), 0.0)
        self.assertEquals(distance.get_jaro_distance("hello", "hallo",
                                                     winkler_ajustment=False), 0.8666666666666667)
        self.assertEquals(distance.get_jaro_distance("ABC Corporation", "ABC Corp",
                                                     winkler_ajustment=False), 0.8444444444444444)
        self.assertEquals(distance.get_jaro_distance("PENNSYLVANIA", "PENNCISYLVNIA",
                                                     winkler_ajustment=False), 0.8300310800310801)
        self.assertEquals(distance.get_jaro_distance("My Gym Children's Fitness Center",
                                                     "My Gym. Childrens Fitness",
                                                     winkler_ajustment=False), 0.9033333333333333)
        self.assertEquals(distance.get_jaro_distance("D N H Enterprises Inc",
                                                     "D & H Enterprises, Inc.",
                                                     winkler_ajustment=False), 0.9073153899240856)


if __name__ == '__main__':
    unittest.main()

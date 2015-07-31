__author__ = 'Jean-Bernard Ratte - jean.bernard.ratte@unary.ca'
import unittest
from jarowinkler import distance


class TestDistance(unittest.TestCase):
    def test_get_jaro_distance(self):
        self.assertEquals(float(0.93), distance.get_jaro_distance("frog", "fog"))
        self.assertEquals(float(0.0), distance.get_jaro_distance("fly", "ant"))
        self.assertEquals(float(0.44), distance.get_jaro_distance("elephant", "hippo"))
        self.assertEquals(float(0.91), distance.get_jaro_distance("ABC Corporation", "ABC Corp"))
        # self.assertEquals(float(0.9), distance.get_jaro_distance("PENNSYLVANIA", "PENNCISYLVNIA"))
        self.assertEquals(float(0.94), distance.get_jaro_distance("My Gym Children's Fitness Center",
                                                                  "My Gym. Childrens Fitness"))

    def test_get_jaro_distance_raises(self):
        with self.assertRaises(distance.JaroDistanceException) as e:
            distance.get_jaro_distance(None, None)
        self.assertTrue('NoneType, NoneType' in e.exception.message)

        with self.assertRaises(distance.JaroDistanceException) as e:
            distance.get_jaro_distance(" ", None)
        self.assertTrue('str, NoneType' in e.exception.message)

        with self.assertRaises(distance.JaroDistanceException) as e:
            distance.get_jaro_distance(None, "")
        self.assertTrue('NoneType, str' in e.exception.message)

    def test_transposition(self):
        self.assertEqual(distance._transpositions("ab", "ac"), 1, "abc")
        self.assertEqual(distance._transpositions("", ""), 0, "Empty string should return zero transpositions")

    def test_score(self):
        pass

    def test_get_diff_index(self):
        pass

    def test_get_prefix(self):
        pass

    def test_get_matching_characters(self):
        pass

if __name__ == '__main__':
    unittest.main()

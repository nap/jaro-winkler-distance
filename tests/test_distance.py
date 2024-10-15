import unittest

from pyjarowinkler import distance

__author__ = "Jean-Bernard Ratte - jean.bernard.ratte@unary.ca"


class TestDistance(unittest.TestCase):
    def test_get_prefix_no_prefix(self) -> None:
        self.assertEqual(distance._get_prefix("1234", "9876"), 0)

    def test_get_prefix_zero_length(self) -> None:
        self.assertEqual(distance._get_prefix("", ""), 0)

    def test_get_prefix_small_length(self) -> None:
        self.assertEqual(distance._get_prefix("aa", "aaaaa"), 2)

    def test_get_prefix_long_length(self) -> None:
        self.assertEqual(distance._get_prefix("123456", "123456789"), 4)

    def test_get_prefix_full_prefix(self) -> None:
        self.assertEqual(distance._get_prefix("vache", "vacheron"), 4)

    def test_get_prefix_partial_prefix(self) -> None:
        self.assertEqual(distance._get_prefix("vache", "vagabon"), 2)

    def test_sanitize_exception(self) -> None:
        with self.assertRaises(distance.JaroDistanceError):
            distance._sanitize(None, None)

    def test_sanitize_exception_args(self) -> None:
        with self.assertRaises(distance.JaroDistanceError):
            distance._sanitize("4", 333)

    def test_sanitize_spaces(self) -> None:
        self.assertEqual(distance._sanitize("   asdf ", "asdf     "), ["asdf", "asdf"])

    def test_get_limit_less_than_max(self) -> None:
        self.assertEqual(distance._get_limit(""), 0)

    def test_clean(self) -> None:
        test: list[str] = ["", "cd", "", "", "ab"]
        distance._clean(test)
        self.assertEqual(test, ["cd", "ab"])

    def test_get_transpositions(self) -> None:
        self.assertEqual(distance._get_transpositions(["a", "b", "c"], ["a", "c", "b"]), 1)

    def test_get_transpositions_special(self) -> None:
        self.assertEqual(distance._get_transpositions(["2", "7", "0", "0", "0"], ["2", "7", "0", "0"]), 0.0)

    def test_get_jaro_winkler_similarity_empty(self) -> None:
        self.assertEqual(distance.get_jaro_winkler_similarity("", ""), 1.0)

    def test_get_jaro_winkler_similarity_equal(self) -> None:
        self.assertEqual(distance.get_jaro_winkler_similarity("foo", "foo"), 1.0)

    def test_get_jaro_winkler_similarity_half_empty(self) -> None:
        self.assertEqual(distance.get_jaro_winkler_similarity("", "a"), 0.0)

    def test_get_jaro_winkler_similarity_half_empty_reversed(self) -> None:
        self.assertEqual(distance.get_jaro_winkler_similarity("aaapppp", ""), 0.0)

    def test_get_jaro_winkler_similarity_zero_similarity(self) -> None:
        self.assertEqual(distance.get_jaro_winkler_similarity("fly", "ant"), 0.0)

    def test_get_jaro_winkler_similarity_zero_similarity_long(self) -> None:
        self.assertEqual(distance.get_jaro_winkler_similarity("hippo", "zzzzzzzz"), 0.0)

    def test_get_jaro_winkler_similarity_martha(self) -> None:
        self.assertEqual(distance.get_jaro_winkler_similarity("MARTHA", "MARHTA"), 0.96)

    def test_get_jaro_winkler_similarity_dwayne(self) -> None:
        self.assertEqual(distance.get_jaro_winkler_similarity("DWAYNE", "DUANE"), 0.84)

    def test_get_jaro_winkler_similarity_dixon(self) -> None:
        self.assertEqual(distance.get_jaro_winkler_similarity("DIXON", "DICKSONX"), 0.81)

    def test_get_jaro_winkler_similarity_75000(self) -> None:
        self.assertEqual(distance.get_jaro_winkler_similarity("75000", "75020", decimals=3), 0.907)

    def test_get_jaro_winkler_similarity_elephant(self) -> None:
        self.assertEqual(distance.get_jaro_winkler_similarity("elephant", "hippo"), 0.44)

    def test_get_jaro_winkler_similarity_hippo(self) -> None:
        self.assertEqual(distance.get_jaro_winkler_similarity("hippo", "elephant"), 0.44)

    def test_get_jaro_winkler_similarity_pennsylvania(self) -> None:
        self.assertEqual(distance.get_jaro_winkler_similarity("PENNSYLVANIA", "PENNCISYLVNIA", decimals=2), 0.90)

    def test_get_jaro_winkler_similarity_frog(self) -> None:
        self.assertEqual(distance.get_jaro_winkler_similarity("frog", "fog", decimals=3), 0.925)

    def test_get_jaro_winkler_similarity_hello(self) -> None:
        self.assertEqual(distance.get_jaro_winkler_similarity("hello", "hallo"), 0.88)

    def test_get_jaro_winkler_similarity_abc_corporation(self) -> None:
        self.assertEqual(distance.get_jaro_winkler_similarity("ABC Corporation", "ABC Corp"), 0.91)

    def test_get_jaro_winkler_similarity_apple(self) -> None:
        self.assertEqual(distance.get_jaro_winkler_similarity("apple", "applet"), 0.97)

    def test_get_jaro_similarity_jake(self) -> None:
        self.assertEqual(distance.get_jaro_similarity("jake", "joe"), 0.72)

    def test_get_jaro_similarity_amy(self) -> None:
        self.assertEqual(distance.get_jaro_similarity("amy", "mary"), 0.81)

    def test_get_jaro_winkler_similarity_hello_no_change(self) -> None:
        self.assertEqual(distance.get_jaro_similarity("hello", "Haloa", ignore_case=False), 0.6)

    def test_get_jaro_winkler_similarity_hello_changed(self) -> None:
        self.assertEqual(distance.get_jaro_similarity("hello", "HaLoA", ignore_case=True), 0.73)

    def test_get_jaro_faremviel(self) -> None:
        self.assertEqual(distance.get_jaro_distance("faremviel", "farmville"), 0.12)

    def test_get_jaro_similarity_faremviel(self) -> None:
        self.assertEqual(distance.get_jaro_similarity("faremviel", "farmville"), 0.88)


if __name__ == "__main__":
    unittest.main()

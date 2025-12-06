import timeit
import unittest


class TestBenchmark(unittest.TestCase):
    def setUp(self):
        self.common_setup = """
from pyjarowinkler import distance
pairs = [
    ("faremviel", "farmville"),
    ("dwayne", "duane"),
    ("martha", "marhta"),
    ("abc", "abc"),
    ("abc", "xyz"),
    ("kitten", "sitting"),
    ("dixon", "dicksonx"),
    ("jellyfish", "smellyfish"),
    ("", ""),
    ("verylongstringthatmatches", "verylongstringthatmatches"),
]
"""
        self.number = 1000
        self.repeat = 5

    def _run_benchmark(self, func_name):
        stmt = f"[distance.{func_name}(p[0], p[1]) for p in pairs]"
        times = timeit.repeat(stmt, setup=self.common_setup, repeat=self.repeat, number=self.number)
        min_time = min(times)
        print(f"{func_name} (1k runs of 10 pairs): min={min_time:.4f}s, avg={sum(times) / len(times):.4f}s")
        self.assertLess(min_time, 0.018, f"{func_name} failed benchmark: {min_time:.4f}s > 0.018s")
        return times

    def test_jaro_distance_benchmark(self):
        self._run_benchmark("get_jaro_distance")

    def test_jaro_similarity_benchmark(self):
        self._run_benchmark("get_jaro_similarity")

    def test_jaro_winkler_distance_benchmark(self):
        self._run_benchmark("get_jaro_winkler_distance")

    def test_jaro_winkler_similarity_benchmark(self):
        self._run_benchmark("get_jaro_winkler_similarity")

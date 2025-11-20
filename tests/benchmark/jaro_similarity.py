
import timeit

def benchmark():
    setup = """
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
    stmt = "[distance.get_jaro_similarity(p[0], p[1]) for p in pairs]"
    # Reduced number of runs since we are doing 10x work per run
    times = timeit.repeat(stmt, setup=setup, repeat=5, number=1000)
    print(f"get_jaro_similarity (1k runs of 10 pairs): min={min(times):.4f}s, avg={sum(times)/len(times):.4f}s")

if __name__ == "__main__":
    benchmark()

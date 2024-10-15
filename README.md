# Jaro Winkler Distance

![PyPI - Version](https://img.shields.io/pypi/v/pyjarowinkler?style=flat-square)
![License](https://img.shields.io/github/license/nap/jaro-winkler-distance?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyjarowinkler?style=flat-square)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/nap/jaro-winkler-distance/workflow.yml)

This library find non-euclidean distance or similarity between two strings.

Jaro and Jaro-Winkler equations provides a score between two short words where errors are more prone at the end of the word. Jaro's equation measure is the weighted sum of percentage of equal and transposed characters from each strings. Winkler's factor adds a weight in Jaro's formula to increased the calculated measure when there are a sequance of characters (prefix) that matches between the compaired items.

> [!NOTE]
> * Impact of the character prefix is limited to 4, as originally defined by Winkler.
> * Input strings are not modified beyond leading or trailing whitespace stripping. In-word whitespace and characters case *will* optionally impact score.
> * Returns a floating point number rounded to the desired decimals (defaults to `2`) using Python's [`round()`](https://docs.python.org/3/library/functions.html#round).
> * Consider usual [Floating Point Arithmetic](https://docs.python.org/3/tutorial/floatingpoint.html#tut-fp-issues) characterisitcs.

## Notes on Calculation

The complexity of this algoritme reside in the calculation of `matching` and `transposed` characters.

* A character of the first string is `matching` if it's found in the second string within a specified `distance`. A character in the first string cannot be matched multiple time to the same character in the second string.
* Two characters are `transposed` if they match, but aren't matched at the same position.
* The `limit` is calculated using the length of the longest string devided by two minus one.

### Example

${d = \left \lfloor {\frac {\max(12, 13)}{2}}\right \rfloor - 1 = 5}$

```
----------------------------
   P E N N C I S Y L V N I A
P  1          |
E    1          |
N      1          |
N        1          |
S              1      |
Y  |             1      |
L    |             1      |
V      |             1      |
A        |                 1
N          |           1
I            |           1
A              |
----------------------------
```
${\text{Where }|s_{1}| = 12\text{, }|s_{2}| = 13\text{, }\ell = 4\text{, }m = 11\text{, }t = 3\text{, and }p = 0.1}$.

${sim_{j}=\left\{{\begin{array}{l l}0&{\text{if }}m=0\\{\frac {1}{3}}\left({\frac {m}{|s_{1}|}}+{\frac {m}{|s_{2}|}}+{\frac {m-t}{m}}\right)&{\text{otherwise}}\end{array}}\right.}$

${sim_{j}=\frac {1}{3}}\left({\frac {11}{12}}+{\frac {11}{13}}+{\frac {11-3}{11}}\right) = 0.83003108003$

${sim_{w} = sim_{j}+\ell p(1-sim_{j})}$

${sim_{w} =0.83003108003 + 4 * 0.1 * (1 - 0.83003108003) = 0.89801864801}$

${\lceil sim_{w}\rceil = 0.9}$

## Implementation

The original implementation is based on the [Jaro Winkler](https://www.census.gov/content/dam/Census/library/working-papers/1991/adrm/rr91-9.pdf) Similarity Algorithm article that can be found on [Wikipedia](http://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance). This version of is based on the [original C implementation of strcmp95](https://web.archive.org/web/20100227020019/http://www.census.gov/geo/msb/stand/strcmp.c) library.

## Example

```python
from pyjarowinkler import distance

distance.get_jaro_distance("hello", "haloa", decimals=2)
# 0.76
distance.get_jaro_winkler_distance("hello", "Haloa", scaling=0.1, ignore_case=False)
# 0.6
distance.get_jaro_winkler_distance("hello", "HaLoA", scaling=0.1, ignore_case=True)
# 0.73
```

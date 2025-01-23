# Jaro Winkler Distance

<div align="center">

![PyPI - Version](https://img.shields.io/pypi/v/pyjarowinkler?style=flat-square)
![License](https://img.shields.io/github/license/nap/jaro-winkler-distance?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyjarowinkler?style=flat-square)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/nap/jaro-winkler-distance/push.yml?branch=main&style=flat-square)

</div>

This library find non-euclidean distance or similarity between two strings.

Jaro and Jaro-Winkler equations provides a score between two short words where errors are more prone at the end of the word. Jaro's equation measure is the weighted sum of percentage of equal and transposed characters from each strings. Winkler's factor adds a weight in Jaro's formula to increased the calculated measure when there are a sequance of characters (prefix) that matches between the compaired items.

> [!NOTE]
> * Impact of prefix is limited to 4 characters, as originally defined by Winkler.
> * Input strings are not modified beyond whitespace trimming.
> * In-word whitespace and characters case can **optionally** impact score.
> * Returns a floating point number rounded to the desired decimals (defaults to `2`) using Python's [`round()`](https://docs.python.org/3/library/functions.html#round).
> * Consider usual [Floating Point Arithmetic](https://docs.python.org/3/tutorial/floatingpoint.html#tut-fp-issues) characterisitcs when working with this library.

## Notes on Calculation

The complexity of this algoritme reside in the calculation of `matching` and `transposed` characters. That is because the interepretation of the meaning of what are the `matching` conditions and `transposed` definition. Definitions of those words will make the score vary between implementations of the algorithme.

Here is how `matching` and `transposed` are definied:

* A character of the first string is `matching` if it's included in the second string within the specified `distance` on either sides.
* A character in the first string cannot be matched multiple time to the same character of the second string.
* Decimals are rounded according to the scientific method.
* Two characters are `transposed` if they match, but aren't matched at the same position.
* The `limit` is calculated using the length of the longest string devided by two minus one.

> [!IMPORTANT]
>
> **TODO**: Use python's std library [Decimal](https://docs.python.org/3.12/library/decimal.html)

### Example

Calculate the Jaro Winkler similarity ($sim_{w}$) between `PENNSYLVANIA` and `PENNCISYLVNIA`:

```math
s_{1}=\text{PENNSYLVANIA} \qquad\text{and}\qquad s_{2}=\text{PENNCISYLVNIA}
```

```
    P E N N C I S Y L V N I A
  ┌-─────────────────────────
P │ 1          ╎
E │   1          ╎
N │     1          ╎
N │       1          ╎          Symbole '╎' represent the sliding window's
S │             1      ╎        boundry in the second string where we look
Y │ ╎             1      ╎          for the first string's character.
L │   ╎             1      ╎
V │     ╎             1                   d = 5 in this example.
A │       ╎                 1
N │         ╎           1
I │           ╎           1
A │             ╎
```

```math
\begin{split}
   d &= \left\lfloor {\max(12, 13) \over 2} \right\rfloor - 1 \newline
     &= 5 \newline
\end{split}

\qquad
   \text{ and }
\qquad

\begin{split}
   |s_{1}| &= 12 \newline
   |s_{2}| &= 13 \newline
\end{split}

\qquad
   \text{ and }
\qquad

\begin{split}
   \ell &= 4 \newline
      m &= 11 \newline
      t &= 3 \newline
      p &= 0.1 \newline
\end{split}
```

Considering the input parameters calculated above:

```math
\begin{split}
   sim_{j} &=\begin{cases}
               0 & \text{if } m = 0 \newline
               {1 \over 3} \times \left({m \over |s_{1}|} + {m \over |s_{2}|} + {{m - t} \over m} \right) & \text{otherwise}
             \end{cases} \newline
           &={1 \over 3} \times \left({11 \over 12} + {11 \over 13} + {{11 - 3} \over 11}\right) \newline
           &= 0.83003108003 \newline
\end{split}

\qquad
   \text{then}
\qquad

\begin{split}
   sim_{w} &= sim_{j} + \ell \times p \times (1 - sim_{j}) \newline
           &= 0.83003108003 + 4 \times 0.1 \times (1 - 0.83003108003) \newline
           &= 0.89801864801 \newline
\end{split}
```

We found that the $\lceil sim_{w} \rceil$ is $0.9$.

## Implementation

The original implementation is based on the [Jaro Winkler](https://www.census.gov/content/dam/Census/library/working-papers/1991/adrm/rr91-9.pdf) Similarity Algorithm article that can be found on [Wikipedia](http://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance). This version of is based on the [original C implementation of strcmp95](https://web.archive.org/web/20100227020019/http://www.census.gov/geo/msb/stand/strcmp.c) library.

## Example

```python
from pyjarowinkler import distance

distance.get_jaro_similarity("PENNSYLVANIA", "PENNCISYLVNIA", decimals=12)
# 0.830031080031
distance.get_jaro_winkler_similarity("PENNSYLVANIA", "PENNCISYLVNIA", decimals=12)
# 0.898018648019
distance.get_jaro_distance("hello", "haloa", decimals=4)
# 0.2667
distance.get_jaro_similarity("hello", "haloa", decimals=2)
# 0.73
distance.get_jaro_winkler_distance("hello", "Haloa", scaling=0.1, ignore_case=False)
# 0.4
distance.get_jaro_winkler_distance("hello", "HaLoA", scaling=0.1, ignore_case=True)
# 0.24
distance.get_jaro_winkler_similarity("hello", "haloa", decimals=2)
# 0.76
```

## Contribute

You need to have installed [`asdf`](https://asdf-vm.com/) on your system. Then, running the commands below will setup your environment with the project's optional (dev) requirements and create the python virtual environment necessary to run test, lint, and build steps.

Typical order of execution is as follow:

```shell
$ cd ./jaro-winkler-distance
$ asdf install
$ pip install '.[dev]'
$ hatch python install 3.13 3.12 3.11 3.10 3.9
$ hatch env create
```

Other helpful commands:

* `hatch test`
* `hatch fmt`
* `hatch env show`
* `hatch run test:unit`
* `hatch run test:all`
* `hatch run lint:all`

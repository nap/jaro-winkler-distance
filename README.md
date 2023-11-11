# Jaro Winkler Distance

![Jaro Winkler Distance Build Status](https://github.com/nap/jaro-winkler-distance/actions/workflows/workflow.yml/badge.svg?branch=master)

Find the Jaro Winkler Distance which indicates the similarity score between two strings or words.
Jaro's equation measure is the weighted sum of percentage of matched and transposed characters from each strings. Winkler's factor increased this measure for matching prefixed characters.

## The Implementation

The original implementation is based on the Jaro Winkler Similarity Algorithm article that can be found on [Wikipedia](http://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance). This version of is based on the [Apache commons-text](https://github.com/apache/commons-text/blob/c2cb4501669e4148aebd9d7265430080f47af016/src/main/java/org/apache/commons/text/similarity/JaroWinklerSimilarity.java#L1-L167) library.

### Correctness

Unit tests similar to what you will find in the `commons-text` library were used to validate the implementation.

### Note

A limit of `shorter / 2 + 1` is used in `commons-text`, this differs from Wikipedia and also [Winkler's paper](https://files.eric.ed.gov/fulltext/ED325505.pdf), where a distance of `longer / 2 - 1` is used, corresponding to positions of `longer / 2`.

## Example

```python
from pyjarowinkler import distance
# Scaling is 0.1 by default
distance.get_jaro_distance("hello", "haloa", winkler=True, scaling=0.1)
# 0.76
distance.get_jaro_distance("hello", "haloa", winkler=False, scaling=0.1)
# 0.733333333333
```

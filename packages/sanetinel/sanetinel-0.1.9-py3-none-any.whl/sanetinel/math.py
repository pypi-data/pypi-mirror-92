# (c) 2020 Simon Rovder and others.
# This file is subject to the terms provided in 'LICENSE'.
"""
File providing common math functions.
"""
import math
import typing as t


def pdf(x: float, mean: float, stddev: float) -> float:
    return math.exp(-0.5 * ((x - mean) / stddev) ** 2) / (stddev * math.sqrt(2 * math.pi))


def linspace(start: float, stop: float, count: int) -> t.List[float]:
    step = (stop - start) / (count - 1)
    return [start + (i * step) for i in range(count)]

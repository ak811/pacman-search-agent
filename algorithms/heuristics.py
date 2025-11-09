from __future__ import annotations
from typing import Tuple
import math

def manhattan(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.hypot(dx, dy)
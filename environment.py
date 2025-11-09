from __future__ import annotations
from dataclasses import dataclass
from typing import Set, Tuple

@dataclass
class Environment:
    width: int
    height: int
    walls: Set[Tuple[int, int]]
    start: Tuple[int, int]
    goal: Tuple[int, int]

    def in_bounds(self, p: Tuple[int, int]) -> bool:
        x, y = p
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, p: Tuple[int, int]) -> bool:
        return p not in self.walls
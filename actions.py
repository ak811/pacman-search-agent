from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class Action:
    name: str
    dx: int
    dy: int

    def step(self, p: Tuple[int, int]) -> Tuple[int, int]:
        return (p[0] + self.dx, p[1] + self.dy)

RIGHT = Action("RIGHT", 1, 0)
UP    = Action("UP", 0, -1)
LEFT  = Action("LEFT", -1, 0)
DOWN  = Action("DOWN", 0, 1)

ALL_ACTIONS = (RIGHT, UP, LEFT, DOWN)
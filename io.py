from __future__ import annotations
import random
from typing import Set, Tuple
from .environment import Environment

# Supported map glyphs:
#   ' ' : empty
#   '*' : wall
#   '#': start (spawn)
#   'x' or 'X': goal
# If start or goal are missing, they will be chosen randomly on free cells.

def read_map(file_path: str) -> Environment:
    walls: Set[Tuple[int, int]] = set()
    start: Tuple[int, int] | None = None
    goal: Tuple[int, int] | None = None

    w = 0
    h = 0

    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    for y, line in enumerate(lines):
        w = max(w, len(line))
        for x, ch in enumerate(line):
            p = (x, y)
            if ch == "*":
                walls.add(p)
            elif ch == "#":
                if start is None:
                    start = p
            elif ch in ("x", "X"):
                if goal is None:
                    goal = p
            elif ch == " ":
                pass
            else:
                # Unknowns become empty space for robustness
                pass
        h += 1

    # Normalize missing start/goal by choosing random free cells
    def random_free() -> Tuple[int, int]:
        while True:
            p = (random.randint(0, w - 1), random.randint(0, h - 1))
            if p not in walls:
                return p

    if start is None:
        start = random_free()
    if goal is None:
        # Ensure goal differs from start
        g = random_free()
        while g == start:
            g = random_free()
        goal = g

    return Environment(w, h, walls, start, goal)
from __future__ import annotations
from typing import Callable, Iterable, List, Tuple
from collections import deque
from ..environment import Environment
from ..algorithms import bfs, dfs, ucs, astar, manhattan, euclidean
from .base import Agent

Coord = Tuple[int, int]

class SearchAgent(Agent):
    def __init__(
        self,
        env: Environment,
        algorithm: str = "astar",
        heuristic: str = "manhattan",
    ) -> None:
        self.env = env
        self.algorithm = algorithm.lower()
        self.heuristic = heuristic.lower()
        self._path: List[Coord] = []
        self._queue: deque[Coord] = deque()

    # Neighborhood helper
    def _neighbors(self, p: Coord) -> Iterable[Coord]:
        x, y = p
        for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
            q = (x + dx, y + dy)
            if self.env.in_bounds(q) and self.env.passable(q):
                yield q

    # Unit cost grid
    def _cost(self, a: Coord, b: Coord) -> float:
        return 1.0

    def reset(self, start: Coord):
        self._path.clear()
        self._queue.clear()

    def plan(self) -> List[Coord]:
        s, g = self.env.start, self.env.goal
        if self.algorithm == "bfs":
            path = bfs(s, g, self._neighbors)
        elif self.algorithm == "dfs":
            path = dfs(s, g, self._neighbors)
        elif self.algorithm == "ucs":
            path = ucs(s, g, self._neighbors, self._cost)
        elif self.algorithm == "astar":
            h = manhattan if self.heuristic == "manhattan" else euclidean
            path = astar(s, g, self._neighbors, self._cost, h)
        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")

        self._path = path
        self._queue = deque(path)
        return list(self._path)

    def step(self) -> Coord:
        if not self._queue:
            return self.env.start
        return self._queue.popleft()
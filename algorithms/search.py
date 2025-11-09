from __future__ import annotations
from typing import Callable, Dict, Iterable, List, Optional, Tuple
import heapq

Coord = Tuple[int, int]
NeighborsFn = Callable[[Coord], Iterable[Coord]]
CostFn = Callable[[Coord, Coord], float]
HeuristicFn = Callable[[Coord, Coord], float]

class _PQ:
    def __init__(self):
        self._h: List[Tuple[float, int, Coord]] = []
        self._t = 0
    def push(self, priority: float, p: Coord):
        self._t += 1
        heapq.heappush(self._h, (priority, self._t, p))
    def pop(self) -> Coord:
        return heapq.heappop(self._h)[2]
    def __len__(self):
        return len(self._h)

def _reconstruct(came: Dict[Coord, Optional[Coord]], goal: Coord) -> List[Coord]:
    path: List[Coord] = []
    cur: Optional[Coord] = goal
    while cur is not None:
        path.append(cur)
        cur = came.get(cur)
    path.reverse()
    return path

# Breadth-First Search (unit-cost)

def bfs(start: Coord, goal: Coord, neighbors: NeighborsFn) -> List[Coord]:
    from collections import deque
    q = deque([start])
    came: Dict[Coord, Optional[Coord]] = {start: None}
    while q:
        cur = q.popleft()
        if cur == goal:
            return _reconstruct(came, goal)
        for nxt in neighbors(cur):
            if nxt not in came:
                came[nxt] = cur
                q.append(nxt)
    return []

# Depth-First Search (returns first found path, not guaranteed shortest)

def dfs(start: Coord, goal: Coord, neighbors: NeighborsFn) -> List[Coord]:
    stack = [start]
    came: Dict[Coord, Optional[Coord]] = {start: None}
    while stack:
        cur = stack.pop()
        if cur == goal:
            return _reconstruct(came, goal)
        for nxt in neighbors(cur):
            if nxt not in came:
                came[nxt] = cur
                stack.append(nxt)
    return []

# Uniform-Cost Search

def ucs(start: Coord, goal: Coord, neighbors: NeighborsFn, cost: CostFn) -> List[Coord]:
    pq = _PQ()
    pq.push(0.0, start)
    came: Dict[Coord, Optional[Coord]] = {start: None}
    g: Dict[Coord, float] = {start: 0.0}

    while len(pq):
        cur = pq.pop()
        if cur == goal:
            return _reconstruct(came, goal)
        for nxt in neighbors(cur):
            step = cost(cur, nxt)
            cand = g[cur] + step
            if cand < g.get(nxt, float("inf")):
                g[nxt] = cand
                came[nxt] = cur
                pq.push(cand, nxt)
    return []

# A*

def astar(start: Coord, goal: Coord, neighbors: NeighborsFn, cost: CostFn, heuristic: HeuristicFn) -> List[Coord]:
    pq = _PQ()
    pq.push(0.0, start)
    came: Dict[Coord, Optional[Coord]] = {start: None}
    g: Dict[Coord, float] = {start: 0.0}

    while len(pq):
        cur = pq.pop()
        if cur == goal:
            return _reconstruct(came, goal)
        for nxt in neighbors(cur):
            step = cost(cur, nxt)
            cand = g[cur] + step
            if cand < g.get(nxt, float("inf")):
                g[nxt] = cand
                came[nxt] = cur
                f = cand + heuristic(nxt, goal)
                pq.push(f, nxt)
    return []
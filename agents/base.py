from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Tuple

Coord = Tuple[int, int]

class Agent(ABC):
    @abstractmethod
    def reset(self, start: Coord):
        ...

    @abstractmethod
    def plan(self) -> List[Coord]:
        ...

    @abstractmethod
    def step(self) -> Coord:
        ...
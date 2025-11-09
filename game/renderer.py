from __future__ import annotations
import pygame
from pygame import Surface
from typing import Iterable, Tuple, Set
from .. import colors as C

Coord = Tuple[int, int]

class Renderer:
    def __init__(self, width: int, height: int, tile: int = 32, margin: int = 0):
        self.width = width
        self.height = height
        self.tile = tile
        self.margin = margin
        self.screen: Surface | None = None

    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.width * self.tile + self.margin * 2,
             self.height * self.tile + self.margin * 2)
        )
        pygame.display.set_caption("Pacman – Search Agent")

    def _rect(self, p: Coord) -> pygame.Rect:
        x = self.margin + p[0] * self.tile
        y = self.margin + p[1] * self.tile
        return pygame.Rect(x, y, self.tile, self.tile)

    def _center(self, p: Coord) -> Tuple[int, int]:
        return (
            int(self.margin + (p[0] + 0.5) * self.tile),
            int(self.margin + (p[1] + 0.5) * self.tile),
        )

    def draw(
        self,
        walls: Set[Coord],
        goal: Coord,
        path: Iterable[Coord],
        current: Coord,
    ) -> None:
        assert self.screen is not None, "Renderer not initialized"
        self.screen.fill(C.gray)

        # Grid background
        for x in range(self.width):
            for y in range(self.height):
                rect = self._rect((x, y))
                color = C.dark_blue if (x, y) in walls else C.black
                pygame.draw.rect(self.screen, color, rect)

        # Goal
        pygame.draw.circle(self.screen, C.white, self._center(goal), self.tile // 4)

        # Planned path (thin outline)
        for p in path:
            pygame.draw.circle(self.screen, C.gray, self._center(p), 3)

        # Agent
        pygame.draw.circle(self.screen, C.yellow, self._center(current), self.tile // 4)

        pygame.display.flip()
from __future__ import annotations
from typing import Iterable, Tuple
import time
import pygame
from .renderer import Renderer
from ..environment import Environment
from ..agents import SearchAgent

Coord = Tuple[int, int]

class Game:
    def __init__(
        self,
        env: Environment,
        algorithm: str = "astar",
        heuristic: str = "manhattan",
        fps: int = 15,
        tile: int = 32,
        margin: int = 0,
    ) -> None:
        self.env = env
        self.agent = SearchAgent(env, algorithm=algorithm, heuristic=heuristic)
        self.renderer = Renderer(env.width, env.height, tile=tile, margin=margin)
        self.fps = fps
        self.current: Coord = env.start
        self.path: Iterable[Coord] = []

    def run(self) -> None:
        self.renderer.init()
        clock = pygame.time.Clock()

        # Plan once, then animate along the path
        self.path = self.agent.plan()
        if not self.path:
            print("No path found.")
        else:
            print(f"Planned path length: {len(self.path)}")

        idx = 0
        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            # Advance along the path
            if self.path:
                if idx < len(self.path):
                    self.current = self.path[idx]
                    idx += 1
                # Stop once goal reached
                if self.current == self.env.goal:
                    pass

            # Draw
            self.renderer.draw(self.env.walls, self.env.goal, self.path, self.current)

            # End if stuck at goal and fully shown
            if self.path and idx >= len(self.path) and self.current == self.env.goal:
                # Keep final frame visible but continue processing events
                # Limit the loop speed
                clock.tick(self.fps)
            else:
                clock.tick(self.fps)
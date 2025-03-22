import heapq
from typing import Optional
from pygame.math import Vector2
from .constants import Direction
from .entities import Entity
from .components import *
from .systems import MoveAndTeleportSystem


def manhattan_dst(x1: int, y1: int, x2: int, y2: int) -> int:
    return int(abs(x1 - x2) + abs(y1 - y2))


def euclidean_dst(x1: int, y1: int, x2: int, y2: int) -> float:
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** .5


class PathfindSystem:
    def __init__(self, game):
        self.game = game

    def get_moves(self, x: int, y: int) -> list[Direction, tuple[int, int]]:
        moves: list[Direction, tuple[int, int]] = []

        for direction in Direction:
            dx, dy = direction.value
            new_x, new_y = MoveAndTeleportSystem.get_next_pos(
                self.game, x, y, dx, dy, False
            )

            if (new_x, new_y) != (x, y):
                moves.append((direction, (new_x, new_y)))

        return moves

    def find(self):
        player = self.game.get_player()
        player_pos = player.get(PosComp)

        frontier = [(0, (player_pos.x, player_pos.y), [])]
        visited = set()

        while frontier:
            cost, (x, y), path = heapq.heappop(frontier)

            if (x, y) in visited:
                continue
            visited.add((x, y))

            for entity in self.game.entities.get_at(x, y):
                if entity.has(ConsumableComp):
                    return path
                
            for direction, (new_x, new_y) in self.get_moves(x, y):
                if (new_x, new_y) not in visited:
                    heapq.heappush(frontier, (cost + 1, (new_x, new_y), path + [direction.name]))

        return []

    # def estimate(self):
    #     player_pos = self.player.get(PosComp).pos
    #     est_fruit: tuple[float, Entity] = (float("inf"), None)

    #     for fruit in self.game.entities.get_by_comp(ConsumableComp):
    #         dst = manhattan_dst(fruit.get(PosComp).pos, player_pos)

    #         if dst < est_fruit[0]:
    #             est_fruit = (dst, fruit)

    #     return est_fruit

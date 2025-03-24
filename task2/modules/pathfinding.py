import heapq
from .constants import Direction, manhattan_dst
from .components import *
from .systems import MoveAndTeleportSystem


class PathfindSystem:
    def __init__(self, game):
        self.game = game

    def get_moves(self, x: int, y: int) -> list[Direction, tuple[int, int]]:
        moves: list[Direction, tuple[int, int]] = []

        for direction in Direction:
            dx, dy = direction.value
            new_x, new_y = MoveAndTeleportSystem.get_next_pos(
                self.game, x, y, dx, dy, any(
                    entity for entity in self.game.entities.get_at(x, y)
                    if entity.has(GhostComp) and entity.get(GhostComp).turns > 0
                )
            )

            if (new_x, new_y) != (x, y):
                moves.append((direction, (new_x, new_y)))

        return moves

    def find(self):
        player = self.game.get_player()
        player_pos = player.get(PosComp)

        frontier = [(
            self.estimate(player_pos.x, player_pos.y),
            (player_pos.x, player_pos.y),
            []
        )]
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
                    heapq.heappush(frontier, (
                        cost + self.estimate(new_x, new_y) + 1,
                        (new_x, new_y),
                        path + [direction.name]
                    ))

        return []

    def estimate(self, x: int, y: int) -> float:
        return 0  # Full UCS pathfinding

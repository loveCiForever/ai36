import heapq
from .common import Direction, manhattan_dst
from .components import *
from .systems import MoveAndTeleportSystem


class Pathfinder:
    def __init__(self, game):
        self.game = game

    def get_moves(self, x: int, y: int, ghost_turns: int) -> list[Direction, tuple[int, int], int]:
        moves: list[Direction, tuple[int, int], int] = []

        for direction in Direction:
            dx, dy = direction.value
            new_x, new_y, ghost_turns = MoveAndTeleportSystem.get_next_pos(
                self.game, x, y, dx, dy, ghost_turns, self.game.get_player().get(GhostComp).max_turns
            )

            if (new_x, new_y) != (x, y):
                moves.append((direction, (new_x, new_y), ghost_turns))

        return moves
    
    def find(self) -> list[str]:
        player = self.game.get_player()
        player_pos = player.get(PosComp)

        x, y = player_pos.x, player_pos.y
        pearls = [
            (pearl.get(PosComp).x, pearl.get(PosComp).y)
            for pearl in self.game.entities.get_by_name("pearl")
        ]
        full_path = []

        while pearls:
            path, x, y, pearls = self._find(x, y, pearls)
            full_path.extend(path)

        return full_path

    def _find(self, x: int, y: int, pearls: list[tuple[int, int]]) -> list[str]:
        frontier = [(
            self.estimate(x, y, pearls),
            0,
            (x, y),
            0,
            []
        )]
        visited = set()

        while frontier:
            f_cost, g_cost, (x, y), ghost_turns, path = heapq.heappop(frontier)

            if (x, y) in visited:
                continue
            visited.add((x, y))

            if (x, y) in pearls:
                return path, x, y, [pearl for pearl in pearls if pearl != (x, y)]
                
            for direction, (new_x, new_y), new_ghost_turn in self.get_moves(x, y, ghost_turns):
                if (new_x, new_y) in visited:
                    continue
            
                heapq.heappush(frontier, (
                    g_cost + self.estimate(new_x, new_y, pearls) + 1,
                    g_cost + 1,
                    (new_x, new_y),
                    new_ghost_turn,
                    path + [direction.name]
                ))

        return [], x, y, pearls

    def estimate(self, x: int, y: int, pearls: list[tuple[int, int]]) -> float:
        if not pearls:
            return 0
        
        return min(manhattan_dst(x, y, *pearl) for pearl in pearls)
from .components import *


class System:
    def __init__(self, game):
        self.game = game

    def update(self):
        ...


class MoveAndTeleportSystem(System):
    @classmethod
    def get_next_pos(cls, game, x: int, y: int, dx: int, dy: int, ghost_turns: int, max_ghost_turns: int) -> tuple[int, int, int]:        
        new_x = x + dx
        new_y = y + dy

        for other_entity in game.entities.get_by_comp(ObstacleComp):
            other_pos = other_entity.get(PosComp)

            if (other_pos.x, other_pos.y) == (new_x, new_y) and (
                not other_entity.get(ObstacleComp).ghostable
                or ghost_turns == 0
            ):
                return x, y, ghost_turns

        for portal in game.entities.get_by_comp(TeleportableComp):
            portal_pos = portal.get(PosComp)

            if (portal_pos.x, portal_pos.y) == (new_x, new_y):
                teleport = portal.get(TeleportableComp)
                new_x = teleport.tx
                new_y = teleport.ty
                break

        for entity in game.entities.get_at(new_x, new_y):
            if entity.has(PowerUpComp):
                ghost_turns = max_ghost_turns + 1

        if ghost_turns > 0:
            ghost_turns -= 1

        return new_x, new_y, ghost_turns

    def update(self):
        for entity in self.game.entities.get_by_comp(DirectionComp):
            pos = entity.get(PosComp)
            direction = entity.get(DirectionComp)

            if entity.has(GhostComp):
                ghost = entity.get(GhostComp)
                pos.x, pos.y, ghost.turns = self.get_next_pos(self.game,
                    pos.x, pos.y, direction.dx, direction.dy, ghost.turns, ghost.max_turns
                )
            else:
                pos.x, pos.y, _ = self.get_next_pos(self.game,
                    pos.x, pos.y, direction.dx, direction.dy, 0, 0
                )


class ConsumeSystem(System):
    def update(self) -> int:
        score = 0

        for entity in self.game.entities.get_by_comp(ConsumerComp):
            player_pos = entity.get(PosComp)

            for consumable in self.game.entities.get_by_comp(ConsumableComp):
                consumable_pos = consumable.get(PosComp)

                if (consumable_pos.x, consumable_pos.y) == (player_pos.x, player_pos.y):
                    score += consumable.get(ConsumableComp).points

                    if consumable.has(PowerUpComp) and entity.has(GhostComp):
                        ghost = entity.get(GhostComp)
                        ghost.turns = ghost.max_turns

                    self.game.entities.remove(consumable)
        
        return score

from .components import *


class System:
    def update(self, game):
        ...


class MoveAndCollideSystem(System):
    """Not to be confused with Godot's move_and_collide() :P"""
    def update(self, game):
        for entity in game.entities.get_by_comp(MoveableComp):
            pos_comp = entity.get(PosComp)
            direction_comp = entity.get(MoveableComp)

            new_pos = direction_comp.move(pos_comp.pos)

            if not any(
                other_entity for other_entity in game.entities.get_by_comp(ObstacleComp)
                if other_entity.get(PosComp).pos == new_pos
                   and (
                       not other_entity.get(ObstacleComp).ghostable
                       or (
                           entity.has(GhostComp)
                           and not entity.get(GhostComp).is_active()
                       )
                   )
            ):
                pos_comp.pos = new_pos


class TeleportSystem(System):
    def update(self, game):
        for entity in game.entities.get_by_comp(MoveableComp):

            pos_comp = entity.get(PosComp)
            portal = [entity for entity in game.entities.get_by_comp(TeleportableComp)
                      if entity.get(PosComp).pos == pos_comp.pos]
            
            if any(portal):
                pos_comp.pos = portal[0].get(TeleportableComp).teleport_pos


class ConsumeSystem(System):
    def update(self, game) -> int:
        score = 0

        for entity in game.entities.get_by_comp(ConsumerComp):
            pos = entity.get(PosComp).pos
            consumables = [entity for entity in game.entities.get_by_comp(ConsumableComp)
                           if entity.get(PosComp).pos == pos]

            for consumable in consumables:
                score += consumable.get(ConsumableComp).points

                if consumable.has(PowerUpComp) and entity.has(GhostComp):
                    entity.get(GhostComp).activate()

                game.entities.remove(consumable)
        
        return score
    

class GhostSystem(System):
    def update(self, game) -> bool:
        for entity in game.entities.get_by_comp(GhostComp):
            ghost_comp = entity.get(GhostComp)

            ghost_comp.use()

            return ghost_comp.is_active()
            
        return False

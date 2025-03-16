from modules.entities import Entity
from .components import ConsumableComponent, ConsumerComponent, MoveableComponent, NameComponent, PositionComponent, TeleportableComponent


class System:
    def update(self, entities: list[Entity]):
        ...


class MoveAndCollideSystem(System):
    """Not to be confused with Godot's move_and_collide() :P"""
    def update(self, entities: list[Entity]):
        for entity in entities:
            if not entity.has_component(MoveableComponent):
                continue

            position_component = entity.get_component(PositionComponent)
            direction_component = entity.get_component(MoveableComponent)

            new_position = direction_component.move(position_component.position)

            if any(
                other_entity
                for other_entity in entities
                if other_entity.get_component(NameComponent).name == "wall"
                and other_entity.get_component(PositionComponent).position == new_position
            ):
                continue

            position_component.position = new_position


class TeleportSystem(System):
    def update(self, entities: list[Entity]):
        for entity in entities:
            if not entity.has_component(MoveableComponent) \
               or not entity.has_component(TeleportableComponent):
                continue

            position_component = entity.get_component(PositionComponent)
            teleportable_component = entity.get_component(TeleportableComponent)
            teleport_points = teleportable_component.teleport(position_component.position)

            if len(teleport_points) != 0:
                position_component.position = teleport_points


class ConsumeSystem(System):
    def update(self, entities: list[Entity]):
        for entity in entities:
            if entity.has_component(ConsumerComponent):
                position = entity.get_component(PositionComponent).position
                consumables = [
                    entity for entity in entities
                    if entity.has_component(ConsumableComponent)
                    and entity.get_component(PositionComponent).position == position
                ]

                for consumable in consumables:
                    print(f"Score {consumable.get_component(ConsumableComponent).points} pts!")
                    entities.remove(consumable)

from typing import Optional, Type
from .components import *


class Entity:
    def __init__(self):
        self.comps = {}

    def add(self, comp: Comp):
        self.comps[type(comp)] = comp

    def get(self, comp_type: Type[Comp]) -> Optional[Comp]:
        return self.comps.get(comp_type)

    def has(self, comp_type: Type[Comp]) -> bool:
        return comp_type in self.comps
    

class EntityCollection:
    _SORT_ORDERS = {
        "portal": 0,
        "wall": 1,
        "fruit": 2,
        "magical_pie": 3,
        "player": 4
    }

    def __init__(self, entities: list[Entity] = None):
        self.entities = entities or []

    def add(self, name: str, pos: tuple[int, int], comps: list[Comp]) -> Entity:
        entity = Entity()

        entity.add(NameComp(name))
        entity.add(PosComp(*pos))

        for comp in comps:
            entity.add(comp)

        self.entities.append(entity)

        return entity
    
    def remove(self, entity: Entity):
        self.entities.remove(entity)

    def get_all(self) -> list[Entity]:
        return self.entities

    def get_by_comp(self, comp_type: Type[Comp]) -> list[Entity]:
        return [entity for entity in self.entities
                if entity.has(comp_type)]

    def get_by_name(self, name: str) -> list[Entity]:
        return [entity for entity in self.get_by_comp(NameComp)
                if entity.get(NameComp).name == name]
    
    def get_by_pos(self, x: int, y: int) -> list[Entity]:
        return [entity for entity in self.get_by_comp(PosComp)
                if tuple(entity.get(PosComp).pos) == (x, y)]
    
    def _sort(self):
        self.entities.sort(key=lambda entity: self._SORT_ORDERS[entity.get(NameComp).name])

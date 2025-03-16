from typing import Optional, Type
from .components import Component


class Entity:
    def __init__(self):
        self.components = {}

    def add_component(self, component: Component):
        self.components[type(component)] = component

    def get_component(self, component_type: Type[Component]) -> Optional[Component]:
        return self.components.get(component_type)

    def has_component(self, component_type: Type[Component]) -> bool:
        return component_type in self.components

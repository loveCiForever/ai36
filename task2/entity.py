from typing import Type
from components import Component


class Entity:
    """Base entity class. Must be created as an instance
    instead of inheriting the class itself."""

    def __init__(self):
        self.components = {}

    def add_component(self, component: Component):
        self.components[type(component)] = component

    def get_component(self, component_type: Type[Component]) -> Component:
        return self.components[component_type]

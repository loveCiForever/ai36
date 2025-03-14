class Component:
    """Base class for all components."""
    ...


class PositionComponent(Component):
    """Handles positioning of the entity."""

    def __init__(self, x: int = 0, y: int = 0):
        self.x, self.y = x, y


class MoveableComponent(Component):
    """Allows the entity to move."""

    def __init__(self):
        self.dx, self.dy = 0, 0


class ConsumableComponent(Component):
    """Allows the entity to be consumed."""

    def __init__(self, points: int = 1):
        self.points = points


class TypeComponent(Component):
    """Assigns an ASCII or Unicode character to the entity."""

    def __init__(self, char: str):
        assert len(char) == 1
        self.char = char

class Component:
    """Base class for all components."""
    ...


class PositionComponent(Component):
    """Handles positioning of entities."""
    def __init__(self, x: int=0, y: int=0):
        self.x, self.y = x, y


class MoveableComponent(Component):
    """Allows entities to be moved."""
    def __init__(self):
        self.dx, self.dy = 0, 0


class ConsumableComponent(Component):
    """Allow entities to be consumed."""
    def __init__(self, points: int=1):
        self.points = points

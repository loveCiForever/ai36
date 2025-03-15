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


class PowerUpComponent(Component):
    """Allows the entity to go through walls for a limited number of turns."""

    def __init__(self, max_turns: int = 5):
        self.max_turns = max_turns
        self.remaining_turns = 0

    def trigger_power_up(self):
        self.remaining_turns = self.max_turns

    def use_turn(self) -> bool:
        if self.remaining_turns > 0:
            self.remaining_turns -= 1
            return True

        return False

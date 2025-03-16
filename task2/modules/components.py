import pygame


class Component:
    ...


class NameComponent(Component):
    def __init__(self, name: str):
        self.name = name


class SpriteComponent(Component):
    def __init__(self, texture_atlas: pygame.Surface, sprite_x: int, sprite_y: int, tile_size: int):
        self.sprite = texture_atlas.subsurface((
            sprite_x * tile_size, sprite_y * tile_size, *[tile_size] * 2
        ))


class PositionComponent(Component):
    def __init__(self, x: int = 0, y: int = 0):
        self.position = pygame.math.Vector2(x, y)


class MoveableComponent(Component):
    def __init__(self, dx: int = 0, dy: int = 0):
        self.direction = pygame.math.Vector2(dx, dy)

    def move(self, position: pygame.math.Vector2) -> pygame.math.Vector2:
        return position + self.direction


class TeleportableComponent(Component):
    def __init__(self, teleport_points: list[pygame.math.Vector2]):
        self.teleport_points = teleport_points

    def teleport(self, position: pygame.math.Vector2) -> pygame.math.Vector2:
        try:
            index = self.teleport_points.index(position)
            return self.teleport_points[(index + 2) % len(self.teleport_points)]
        except ValueError:
            return tuple()


class ConsumerComponent(Component):
    ...


class ConsumableComponent(Component):
    def __init__(self, points: int):
        self.points = points

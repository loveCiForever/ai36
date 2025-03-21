import pygame


class Comp:
    ...


class NameComp(Comp):
    def __init__(self, name: str):
        self.name = name


class SpriteComp(Comp):
    def __init__(self, texture_atlas: pygame.Surface, sprite_x: int, sprite_y: int, tile_size: int):
        self.sprite = texture_atlas.subsurface((
            sprite_x * tile_size, sprite_y * tile_size, *[tile_size] * 2
        ))


class PosComp(Comp):
    def __init__(self, x: int = 0, y: int = 0):
        self.pos = pygame.math.Vector2(x, y)


class MoveableComp(Comp):
    def __init__(self, dx: int = 0, dy: int = 0):
        self.direction = pygame.math.Vector2(dx, dy)

    def move(self, pos: pygame.math.Vector2) -> pygame.math.Vector2:
        return pos + self.direction


class TeleportableComp(Comp):
    def __init__(self, teleport_pos: tuple[int, int]):
        self.teleport_pos = pygame.math.Vector2(teleport_pos)


class ConsumerComp(Comp):
    ...


class ConsumableComp(Comp):
    def __init__(self, points: int):
        self.points = points

    
class PowerUpComp(Comp):
    ...


class GhostComp(Comp):
    def __init__(self, max_turns: int):
        self.max_turns = max_turns
        self.turns = 0

    def activate(self):
        self.turns = self.max_turns

    def use(self):
        if self.is_active():
            self.turns -= 1
            
    def is_active(self) -> bool:
        return self.turns > 0


class ObstacleComp:
    def __init__(self, ghostable: bool=False):
        self.ghostable = ghostable

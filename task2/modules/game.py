import pygame
from enum import Enum
from .entities import Entity
from .components import MoveableComponent, PositionComponent, SpriteComponent, NameComponent, TeleportableComponent, ConsumableComponent, ConsumerComponent
from .systems import MoveAndCollideSystem, TeleportSystem, ConsumeSystem

TILE_SIZE = 16
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Game:
    def __init__(self, map_width: int, map_height: int):
        pygame.init()

        self.map_width = map_width
        self.map_height = map_height

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.texture_atlas = pygame.image.load("assets/texture_atlas.png").convert_alpha()

        self.entities: list[Entity] = []

        self.move_and_collide_system = MoveAndCollideSystem()
        self.teleport_system = TeleportSystem()
        self.consume_system = ConsumeSystem()

        self.delta_time = 0

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def update(self):
        if self.delta_time >= .5:
            self.move_and_collide_system.update(self.entities)
            self.teleport_system.update(self.entities)
            self.consume_system.update(self.entities)

            self.delta_time = 0

    def render(self):
        self.screen.fill(pygame.Color("black"))

        for entity in self.entities:
            position = entity.get_component(PositionComponent).position

            if entity.has_component(SpriteComponent):
                self.screen.blit(
                    entity.get_component(SpriteComponent).sprite,
                    (position.x * TILE_SIZE, position.y * TILE_SIZE)
                )

        pygame.display.flip()

    def add_entity(self, entity: Entity):
        self.entities.append(entity)

    def run(self):
        while self.is_running:
            self.delta_time += self.clock.tick(60) / 1000
            self.handle_input()
            self.update()
            self.render()


def load_game(map_data: str) -> Game:
    map_data = map_data.split("\n")

    game = Game(
        map_width=len(map_data[0]),
        map_height=len(map_data)
    )

    for y, row in enumerate(map_data):
        for x, char in enumerate(row):
            if char != " ":
                entity = Entity()
                entity.add_component(PositionComponent(x, y))

                match (char):
                    case "%":
                        entity.add_component(NameComponent("wall"))
                        entity.add_component(SpriteComponent(game.texture_atlas, 3, 0, TILE_SIZE))

                    case "P":
                        entity.add_component(NameComponent("player"))
                        entity.add_component(SpriteComponent(game.texture_atlas, 0, 0, TILE_SIZE))
                        entity.add_component(MoveableComponent(Direction.LEFT.value))
                        entity.add_component(TeleportableComponent([
                            pygame.math.Vector2(1, 1),
                            pygame.math.Vector2(game.map_width - 2, 1),
                            pygame.math.Vector2(game.map_width - 2, game.map_height - 2),
                            pygame.math.Vector2(1, game.map_height - 2)
                        ]))
                        entity.add_component(ConsumerComponent())

                    case ".":
                        entity.add_component(NameComponent("fruit"))
                        entity.add_component(SpriteComponent(game.texture_atlas, 1, 0, TILE_SIZE))
                        entity.add_component(ConsumableComponent(10))

                    case "O":
                        entity.add_component(NameComponent("magical_pie"))
                        entity.add_component(SpriteComponent(game.texture_atlas, 2, 0, TILE_SIZE))
                        entity.add_component(ConsumableComponent(100))

                game.add_entity(entity)

    return game

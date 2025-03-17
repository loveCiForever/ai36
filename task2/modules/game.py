import pygame
from enum import Enum
from .entities import Entity
from .components import MoveableComponent, PositionComponent, SpriteComponent, NameComponent, TeleportableComponent, ConsumableComponent, ConsumerComponent
from .systems import MoveAndCollideSystem, TeleportSystem, ConsumeSystem

TILE_SIZE = 16
WINDOW_WIDTH, WINDOW_HEIGHT = 960, 540


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


keybindings = {
    pygame.K_w: Direction.UP,
    pygame.K_s: Direction.DOWN,
    pygame.K_a: Direction.LEFT,
    pygame.K_d: Direction.RIGHT
}


class Game:
    def __init__(self, map_width: int, map_height: int):
        pygame.init()

        self.map_width = map_width
        self.map_height = map_height

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.surface = pygame.Surface((map_width * TILE_SIZE, map_height * TILE_SIZE))

        self.clock = pygame.time.Clock()
        self.is_running = True

        self.texture_atlas = pygame.image.load("assets/texture_atlas.png").convert_alpha()

        self.entities: list[Entity] = []

        self.move_and_collide_system = MoveAndCollideSystem()
        self.teleport_system = TeleportSystem()
        self.consume_system = ConsumeSystem()

        self.delta_time = 0

        self.score = 0
        self.path_taken = 0

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            if event.type == pygame.KEYDOWN:
                player = [entity for entity in self.entities
                          if entity.get_component(NameComponent).name == "player"][0]
                direction_component = player.get_component(MoveableComponent)

                if event.key in keybindings.keys():
                    direction_component.direction = keybindings[event.key].value

    def update(self):
        if self.delta_time >= .2:
            self.move_and_collide_system.update(self.entities)
            self.teleport_system.update(self.entities)
            
            self.score += self.consume_system.update(self.entities)

            self.delta_time = 0
            self.path_taken += 1

    def render(self):
        self.screen.fill(pygame.Color("black"))
        self.surface.fill(pygame.Color("black"))

        for entity in self.entities:
            position = entity.get_component(PositionComponent).position

            if entity.has_component(SpriteComponent):
                sprite = entity.get_component(SpriteComponent).sprite

                if entity.has_component(MoveableComponent):
                    direction = entity.get_component(MoveableComponent).direction
                    sprite = pygame.transform.rotate(
                        pygame.transform.flip(sprite, direction[0] == 1, False),
                        90 * direction[1]
                    )
                
                self.surface.blit(sprite,
                    (position.x * TILE_SIZE, position.y * TILE_SIZE)
                )

        scaled_surface = pygame.transform.scale_by(self.surface,
            WINDOW_WIDTH / (self.map_width * TILE_SIZE)
        )
        self.screen.blit(scaled_surface, (0, WINDOW_HEIGHT - scaled_surface.get_size()[1]))

        font = pygame.font.Font(None, 32)
        hud_info = f"Score: {self.score}    Path taken: {self.path_taken}"
        text_surface = font.render(hud_info, True, pygame.Color("white"))
        self.screen.blit(text_surface, (20, 20))

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

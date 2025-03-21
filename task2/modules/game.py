import pygame
from typing import Self
from enum import Enum
from .entities import Entity, EntityCollection
from .components import *
from .systems import *

TILE_SIZE = 64
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720


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
    def __init__(self, title: str, width: int, height: int):
        pygame.init()
        pygame.display.set_caption(title)

        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.surface = pygame.Surface((width * TILE_SIZE, height * TILE_SIZE))

        self.clock = pygame.time.Clock()
        self.is_running = True

        self.texture_atlas = pygame.image.load("assets/texture_atlas.png").convert_alpha()

        self.entities = EntityCollection()

        self.systems = {
            system: (system(), None) for system in [
                MoveAndCollideSystem,
                TeleportSystem,
                ConsumeSystem,
                GhostSystem
            ]
        }

        self.delta_time = 0

        self.score = 0
        self.path_taken = 0

        self.is_ghosting = False

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            if event.type == pygame.KEYDOWN:
                player = [entity for entity in self.entities.get_all()
                          if entity.get(NameComp).name == "player"][0]
                direction_component = player.get(MoveableComp)

                if event.key in keybindings.keys():
                    direction_component.direction = keybindings[event.key].value

    def update(self):
        if self.delta_time >= .2 and not self.is_losing():
            for system_type, (system, _) in self.systems.items():
                self.systems[system_type] = system, system.update(self)

            self.score += self.systems[ConsumeSystem][1]
            self.is_ghosting = self.systems[GhostSystem][1]
            
            self.delta_time = 0
            self.path_taken += 1

    def get_player(self) -> Entity:
        return self.entities.get_by_name("player")[0]

    def is_winning(self) -> bool:
        return not any(self.entities.get_by_comp(ConsumableComp))
    
    def is_losing(self) -> bool:
        player_pos = self.get_player().get(PosComp).pos
        return not self.is_ghosting and any(
            entity for entity in self.entities.get_by_comp(ObstacleComp)
            if entity.get(PosComp).pos == player_pos
        )

    def render(self):
        self.screen.fill(pygame.Color("black"))
        self.surface.fill(pygame.Color("steelblue"))

        for entity in self.entities.get_all():
            pos = entity.get(PosComp).pos
            sprite = entity.get(SpriteComp).sprite

            if entity.has(MoveableComp):
                direction = entity.get(MoveableComp).direction
                sprite = pygame.transform.rotate(
                    pygame.transform.flip(sprite, direction[0] == 1, False),
                    90 * direction[1]
                )

            if entity.has(ObstacleComp):
                sprite.set_alpha(
                    128 if entity.get(ObstacleComp).ghostable
                        and self.is_ghosting
                    else 255
                )
            
            self.surface.blit(sprite, (pos.x * TILE_SIZE, pos.y * TILE_SIZE))

        scaled_surface = pygame.transform.smoothscale_by(self.surface,
            WINDOW_WIDTH / (self.width * TILE_SIZE)
        )

        self.screen.blit(scaled_surface, (0, WINDOW_HEIGHT - scaled_surface.get_size()[1]))

        font = pygame.font.Font(None, 32)
        hud_info = f"Score: {self.score}    Path taken: {self.path_taken}    {"POWER UP!" if self.is_ghosting else ""}"
        text_surface = font.render(hud_info, True, pygame.Color("white"))
        self.screen.blit(text_surface, (20, (WINDOW_HEIGHT - scaled_surface.get_size()[1] - text_surface.get_size()[1]) / 2))

        pygame.display.flip()

    def run(self):
        while self.is_running:
            self.delta_time += self.clock.tick(60) / 1000
            self.handle_input()
            self.update()
            self.render()

    @classmethod
    def load_from_map(cls, title: str, map_data: str) -> Self:
        map_data = map_data.split("\n")

        game = cls(title, len(map_data[0]), len(map_data))

        portals = [
            (1, 1),
            (game.width - 2, 1),
            (game.width - 2, game.height - 2),
            (1, game.height - 2)
        ]

        for i, pos in enumerate(portals):
            game.entities.add("portal", pos, [
                SpriteComp(game.texture_atlas, 1, 0, TILE_SIZE),
                TeleportableComp(portals[(i + 2) % 4])
            ])

        for y, row in enumerate(map_data):
            for x, char in enumerate(row):
                if char != " ":
                    name: str
                    sprite_pos: tuple[int, int]
                    comps: list[Comp]

                    match (char):
                        case "%":
                            is_inside = x == 0 or x == game.width - 1 \
                                        or y == 0 or y == game.height - 1

                            name = "wall"
                            sprite_pos = 0, 0
                            comps = [ObstacleComp(ghostable=not is_inside)]

                        case "P":
                            name = "player"
                            sprite_pos = 2, 0
                            comps = [
                                MoveableComp(Direction.LEFT.value),
                                GhostComp(5),
                                ConsumerComp()
                            ]

                        case ".":
                            name = "fruit"
                            sprite_pos = 0, 1
                            comps = [ConsumableComp(10)]

                        case "O":
                            name = "magical_pie"
                            sprite_pos = 1, 1
                            comps = [
                                ConsumableComp(100),
                                PowerUpComp()
                            ]

                    game.entities.add(name, (x, y), [
                        SpriteComp(game.texture_atlas, *sprite_pos, TILE_SIZE),
                        *comps
                    ])

        game.entities._sort()

        return game

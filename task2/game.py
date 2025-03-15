from entity import Entity
from components import \
    PositionComponent, MoveableComponent, TypeComponent, \
    ConsumableComponent, PowerUpComponent


class Game:
    def __init__(self, width: int, height: int):
        self.entities = []
        self.width = width
        self.height = height

    def add_entity(self, entity: Entity):
        self.entities.append(entity)

    def __repr__(self) -> str:
        grid = [["" for _ in range(self.height)] for _ in range(self.width)]

        for entity in self.entities:
            position = entity.get_component(PositionComponent)
            ctype = entity.get_component(TypeComponent)

            if position and ctype:
                grid[position.y][position.x] = ctype.char

        return "\n".join("".join(row) for row in grid) + "\n"

    def __str__(self) -> str:
        return (f"Game#{hash(self)}["
                f"size=({self.width}, {self.height})"
                f", num_entities={len(self.entities)}"
                "]")


def load_from_map(map_data: str) -> Game:
    map_data = map_data.strip().split("\n")
    game = Game(width=len(map_data), height=len(map_data[0]))

    for y, row in enumerate(map_data):
        for x, char in enumerate(row):
            entity = Entity()
            entity.add_component(PositionComponent(x, y))
            entity.add_component(TypeComponent(char))

            match(char):
                case "P":
                    entity.add_component(MoveableComponent())
                    entity.add_component(PowerUpComponent())

                case ".":
                    entity.add_component(ConsumableComponent())

                case "O":
                    entity.add_component(ConsumableComponent())

            game.add_entity(entity)

    return game

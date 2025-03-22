from modules.game import Game

TITLE = "Wilbur's Wavy Waters"


def main():
    with open("input.txt") as map_file:
        map_data = map_file.read()

        game = Game.load_from_map(TITLE, map_data)

        print(game.pathfinder.find())

        game.run()


if __name__ == "__main__":
    main()

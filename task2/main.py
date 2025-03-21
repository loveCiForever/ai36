from modules.game import Game


def main():
    with open("input.txt") as map_file:
        map_data = map_file.read()

        game = Game.load_from_map(map_data)
        game.run()


if __name__ == "__main__":
    main()

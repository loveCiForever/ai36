from modules.game import load_game


def main():
    with open("input.txt") as map_file:
        map_data = map_file.read()

        game = load_game(map_data)
        game.run()


if __name__ == "__main__":
    main()

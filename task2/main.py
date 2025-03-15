from game import load_from_map


def main():
    with open("input.txt") as map_file:
        map_data = map_file.read()
        game = load_from_map(map_data)

        print(repr(game))


if __name__ == "__main__":
    main()

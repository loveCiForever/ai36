import time
from itertools import groupby
from modules import Game, Pathfinder

TITLE = "Wilbur's Wavy Waters"


def main():
    with open("input.txt") as map_file:
        map_data = map_file.read()
        game = Game.load_from_map(TITLE, map_data)

        pathfinder = Pathfinder(game)

        print("\nComputing path, please wait...")

        pathfind_time = time.time()
        path = pathfinder.find()
        pathfind_duration = time.time() - pathfind_time

        print(
            f"\n{"Pathfinding complete!":^80}\n{"=" * 80}",
            f"\nPathfind duration: {pathfind_duration:.2f}s",
            f"\nPath: {" ".join(f"{len(list(group))}{direction[0]}" for direction, group in groupby(path))}"
        )

        with open("output.txt", "w+") as output_file:
            output_file.writelines([
                "Step | Direction\n",
                "-----|----------\n",
                *[f" {i + 1:<3} |  {direction:<8}\n" for i, direction in enumerate(path)]
            ])

            print("\nPath has been written to \"output.txt\".")

        game.run(path)


if __name__ == "__main__":
    main()

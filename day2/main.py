import dataclasses
import typing as t
from pathlib import Path

FILE_DIR = Path(__file__).parent.resolve()


@dataclasses.dataclass(slots=True, frozen=True)
class Set:
    blue: int
    green: int
    red: int


@dataclasses.dataclass
class Game:
    idx: int
    game_sets: t.List[Set]

    def blues(self):
        return [game_set.blue for game_set in self.game_sets]

    def greens(self):
        return [game_set.green for game_set in self.game_sets]

    def reds(self):
        return [game_set.red for game_set in self.game_sets]


def get_input():
    with open(FILE_DIR / "input.txt", "r") as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def parse_input(input_lines: t.List[str]) -> t.List[Game]:
    games = []
    for line in input_lines:
        game, game_sets = line.split(":")
        # Get game number
        game_number = int(game.split()[1])
        # Get sets
        game_sets = game_sets.split(";")
        game_sets = [str_to_game_set(game_set) for game_set in game_sets]
        games.append(Game(idx=game_number, game_sets=game_sets))
    return games


def str_to_game_set(input_str: str) -> Set:
    blue, green, red = 0, 0, 0
    colour_sets = input_str.split(",")
    for colour_set in colour_sets:
        val, colour = colour_set.split()
        match colour:
            case "blue":
                blue = int(val)
            case "green":
                green = int(val)
            case "red":
                red = int(val)
    return Set(blue=blue, green=green, red=red)


def is_game_valid(game: Game, comparison_game_set: Set) -> bool:
    if (
        all(val <= comparison_game_set.blue for val in game.blues())
        and all(val <= comparison_game_set.green for val in game.greens())
        and all(val <= comparison_game_set.red for val in game.reds())
    ):
        return True
    return False


def day1(games: t.List[Game], comparison_game_set: Set):
    valid_games = filter(lambda game: is_game_valid(game, comparison_game_set), games)
    return sum([game.idx for game in valid_games])


def day2(games: t.List[Game]):
    powers = [
        max(game.blues()) * max(game.greens()) * max(game.reds()) for game in games
    ]
    return sum(powers)


if __name__ == "__main__":
    input_data = get_input()
    parsed_input = parse_input(input_data)
    print(day1(parsed_input, Set(blue=14, green=13, red=12)))
    print(day2(parsed_input))

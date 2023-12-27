import dataclasses
import re
import typing as t
from pathlib import Path

import numpy as np

FILE_DIR = Path(__file__).parent.resolve()
DIGIT_REGEX = r"(\d+)"


@dataclasses.dataclass
class PartNumber:
    val: int
    row: int
    col_start: int
    col_end: int


def get_input():
    with open(FILE_DIR / "input.txt", "r") as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def parse_input(
    input_lines: t.List[str],
) -> t.Tuple[t.List[PartNumber], t.List[t.List[str]]]:
    partnumbers = []
    for idx, line in enumerate(input_lines):
        matchs = re.finditer(DIGIT_REGEX, line)
        for match in matchs:
            partnumbers.append(
                PartNumber(
                    val=int(match.group()),
                    row=idx,
                    col_start=match.span()[0],
                    col_end=match.span()[1] - 1,
                )
            )

    return (partnumbers, [list(line) for line in input_lines])


def check_is_symbol(char_to_check: str):
    if char_to_check != "." and not char_to_check.isdigit():
        return True
    return False


check_is_asterisk = lambda x: x == "*"


def check_adj(
    partnumber: PartNumber, schematic: t.List[t.List[str]], check_func: t.Callable
):
    indexes_to_try = [  # left and right
        (partnumber.row, partnumber.col_start - 1),
        (partnumber.row, partnumber.col_end + 1),
    ]
    indexes_above = [
        (partnumber.row - 1, x)
        for x in range(partnumber.col_start - 1, partnumber.col_end + 2)
    ]
    indexes_below = [
        (partnumber.row + 1, x)
        for x in range(partnumber.col_start - 1, partnumber.col_end + 2)
    ]
    indexes_to_try.extend(indexes_above)
    indexes_to_try.extend(indexes_below)
    # filter the indexes
    indexes_to_try = filter(
        lambda x: x[0] >= 0 and x[0] <= len(schematic) - 1, indexes_to_try
    )  # filter rows
    indexes_to_try = filter(
        lambda x: x[1] >= 0 and x[1] <= len(schematic[0]) - 1, indexes_to_try
    )  # filter columns
    checked_indexes = map(
        lambda x: (check_func(schematic[x[0]][x[1]]), x), indexes_to_try
    )
    valid_indexes = [x for x in checked_indexes if x[0] is True]
    if any(valid_indexes):
        return True, [x[1] for x in valid_indexes]
    return False, []


def day1(partnumbers: t.List[PartNumber], schematic: t.List[t.List[str]]):
    # check adjacent is not a '.' or digit
    valid = []
    for partnumber in partnumbers:
        checked = check_adj(partnumber, schematic, check_is_symbol)
        if checked[0]:
            valid.append(partnumber.val)
    return sum(valid)


def day2(partnumbers: t.List[PartNumber], schematic: t.List[t.List[str]]):
    valid = {}
    gear_sum = 0
    for partnumber in partnumbers:
        checked, coords = check_adj(partnumber, schematic, check_is_symbol)
        if checked:
            for coord in coords:
                if valid.get(coord):
                    valid[coord].append(partnumber.val)
                else:
                    valid[coord] = [partnumber.val]
    for val in valid.values():
        if len(val) == 2:
            gear_sum += val[0] * val[1]
    return gear_sum


if __name__ == "__main__":
    input_data = get_input()
    parsed_input = parse_input(input_data)
    print(day1(*parsed_input))
    print(day2(*parsed_input))

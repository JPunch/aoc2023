import typing as t
from pathlib import Path


FILE_DIR = Path(__file__).parent.resolve()


def get_input():
    with open(FILE_DIR / "test_input.txt", "r") as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def parse_input(
    input_lines: t.List[str],
) -> t.List[t.Tuple[int, t.List[int], t.List[int]]]:
    lines = []
    for line in input_lines:
        card = line.split(":")
        card_num = int(card[0].split()[1])
        winning, numbers = card[1].split("|")
        lines.append(
            (
                card_num,
                [int(x) for x in winning.strip().split()],
                [int(x) for x in numbers.strip().split()],
            )
        )
    return lines


def day1(cards: t.List[t.Tuple[int, t.List[int], t.List[int]]]):
    # 2 ** len(matches) - 1
    points = 0
    for _, winning, numbers in cards:
        winning_numbers = [x for x in numbers if x in winning]
        if winning_numbers:
            points += 2 ** (len(winning_numbers) - 1)
    return points


def day2(cards: t.List[t.Tuple[int, t.List[int], t.List[int]]]):
    card_dict = {i: 1 for i in range(1, len(cards) + 1)}
    for card_num, winning, numbers in cards:
        winning_numbers = [x for x in numbers if x in winning]
        if winning_numbers:
            for i in range(1, len(winning_numbers) + 1):
                if (card_val := card_dict.get(card_num + i)):
                    card_dict[card_num + i] += card_dict[card_num]
    return sum(card_dict.values())


if __name__ == "__main__":
    input_data = get_input()
    parsed_input = parse_input(input_data)
    print(day1(parsed_input))
    print(day2(parsed_input))

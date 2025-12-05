import bisect
from typing import Any

from aoc.puzzle import PuzzleInput


def parse_input(puzzle: PuzzleInput) -> tuple[list[tuple[int, int]], list[int]]:
    top, bottom = puzzle.raw.strip().split("\n\n")
    ranges = []
    for line in top.splitlines():
        left, right = line.split("-", maxsplit=1)
        ranges.append((int(left), int(right)))

    fruit = []
    for line in bottom.splitlines():
        fruit.append(int(line))

    return ranges, fruit


def part_1(puzzle: PuzzleInput) -> Any:
    ranges, fruits = parse_input(puzzle=puzzle)
    range_starts = sorted([r[0] for r in ranges])
    range_ends = sorted([r[1] for r in ranges])
    a = [(r, 1) for r in range_starts]
    b = [(r, -1) for r in range_ends]
    c = sorted(a + b, key=lambda x: x[0])

    current = 0
    numberline = []
    for point, movement in c:
        current += movement
        numberline.append((point, current))

    total = 0
    for fruit in fruits:
        i = bisect.bisect_left(c, fruit, key=lambda x: x[0])
        if i:
            point, movement = numberline[i - 1]
            if movement > 0:
                total += 1

    return total


def part_2(puzzle: PuzzleInput) -> Any:
    ranges, _ = parse_input(puzzle=puzzle)
    range_starts = sorted([r[0] for r in ranges])
    range_ends = sorted([r[1] for r in ranges])
    a = [(r, 1) for r in range_starts]
    b = [(r, -1) for r in range_ends]
    c = sorted(a + b, key=lambda x: x[0])

    total = 0
    current = 0
    last_num = 0
    numberline = []
    for point, movement in c:
        if current == 0:
            last_num = point
        current += movement
        if current == 0:
            total += point - last_num
            total += 1
        numberline.append((point, current))

    return total


# I scored roughly 1656 globally

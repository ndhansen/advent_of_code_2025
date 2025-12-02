from typing import Any

from aoc.puzzle import PuzzleInput


def parse_input(puzzle: PuzzleInput) -> list[tuple[int, int]]:
    line = puzzle.raw.strip()
    pieces = line.split(",")
    ranges = []
    for piece in pieces:
        left, right = piece.split("-")
        ranges.append((int(left), int(right)))
    return ranges


def part_1(puzzle: PuzzleInput) -> Any:
    ranges = parse_input(puzzle)
    total = 0
    for start, stop in ranges:
        for i in range(start, stop + 1):
            x = str(i)
            if len(x) % 2 == 0 and x[: (len(x) // 2)] == x[(len(x) // 2) :]:
                total += i
    return total


def is_repeating(number: str) -> bool:
    for i in range(1, (len(number) // 2) + 1):
        start = number[:i]
        remainder = number[i:]
        while remainder.startswith(start):
            remainder = remainder[i:]
        if remainder == "":
            return True
    return False


def part_2(puzzle: PuzzleInput) -> Any:
    ranges = parse_input(puzzle)
    total = 0
    for start, stop in ranges:
        for i in range(start, stop + 1):
            x = str(i)
            if is_repeating(x):
                total += i
    return total

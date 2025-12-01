from typing import Any

from aoc.puzzle import PuzzleInput


def part_1(puzzle: PuzzleInput) -> Any:
    total = 0
    dial = 50
    for line in puzzle.lines:
        direction = line[0]
        count = int(line[1:])
        if direction == "L":
            dial -= count
        if direction == "R":
            dial += count
        if dial < 0 or dial > 99:
            dial %= 100
        if dial == 0:
            total += 1
    return total


def part_2(puzzle: PuzzleInput) -> Any:
    total = 0
    dial = 50
    for line in puzzle.lines:
        direction = line[0]
        count = int(line[1:])
        while count > 0:
            if direction == "L":
                dial -= 1
            if direction == "R":
                dial += 1
            count -= 1

            if dial < 0 or dial > 99:
                dial %= 100

            if dial == 0:
                total += 1
    return total

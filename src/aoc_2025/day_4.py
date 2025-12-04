from typing import Any

from aoc.datatypes import Coord
from aoc.puzzle import PuzzleInput


def parse_input(puzzle: PuzzleInput) -> set[Coord]:
    rolls = set()
    for row, line in enumerate(puzzle.lines):
        for col, char in enumerate(line):
            if char == "@":
                rolls.add(Coord(row=row, col=col))
    return rolls


def part_1(puzzle: PuzzleInput) -> Any:
    total = 0
    rolls = parse_input(puzzle=puzzle)
    for roll in rolls:
        # Check adjacent
        adjacent = 0
        for row in [-1, 0, 1]:
            for col in [-1, 0, 1]:
                if row == 0 and col == 0:
                    continue
                if Coord(row=roll.row + row, col=roll.col + col) in rolls:
                    adjacent += 1
        if adjacent < 4:
            total += 1
    return total


def part_2(puzzle: PuzzleInput) -> Any:
    total = 0
    rolls = parse_input(puzzle=puzzle)
    while True:
        to_remove = []
        for roll in rolls:
            # Check adjacent
            adjacent = 0
            for row in [-1, 0, 1]:
                for col in [-1, 0, 1]:
                    if row == 0 and col == 0:
                        continue
                    if Coord(row=roll.row + row, col=roll.col + col) in rolls:
                        adjacent += 1
            if adjacent < 4:
                to_remove.append(roll)

        if not to_remove:
            break

        for accessible_roll in to_remove:
            total += 1
            rolls.remove(accessible_roll)

    return total

from collections import defaultdict
from typing import Any

from aoc.puzzle import PuzzleInput


def parse_input(puzzle: PuzzleInput) -> tuple[int, list[set[int]]]:
    start_line = puzzle.lines[0]
    start_point = start_line.index("S")

    splitters = []
    for line in puzzle.lines[2::2]:
        line_splitters = set()
        for i, char in enumerate(line):
            if char == "^":
                line_splitters.add(i)
        splitters.append(line_splitters)

    return start_point, splitters


def part_1(puzzle: PuzzleInput) -> Any:
    start_point, splitters = parse_input(puzzle=puzzle)
    beams = {start_point}

    total = 0
    for splitter_array in splitters:
        to_remove = set()
        to_add = set()
        for beam in beams:
            if beam in splitter_array:
                total += 1
                to_remove.add(beam)
                to_add.add(beam - 1)
                to_add.add(beam + 1)

        beams -= to_remove
        beams |= to_add

    return total


def part_2(puzzle: PuzzleInput) -> Any:
    start_point, splitters = parse_input(puzzle=puzzle)
    beams = defaultdict(int)
    beams[start_point] += 1

    total = 1
    for splitter_array in splitters:
        for beam, universes in beams.copy().items():
            if beam in splitter_array:
                total += universes

                del beams[beam]
                beams[beam - 1] += universes
                beams[beam + 1] += universes

    return total


# Came 1491th (had to take a break during exercise)

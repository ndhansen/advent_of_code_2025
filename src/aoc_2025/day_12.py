from typing import Any, NamedTuple

from aoc.datatypes import Coord
from aoc.exceptions import UnsolveableError
from aoc.puzzle import PuzzleInput
from frozendict import frozendict


class Shape(NamedTuple):
    size: int
    points: tuple[Coord, ...]


class Place(NamedTuple):
    size: Coord
    presents: frozendict[int, int]


def parse_puzzle(puzzle: PuzzleInput) -> tuple[frozendict[int, Shape], list[Place]]:
    parts = puzzle.raw.split("\n\n")
    presents_raw = parts[:-1]
    places_raw = parts[-1]

    presents = {}
    for present in presents_raw:
        index, locs_raw = present.split(":", maxsplit=1)
        coords = locs_raw.strip().splitlines()
        points = []
        for row, line in enumerate(coords):
            for col, char in enumerate(line):
                if char == ".":
                    continue
                points.append(Coord(row=row, col=col))
        presents[int(index)] = Shape(size=len(points), points=tuple(points))

    places = []
    for place_raw in places_raw.splitlines():
        size_raw, presents_count = place_raw.split(": ")
        col, row = size_raw.split("x")
        size = Coord(row=int(row), col=int(col))
        place_presents = {}
        for i, present_count in enumerate(presents_count.split(" ")):
            place_presents[i] = int(present_count)
        places.append(Place(size=size, presents=frozendict(place_presents)))

    return frozendict(presents), places


def part_1(puzzle: PuzzleInput) -> Any:
    shapes, regions = parse_puzzle(puzzle=puzzle)
    impossible = 0
    trivial = 0
    for region in regions:
        region_size = region.size.col * region.size.row
        shape_size_max = 0
        total_size_max = 0
        for i, count in region.presents.items():
            shape_size_max += count * shapes[i].size
            total_size_max += 9 * count

        if shape_size_max > region_size:
            impossible += 1
        if total_size_max <= region_size:
            trivial += 1

    plausible = (len(regions) - impossible) - trivial
    if plausible > 0:
        print("Your input was harder than mine I guess")
        raise UnsolveableError

    return trivial


def part_2(puzzle: PuzzleInput) -> Any:
    return "Merry Christmas!"


# Came 1237th

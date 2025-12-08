import itertools
from typing import Any

from aoc.puzzle import PuzzleInput


def parse_input(puzzle: PuzzleInput) -> list[tuple[int, int, int]]:
    boxes = []
    for line in puzzle.lines:
        x, y, z = line.split(",", maxsplit=2)
        boxes.append((int(x), int(y), int(z)))
    return boxes


def calc_distance(box_1: tuple[int, int, int], box_2: tuple[int, int, int]) -> float:
    return (
        ((box_1[0] - box_2[0]) ** 2)
        + ((box_1[1] - box_2[1]) ** 2)
        + ((box_1[2] - box_2[2]) ** 2)
    ) ** 0.5


def calc_score(
    networks: dict[tuple[int, int, int], frozenset[tuple[int, int, int]]],
) -> int:
    unique_networks = set(s for s in networks.values())
    lengths = sorted([len(x) for x in unique_networks], reverse=True)
    return lengths[0] * lengths[1] * lengths[2]


def part_1(puzzle: PuzzleInput) -> Any:
    boxes = parse_input(puzzle)
    distances = []
    for box_1, box_2 in itertools.combinations(boxes, 2):
        distance = calc_distance(box_1, box_2)
        distances.append((distance, box_1, box_2))
    distances.sort(key=lambda b: b[0])

    networks = {box: frozenset((box,)) for box in boxes}

    connected = 0
    iterations = 10 if puzzle.test else 1000
    while connected < iterations:
        _, box_1, box_2 = distances.pop(0)  # make this an index instead

        new_network = frozenset(networks[box_1] | networks[box_2])
        for b in networks[box_1] | networks[box_2]:
            networks[b] = new_network
            networks[b] = new_network

        connected += 1

    return calc_score(networks)


def part_2(puzzle: PuzzleInput) -> Any:
    boxes = parse_input(puzzle)
    distances = []
    for box_1, box_2 in itertools.combinations(boxes, 2):
        distance = calc_distance(box_1, box_2)
        distances.append((distance, box_1, box_2))
    distances.sort(key=lambda b: b[0])

    networks = {box: frozenset((box,)) for box in boxes}

    while True:
        _, box_1, box_2 = distances.pop(0)  # make this an index instead

        new_network = frozenset(networks[box_1] | networks[box_2])
        if len(new_network) == len(boxes):
            return box_1[0] * box_2[0]
        for b in networks[box_1] | networks[box_2]:
            networks[b] = new_network
            networks[b] = new_network


# Spent waaaay too long debugging a poorly written network, came 2457th

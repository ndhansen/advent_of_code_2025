import itertools
from collections.abc import Iterator, Sequence
from typing import Any

import numpy as np
from aoc.puzzle import PuzzleInput
from scipy import linalg
from tqdm import tqdm


def parse_puzzle(
    puzzle: PuzzleInput,
) -> list[tuple[tuple[bool, ...], list[tuple[int, ...]], tuple[int, ...]]]:
    machines = []
    for line in puzzle.lines:
        components = line.split(" ")
        lights_str = components[0]
        buttons_str = components[1:-1]
        joltage_str = components[-1]

        lights = tuple(
            False if light == "." else True for light in list(lights_str.strip("[]"))
        )
        joltage = tuple(int(j) for j in joltage_str.strip("{}").split(","))
        buttons = []
        for button_str in buttons_str:
            buttons.append(tuple(int(b) for b in button_str.strip("()").split(",")))

        machines.append((lights, buttons, joltage))

    return machines


def combinations_inf[T](items: Sequence[T]) -> Iterator[tuple[T, ...]]:
    i = 1
    while True:
        for num in itertools.combinations_with_replacement(items, r=i):
            yield num
        i += 1


def push_buttons(light: tuple[bool, ...], buttons: tuple[tuple[int, ...], ...]) -> bool:
    light_status = [False for _ in light]
    for button in buttons:
        for toggle in button:
            light_status[toggle] = not light_status[toggle]
    return tuple(light_status) == light


def part_1(puzzle: PuzzleInput) -> Any:
    machines = parse_puzzle(puzzle=puzzle)
    total = 0
    for lights, buttons, _ in machines:
        # Try all button combinations
        for combo in combinations_inf(buttons):
            if push_buttons(lights, combo):
                total += len(combo)
                break
    return total


# 1401


def min_button_presses(buttons: list[tuple[int, ...]], joltage: tuple[int, ...]) -> int:
    button_arrays = []
    for button in buttons:
        button_array = [0 for _ in joltage]
        for index in button:
            button_array[index] = 1
        button_arrays.append(button_array)

    button_arrays_rot = list(zip(*button_arrays))
    a = np.array(button_arrays_rot)
    b = np.array(joltage)
    x = linalg.solve(a, b)
    return int(sum(x))


def part_2(puzzle: PuzzleInput) -> Any:
    machines = parse_puzzle(puzzle=puzzle)
    total = 0
    for _, buttons, joltage in tqdm(machines):
        # Not fast or correct
        total += min_button_presses(buttons, joltage)
        ...
    return total


"""
(1,3) (0,1,2) (1,2,3) (0,2) {7,15,19,15}
15x (1,3) | (0,1,2) (1,2,3) (0,2) {7,0,19,0}
15x (1,3) 7x(0,2) | (0,1,2) (1,2,3) {0,0,12,0}

(0,1,2) (1,2,3) (0,2) (1,3) {7,15,19,15}
7x (0,1,2) | (1,2,3) (0,2) (1,3) {0,8,12,15}
8x (1,2,3) | (0,2) (1,3) {0,0,4,7}
8x (1,3) | (0,2) {0,0,12,7}

(1,3) (0,1,2) (1,2,3) (0,2) {7,15,19,15}
7x(0,2) | (1,3) (0,1,2) (1,2,3) {0,15,12,15}
12x(0,1,2) | (1,3) (1,2,3) {0,3,0,3}
3x(1,3) | (1,2,3) {0,3,0,3}
"""

import functools
import operator
from collections.abc import Callable
from typing import Any

from aoc.puzzle import PuzzleInput


def parse_ops(ops_line: list[str]) -> list[Callable[[int, int], int]]:
    operators = []
    for op_str in ops_line:
        if op_str == "+":
            operators.append(operator.add)
        if op_str == "*":
            operators.append(operator.mul)
    return operators


def parse_puzzle(
    puzzle: PuzzleInput,
) -> tuple[list[list[int]], list[Callable[[int, int], int]]]:
    numbers = []
    for line in puzzle.lines[:-1]:
        numbers.append([int(n) for n in line.split()])

    operators = parse_ops(puzzle.lines[-1].split())
    return numbers, operators


def part_1(puzzle: PuzzleInput) -> Any:
    numbers, operators = parse_puzzle(puzzle=puzzle)
    total = 0
    rotated = zip(*numbers)
    for nums, op in zip(rotated, operators):
        total += functools.reduce(op, nums)
    return total


def parse_puzzle_2(
    puzzle: PuzzleInput,
) -> tuple[list[list[int]], list[Callable[[int, int], int]]]:
    lines = puzzle.raw.splitlines()
    raw_nums = lines[:-1]
    flipped_raw_nums = list(zip(*[list(s) for s in raw_nums]))
    flipped_raw_nums = ["".join(s).strip() for s in flipped_raw_nums]

    numbers = []
    curr = []
    for num in flipped_raw_nums:
        if num != "":
            curr.append(int(num))
        else:
            numbers.append(curr.copy())
            curr = []
    if curr:
        numbers.append(curr.copy())

    operators = parse_ops(puzzle.lines[-1].split())

    return numbers, operators


def part_2(puzzle: PuzzleInput) -> Any:
    numbers, operators = parse_puzzle_2(puzzle=puzzle)
    total = 0
    for nums, op in zip(numbers, operators):
        total += functools.reduce(op, nums)
    return total


# Came 1086th

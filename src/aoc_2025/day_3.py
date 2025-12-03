from typing import Any

from aoc.puzzle import PuzzleInput


def parse_input(puzzle: PuzzleInput) -> list[list[int]]:
    lines = []
    for line in puzzle.lines:
        lines.append([int(x) for x in line.strip()])
    return lines


def part_1(puzzle: PuzzleInput) -> Any:
    total = 0
    counters = parse_input(puzzle)
    for bank in counters:
        tens = max(bank[:-1])

        ones = max(bank[bank.index(tens) + 1 :])
        total += (10 * tens) + ones
    return total


def part_2(puzzle: PuzzleInput) -> Any:
    total = 0
    numbers = parse_input(puzzle)
    for bank in numbers:
        i = 0
        while len(bank) > 12 and i < (len(bank) - 1):
            left, right = bank[i], bank[i + 1]
            if left < right:
                bank.pop(i)
                if i > 0:
                    i -= 1
            else:
                i += 1

        eliminate = 1
        while len(bank) > 12:
            if eliminate in bank:
                bank.pop(bank.index(eliminate))
            else:
                eliminate += 1

        new_num = int("".join(str(s) for s in bank))
        total += new_num
    return total

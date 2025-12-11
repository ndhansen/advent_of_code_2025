import functools
from typing import Any

from aoc.puzzle import PuzzleInput
from frozendict import frozendict


def parse_puzzle(puzzle: PuzzleInput) -> dict[str, frozenset[str]]:
    connections = {}
    for line in puzzle.lines:
        source, targets_str = line.split(": ", maxsplit=1)
        connections[source] = frozenset(targets_str.split(" "))
    return connections


@functools.cache
def dfs(start: str, goal: str, paths: frozendict[str, set[str]]) -> int:
    goals = 0
    for neighbor in paths[start]:
        if neighbor == goal:
            goals += 1
        else:
            goals += dfs(neighbor, goal, paths=paths)

    return goals


def part_1(puzzle: PuzzleInput) -> Any:
    servers = parse_puzzle(puzzle=puzzle)
    servers["out"] = frozenset()
    return dfs(start="you", goal="out", paths=frozendict(servers))


def part_2(puzzle: PuzzleInput) -> Any:
    servers = parse_puzzle(puzzle=puzzle)
    servers["out"] = frozenset()
    paths_fft = dfs(start="svr", goal="fft", paths=frozendict(servers))
    paths_fft_dac = dfs(start="fft", goal="dac", paths=frozendict(servers))
    paths_dac_out = dfs(start="dac", goal="out", paths=frozendict(servers))
    return paths_fft * paths_fft_dac * paths_dac_out


# 2536th

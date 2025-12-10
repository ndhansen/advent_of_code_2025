import itertools
from collections.abc import Iterator, Sequence
from typing import Any, Mapping

from aoc import a_star
from aoc.puzzle import PuzzleInput
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
    # curr_jolts -> min_steps
    jolt_by_step: dict[tuple[int, ...], int] = {}
    seen_jolts = set()
    frontier = [[0 for _ in joltage]]
    next_frontier = []
    steps = 1
    while True:
        for item in frontier:
            for button in buttons:
                curr_list = item.copy()
                skip = False
                for index in button:
                    curr_list[index] += 1
                    if curr_list[index] > joltage[index]:
                        skip = True
                if skip:
                    continue
                curr = tuple(curr_list)
                if curr == joltage:
                    return steps
                if curr in seen_jolts:
                    continue
                next_frontier.append(curr_list)
                seen_jolts.add(curr)

        steps += 1
        print(steps)
        frontier = next_frontier
        next_frontier = []


def greedy(buttons: list[tuple[int, ...]], joltage: tuple[int, ...]) -> int | None:
    buttons = sorted(buttons, key=len, reverse=True)
    for button in buttons:
        divisor = min(joltage[b] for b in button)

        new_joltage = list(joltage)
        for index in button:
            new_joltage[index] -= divisor

        if sum(new_joltage) == 0:
            return divisor

        new_buttons = buttons.copy()
        new_buttons.remove(button)
        remaining = greedy(new_buttons, tuple(new_joltage))
        if remaining:
            return divisor + remaining
    return None


class ButtonPressHeuristic(a_star.Heuristic[tuple[int, ...]]):
    def __call__(self, current: tuple[int, ...], goal: tuple[int, ...]) -> float:
        total = 0
        for cj, gj in zip(current, goal, strict=True):
            if cj > gj:
                return float("inf")
            total += gj - cj
        return float(total)


class ButtonPressCost(a_star.Cost[tuple[int, ...]]):
    def __call__(
        self,
        paths: Mapping[tuple[int, ...], tuple[int, ...]],
        current: tuple[int, ...],
        last: tuple[int, ...],
    ) -> float:
        return 1.0


class ButtonPressNeighbors(a_star.Neighbors[tuple[int, ...]]):
    def __init__(self, buttons: list[tuple[int, ...]], goal: tuple[int, ...]) -> None:
        self.buttons = buttons
        self.goal = goal

    def __call__(
        self, current: tuple[int, ...], paths: Mapping[tuple[int, ...], tuple[int, ...]]
    ) -> Iterator[tuple[int, ...]]:
        for button in self.buttons:
            c = list(current)
            skip = False
            for index in button:
                c[index] += 1
                if c[index] > self.goal[index]:
                    skip = True
            if not skip:
                yield tuple(c)


def part_2(puzzle: PuzzleInput) -> Any:
    machines = parse_puzzle(puzzle=puzzle)
    total = 0
    for _, buttons, joltage in tqdm(machines):
        # Not fast or correct
        steps = greedy(buttons, joltage)
        print(steps)
        if not steps:
            raise RuntimeError("No path found!")
        total += steps
        # Dynamic Programming attempt 1, Too slow
        # total += min_button_presses(buttons, joltage)

        # A-star is even slower
        # start = tuple(0 for _ in joltage)
        # _, steps = a_star.a_star(
        #     start=start,
        #     goal=joltage,
        #     heuristic=ButtonPressHeuristic(),
        #     cost_func=ButtonPressCost(),
        #     next_func=ButtonPressNeighbors(buttons=buttons, goal=joltage),
        # )
        # total += steps
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

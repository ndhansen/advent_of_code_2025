import heapq
import itertools
from typing import Any, NamedTuple

from aoc.datatypes import Coord
from aoc.puzzle import PuzzleInput


def parse_puzzle(puzzle: PuzzleInput) -> list[Coord]:
    corners = []
    for line in puzzle.lines:
        x, y = line.split(",")
        corners.append(Coord(int(y), int(x)))
    return corners


def part_1(puzzle: PuzzleInput) -> Any:
    corners = parse_puzzle(puzzle=puzzle)
    largest_area = 0
    for c1, c2 in itertools.combinations(corners, 2):
        area = (abs(c1.row - c2.row) + 1) * (abs(c1.col - c2.col) + 1)
        if area > largest_area:
            largest_area = area
    return largest_area


# 229th


def does_vector_intercept(h_s: Coord, h_e: Coord, v_s: Coord, v_e: Coord) -> bool:
    intersect = Coord(row=h_s.row, col=v_s.col)
    if h_s.col < intersect.col < h_e.col and v_s.row < intersect.row < v_e.row:
        return True
    return False


class Rectangle(NamedTuple):
    tl: Coord
    tr: Coord
    bl: Coord
    br: Coord

    @staticmethod
    def from_points(first: Coord, second: Coord) -> "Rectangle":
        left_col = min(first.col, second.col)
        right_col = max(first.col, second.col)
        top_row = min(first.row, second.row)
        bot_row = max(first.row, second.row)
        tl = Coord(row=top_row, col=left_col)
        tr = Coord(row=top_row, col=right_col)
        bl = Coord(row=bot_row, col=left_col)
        br = Coord(row=bot_row, col=right_col)
        return Rectangle(tl=tl, tr=tr, bl=bl, br=br)

    def intersects(self, other: "Rectangle") -> bool:
        # Check if it's contained
        if (
            self.tr.row <= other.tr.row
            and self.br.row >= other.br.row
            and self.tr.col <= other.tr.col
            and self.tl.col >= other.tl.col
        ):
            return True

        if (
            other.tr.row <= self.tr.row
            and other.br.row >= self.br.row
            and other.tr.col <= self.tr.col
            and other.tl.col >= self.tl.col
        ):
            return True

        # Calculate intersections
        # Top row to left col
        if does_vector_intercept(self.tl, self.tr, other.bl, other.tl):
            return True
        # Top row to right col
        if does_vector_intercept(self.tl, self.tr, other.br, other.tr):
            return True
        # Bot row to left col
        if does_vector_intercept(self.bl, self.br, other.bl, other.tl):
            return True
        # Bot row to right col
        if does_vector_intercept(self.bl, self.br, other.br, other.tr):
            return True

        # left col to top row
        if does_vector_intercept(other.tl, other.tr, self.bl, self.tl):
            return True
        # left col to bot row
        if does_vector_intercept(other.bl, other.br, self.bl, self.tl):
            return True
        # right col to top row
        if does_vector_intercept(other.tl, other.tr, self.br, self.tr):
            return True
        # right col to bot row
        if does_vector_intercept(other.bl, other.br, self.br, self.tr):
            return True

        return False


def is_left_turn(c1: Coord, c2: Coord, c3: Coord) -> bool:
    # If second point is to the right, expec third point below
    if c1.col < c2.col and c2.row < c3.row:
        return False
    # if second point below, expect third point to left
    if c1.row < c2.row and c2.col > c3.col:
        return False
    # if second point to left, expect third point above
    if c1.col > c2.col and c2.row > c3.row:
        return False
    # if second point above, expect third point to right
    if c1.row > c2.row and c2.col < c3.col:
        return False
    return True


def part_2(puzzle: PuzzleInput) -> Any:
    corners = parse_puzzle(puzzle=puzzle)
    areas: list[tuple[int, tuple[Coord, Coord]]] = []

    print(len(corners))
    print(Coord(row=50282, col=95634) == Coord(row=50282, col=95634))
    print(Coord(row=50282, col=95634) in corners)
    print(Coord(row=95634, col=50282) in corners)
    # Build all areas (includes incorrect "outer" areas)
    for c1, c2 in itertools.combinations(corners, 2):
        if Coord(row=50282, col=95634) in (c1, c2):
            import pudb

            pudb.set_trace()
        if Coord(row=95634, col=50282) in (c1, c2) and Coord(row=5207, col=66267) in (
            c1,
            c2,
        ):
            import pudb

            pudb.set_trace()
        area = (abs(c1.row - c2.row) + 1) * (abs(c1.col - c2.col) + 1)
        heapq.heappush(areas, (-area, (c1, c2)))

    left_turn_rects = []
    a_corner_iter = iter(corners)
    b_corner_iter = iter(corners[1:] + corners[:1])
    c_corner_iter = iter(corners[2:] + corners[:2])
    for c1, c2, c3 in zip(a_corner_iter, b_corner_iter, c_corner_iter):
        if is_left_turn(c1, c2, c3):
            left_turn_rects.append(Rectangle.from_points(c1, c3))

    for area, area_corners in areas:
        c1, c2 = area_corners

        low_row = min(c1.row, c2.row)
        high_row = max(c1.row, c2.row)
        low_col = min(c1.col, c2.col)
        high_col = max(c1.col, c2.col)

        failed = False

        # Maybe not needed?
        for corner in corners:
            # if row is between corner rows and col is between corner cols
            if low_col < corner.col < high_col and low_row < corner.row < high_row:
                failed = True

        area_rect = Rectangle.from_points(c1, c2)
        for outside_rect in left_turn_rects:
            if area_rect.intersects(outside_rect):
                failed = True

        if not failed:
            import pudb

            pudb.set_trace()
            return -area


# Not:
# 113979918
# 167704056
# 4667093750
# 1035829542
# 58874757
# Is:
#
# Rect:
# 94634,50282
# 5207,66267

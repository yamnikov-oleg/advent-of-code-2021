from collections import defaultdict
from dataclasses import dataclass
from typing import Iterator, List

from common import read_input_txt


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass
class VentLine:
    start: Point
    end: Point

    @property
    def is_vertical(self) -> bool:
        return self.start.x == self.end.x

    @property
    def is_horizontal(self) -> bool:
        return self.start.y == self.end.y

    @property
    def is_diagonal(self) -> bool:
        return abs(self.end.x - self.start.x) == abs(self.end.y - self.start.y)

    @property
    def points(self) -> Iterator[Point]:
        if not self.is_vertical and not self.is_horizontal and not self.is_diagonal:
            raise ValueError(f"The points of this line ({self}) cannot be computed")

        if self.is_vertical or self.is_diagonal:
            point_count = abs(self.end.y - self.start.y) + 1
        elif self.is_horizontal:
            point_count = abs(self.end.x - self.start.x) + 1

        if self.end.x > self.start.x:
            delta_x = 1
        elif self.end.x < self.start.x:
            delta_x = -1
        else:
            delta_x = 0

        if self.end.y > self.start.y:
            delta_y = 1
        elif self.end.y < self.start.y:
            delta_y = -1
        else:
            delta_y = 0

        x, y = self.start.x, self.start.y
        for _ in range(point_count):
            yield Point(x, y)
            x += delta_x
            y += delta_y


def parse_vent_line(line: str) -> VentLine:
    pos1, pos2 = line.split(" -> ")

    x1_str, y1_str = pos1.split(",")
    x1, y1 = int(x1_str), int(y1_str)

    x2_str, y2_str = pos2.split(",")
    x2, y2 = int(x2_str), int(y2_str)

    return VentLine(
        start=Point(x1, y1),
        end=Point(x2, y2),
    )


def count_multiline_points(vent_lines: List[VentLine]) -> int:
    covered_points = defaultdict(int)
    for vent_line in vent_lines:
        for point in vent_line.points:
            covered_points[point] += 1

    multiline_point_count = 0
    for point, line_count in covered_points.items():
        if line_count > 1:
            multiline_point_count += 1

    return multiline_point_count


def part1(input_txt: str) -> int:
    vent_lines = [parse_vent_line(line) for line in input_txt.splitlines()]
    right_vent_lines = [line for line in vent_lines if line.is_horizontal or line.is_vertical]
    return count_multiline_points(right_vent_lines)


def part2(input_txt: str) -> int:
    vent_lines = [parse_vent_line(line) for line in input_txt.splitlines()]
    return count_multiline_points(vent_lines)


def main():
    input_txt = read_input_txt(__file__)

    part1_answer = part1(input_txt)
    print("Part 1:", part1_answer)

    part2_answer = part2(input_txt)
    print("Part 2:", part2_answer)

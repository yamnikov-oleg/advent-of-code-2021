import dataclasses
from dataclasses import dataclass, field
from enum import Enum
from typing import Type, TypeVar

from common import read_input_txt


class Dir(Enum):
    FORWARD = "forward"
    UP = "up"
    DOWN = "down"


@dataclass(frozen=True)
class Command:
    dir: Dir
    amount: int


PositionBase = TypeVar("PositionBase", bound="Position")


@dataclass(frozen=True)
class Position:
    x: int
    depth: int

    @classmethod
    def zero(cls: Type[PositionBase]) -> PositionBase:
        return cls(x=0, depth=0)


def parse_command(line: str) -> Command:
    dir_str, amount_str = line.split()
    return Command(Dir(dir_str), int(amount_str))


def apply_command(position: Position, command: Command) -> Position:
    if command.dir == Dir.FORWARD:
        return dataclasses.replace(position, x=position.x + command.amount)
    elif command.dir == Dir.UP:
        return dataclasses.replace(position, depth=position.depth - command.amount)
    elif command.dir == Dir.DOWN:
        return dataclasses.replace(position, depth=position.depth + command.amount)
    else:
        raise ValueError(command.dir)


def part1(input_txt: str) -> int:
    lines = input_txt.splitlines()
    commands = [parse_command(line) for line in lines]
    position = Position(x=0, depth=0)
    for command in commands:
        position = apply_command(position, command)
    return position.x * position.depth


@dataclass
class Submarine:
    position: Position = field(default_factory=Position.zero)
    aim: int = 0

    def apply_command(self, command: Command) -> None:
        if command.dir == Dir.FORWARD:
            self.position = dataclasses.replace(
                self.position,
                x=self.position.x + command.amount,
                depth=self.position.depth + self.aim * command.amount,
            )
        elif command.dir == Dir.UP:
            self.aim -= command.amount
        elif command.dir == Dir.DOWN:
            self.aim += command.amount
        else:
            raise ValueError(command.dir)


def part2(input_txt: str) -> int:
    lines = input_txt.splitlines()
    commands = [parse_command(line) for line in lines]
    submarine = Submarine()
    for command in commands:
        submarine.apply_command(command)
    return submarine.position.x * submarine.position.depth


def main() -> None:
    input_txt = read_input_txt(__file__)

    part1_answer = part1(input_txt)
    print("Part1:", part1_answer)

    part2_answer = part2(input_txt)
    print("Part2:", part2_answer)

from .solution import part1, part2

input_txt = (
    "0,9 -> 5,9\n"
    "8,0 -> 0,8\n"
    "9,4 -> 3,4\n"
    "2,2 -> 2,1\n"
    "7,0 -> 7,4\n"
    "6,4 -> 2,0\n"
    "0,9 -> 2,9\n"
    "3,4 -> 1,4\n"
    "0,0 -> 8,8\n"
    "5,5 -> 8,2\n"
)


def test_part1():
    assert part1(input_txt) == 5


def test_part2() -> None:
    assert part2(input_txt) == 12

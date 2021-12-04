from .solution import part1, part2


def test_part1():
    input_txt = "forward 5\ndown 5\nforward 8\nup 3\ndown 8\nforward 2\n"
    assert part1(input_txt) == 150


def test_part2():
    input_txt = "forward 5\ndown 5\nforward 8\nup 3\ndown 8\nforward 2\n"
    assert part2(input_txt) == 900

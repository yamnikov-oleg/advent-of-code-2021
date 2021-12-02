from day02 import part1, part2


def test_part1():
    input_txt = (
        "forward 5\n"
        "down 5\n"
        "forward 8\n"
        "up 3\n"
        "down 8\n"
        "forward 2\n"
    )
    assert part1(input_txt) == 150


def test_part2():
    input_txt = (
        "forward 5\n"
        "down 5\n"
        "forward 8\n"
        "up 3\n"
        "down 8\n"
        "forward 2\n"
    )
    assert part2(input_txt) == 900

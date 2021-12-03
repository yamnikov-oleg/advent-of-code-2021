from day03 import part1, part2


def test_part1():
    input_txt = (
        "00100\n"
        "11110\n"
        "10110\n"
        "10111\n"
        "10101\n"
        "01111\n"
        "00111\n"
        "11100\n"
        "10000\n"
        "11001\n"
        "00010\n"
        "01010\n"
    )
    assert part1(input_txt) == 198


def test_part2():
    input_txt = (
        "00100\n"
        "11110\n"
        "10110\n"
        "10111\n"
        "10101\n"
        "01111\n"
        "00111\n"
        "11100\n"
        "10000\n"
        "11001\n"
        "00010\n"
        "01010\n"
    )
    assert part2(input_txt) == 230

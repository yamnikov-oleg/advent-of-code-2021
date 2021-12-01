from day01 import part1, part2


def test_part1():
    depths = [
        199,
        200,
        208,
        210,
        200,
        207,
        240,
        269,
        260,
        263,
    ]
    assert part1(depths) == 7


def test_part2():
    depths = [
        199,
        200,
        208,
        210,
        200,
        207,
        240,
        269,
        260,
        263,
    ]
    assert part2(depths) == 5

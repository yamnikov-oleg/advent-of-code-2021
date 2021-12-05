from common import read_input_txt


def window(lst, n):
    if n < 1:
        raise ValueError(n)
    elif n == 1:
        for el in lst:
            yield (el,)
    else:
        for el, rest in zip(lst, window(lst[1:], n - 1)):
            yield (el, *rest)


def part1(depths: list[int]) -> int:
    increases = 0
    for prev, curr in window(depths, 2):
        if curr > prev:
            increases += 1
    return increases


def part2(depths: list[int]) -> int:
    increases = 0
    prev_window_sum = None
    for el1, el2, el3 in window(depths, 3):
        window_sum = el1 + el2 + el3
        if prev_window_sum is not None and window_sum > prev_window_sum:
            increases += 1
        prev_window_sum = window_sum
    return increases


def main():
    input_txt = read_input_txt(__file__)
    input_lines = input_txt.splitlines()
    depths = [int(line) for line in input_lines]

    part1_answer = part1(depths)
    print("Part1:", part1_answer)

    part2_answer = part2(depths)
    print("Part2:", part2_answer)

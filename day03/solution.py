from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Tuple, Type

BASE_DIR = Path(__file__).resolve().parent


class BitString:
    def __init__(self, bits: str = None, length: int = None) -> None:
        """
        :param bits: E.g. "001101"
        :param length: Given length 5 produces "00000"
        """
        if bits:
            self.bits = bits
        elif length:
            self.bits = "0" * length
        else:
            self.bits = ""

    def __getitem__(self, index: int) -> bool:
        """
        E.g.::
            BitString("01001")[1]  # => True
            BitString("01001")[2]  # => False
        """
        try:
            return self.bits[index] == "1"
        except IndexError:
            return False

    def __setitem__(self, index: int, bit: bool) -> None:
        """
        E.g.::
            BitString("01001")[1] = False  # => BitString("00001")
        """
        pre_bits = self.bits[:index]
        if len(pre_bits) < index:
            pre_bits += "0" * (index - len(pre_bits))

        post_bits = self.bits[index + 1 :]

        new_bit = "1" if bit else "0"

        self.bits = pre_bits + new_bit + post_bits

    def __len__(self) -> int:
        """
        E.g.::
            len(BitString("01001"))  # => 5
        """
        return len(self.bits)

    def __iter__(self):
        """
        E.g.::
            for bit in BitString("01001"):
                print(bit)

            # False
            # True
            # False
            # False
            # True
        """
        for bit_str in self.bits:
            yield bit_str == "1"

    def __int__(self) -> int:
        """
        E.g.::
            int(BitString("01001"))  # => 9
        """
        integer = 0
        for bit in self:
            if bit:
                integer = integer * 2 + 1
            else:
                integer = integer * 2

        return integer


def get_bit_stats(bit_strings: List[BitString], bit_ix: int) -> Tuple[int, int]:
    """
    :returns: (number of ones, number of zeroes) at index bit_ix in bit_strings.
    """
    count_ones = 0
    count_zeros = 0
    for bit_string in bit_strings:
        if bit_string[bit_ix]:
            count_ones += 1
        else:
            count_zeros += 1

    return count_ones, count_zeros


def extract_rates(bit_strings: List[BitString]) -> Tuple[int, int]:
    """
    :returns: (gamma rate, epsilon rate)
    """
    max_string_len = max(len(s) for s in bit_strings)

    # Count 1's and 0's for each bit position
    bit_stats = []
    for bit_ix in range(max_string_len):
        bit_stats.append(get_bit_stats(bit_strings, bit_ix))

    # Calculate gamma and epsilon using the collected counts
    gamma = BitString(length=max_string_len)
    epsilon = BitString(length=max_string_len)
    for bit_ix, (count_ones, count_zeros) in enumerate(bit_stats):
        if count_ones > count_zeros:
            gamma[bit_ix] = True
            epsilon[bit_ix] = False
        else:
            gamma[bit_ix] = False
            epsilon[bit_ix] = True

    return int(gamma), int(epsilon)


def part1(input_txt: str) -> int:
    bit_strings = [BitString(line) for line in input_txt.splitlines()]
    gamma, epsilon = extract_rates(bit_strings)
    return gamma * epsilon


class RatingCriteria(ABC):
    """
    Abstract class for O2GenRatingCriteria and CO2ScrubRatingCriteria.
    """

    @classmethod
    @abstractmethod
    def prepare(cls, bit_strings: List[BitString], bit_ix: int) -> "RatingCriteria":
        """
        Given bit_strings and bit_ix produces the criteria object.
        That is, counts ones and zeroes at bit_ix and returns the object that will
        decide which bit strings to keep and which to discard.
        """
        ...

    @abstractmethod
    def match(self, bit_string: BitString) -> bool:
        """
        :returns: True to keep the string, False to discard
        """
        ...


@RatingCriteria.register
class O2GenRatingCriteria:
    """
    O2 generator rating criteria.
    """

    def __init__(self, bit_ix: int, keep_bit: bool) -> None:
        self.bit_ix = bit_ix
        self.keep_bit = keep_bit

    @classmethod
    def prepare(
        cls, bit_strings: List[BitString], bit_ix: int
    ) -> "O2GenRatingCriteria":
        count_ones, count_zeros = get_bit_stats(bit_strings, bit_ix)
        if count_ones > count_zeros:
            return cls(bit_ix=bit_ix, keep_bit=True)
        elif count_ones < count_zeros:
            return cls(bit_ix=bit_ix, keep_bit=False)
        else:
            return cls(bit_ix=bit_ix, keep_bit=True)

    def match(self, bit_string: BitString) -> bool:
        return bit_string[self.bit_ix] == self.keep_bit


@RatingCriteria.register
class CO2ScrubRatingCriteria:
    """
    CO2 scrubber rating criteria.
    """

    def __init__(self, bit_ix: int, keep_bit: bool) -> None:
        self.bit_ix = bit_ix
        self.keep_bit = keep_bit

    @classmethod
    def prepare(
        cls, bit_strings: List[BitString], bit_ix: int
    ) -> "CO2ScrubRatingCriteria":
        count_ones, count_zeros = get_bit_stats(bit_strings, bit_ix)
        if count_ones > count_zeros:
            return cls(bit_ix=bit_ix, keep_bit=False)
        elif count_ones < count_zeros:
            return cls(bit_ix=bit_ix, keep_bit=True)
        else:
            return cls(bit_ix=bit_ix, keep_bit=False)

    def match(self, bit_string: BitString) -> bool:
        return bit_string[self.bit_ix] == self.keep_bit


def extract_rating(
    bit_strings: List[BitString], criteria_cls: Type[RatingCriteria]
) -> int:
    """
    :returns: The rating value given its criteria class.
    """
    bit_ix = 0
    max_string_len = max(len(s) for s in bit_strings)

    while bit_ix < max_string_len and len(bit_strings) > 1:
        criteria = criteria_cls.prepare(bit_strings, bit_ix)
        bit_strings = [s for s in bit_strings if criteria.match(s)]
        bit_ix += 1

    if len(bit_strings) == 1:
        return int(bit_strings[0])
    else:
        raise ValueError(f"Didn't work: {bit_strings}")


def part2(input_txt: str) -> int:
    bit_strings = [BitString(line) for line in input_txt.splitlines()]
    o2_rating = extract_rating(bit_strings, O2GenRatingCriteria)
    co2_rating = extract_rating(bit_strings, CO2ScrubRatingCriteria)
    return o2_rating * co2_rating


def main():
    input_txt = (BASE_DIR / "input.txt").read_text()

    part1_answer = part1(input_txt)
    print("Part1:", part1_answer)

    part2_answer = part2(input_txt)
    print("Part2:", part2_answer)


if __name__ == "__main__":
    main()

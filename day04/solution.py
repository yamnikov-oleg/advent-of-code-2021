from dataclasses import InitVar, dataclass, field
from typing import Iterator, List, Optional, Tuple

from common import read_input_txt


@dataclass
class BoardCell:
    number: int
    marked: bool = False


@dataclass
class Board:
    """
    Example:
        board = Board(size=2)
        board[0, 0] = 1
        board[0, 1] = 2
        board[1, 0] = 3
        board[1, 1] = 4

        board.mark(1)
        board.is_winning  # => False

        board.mark(3)
        board.is_winning  # => True
        board.score  # => 18 = (2 + 4) * 3
    """

    size: InitVar[int]
    rows: List[List[BoardCell]] = field(init=False)
    winning_draw: Optional[int] = None

    def __post_init__(self, size):
        self.rows = []
        for _ in range(size):
            row = []
            for _ in range(size):
                row.append(BoardCell(0))
            self.rows.append(row)

    def __setitem__(self, cell_indices: Tuple[int, int], number: int):
        row_ix, column_ix = cell_indices
        self.rows[row_ix][column_ix].number = number

    def mark(self, number: int):
        was_winning = self.is_winning

        for row in self.rows:
            for cell in row:
                if cell.number == number:
                    cell.marked = True

        if not was_winning and self.is_winning:
            self.winning_draw = number

    @property
    def columns(self) -> Iterator[List[BoardCell]]:
        return zip(*self.rows)

    @property
    def is_winning(self) -> bool:
        for row in self.rows:
            if all(cell.marked for cell in row):
                return True

        for column in self.columns:
            if all(cell.marked for cell in column):
                return True

        return False

    @property
    def score(self) -> int:
        if not self.is_winning:
            raise RuntimeError("Non-winning board has no score")

        unmarked_sum = 0
        for row in self.rows:
            for cell in row:
                if not cell.marked:
                    unmarked_sum += cell.number

        return unmarked_sum * self.winning_draw


def parse_number_grid(grid_txt: str) -> List[List[int]]:
    """
    Example::
        parse_number_grid("1 2\n3 4\n")  # => [[1, 2], [3, 4]]
    """
    grid = []
    for line in grid_txt.splitlines():
        line = line.strip()
        if not line:
            continue

        row = [int(el) for el in line.split(" ") if el]
        grid.append(row)

    return grid


def parse_board(board_txt: str) -> Board:
    """
    Example::
        board = parse_board("1 2\n3 4\n")
        board.rows  # => [[BoardCell(1), BoardCell(2)], [BoardCell(3), BoardCell(4)]]
    """
    grid = parse_number_grid(board_txt)
    board = Board(size=len(grid))
    for row_ix, row in enumerate(grid):
        for column_ix, number in enumerate(row):
            board[row_ix, column_ix] = number

    return board


def play_bingo(number_queue: List[int], boards: List[Board]) -> List[Board]:
    """
    Plays bingo given the queue of drawn numbers and playing board.
    Winning boards are excluded from the game.
    The game is played until all the boards have won or until we run out of numbers to draw.

    :returns: The winning boards in the order they have won.
    """
    won_boards = []

    for number in number_queue:
        for board in boards:
            board.mark(number)

        still_playing_boards = []
        for board in boards:
            if board.is_winning:
                won_boards.append(board)
            else:
                still_playing_boards.append(board)

        if not still_playing_boards:
            break

        boards = still_playing_boards

    return won_boards


def parse_input(input_txt: str) -> Tuple[List[int], List[Board]]:
    """
    :returns: The number drawing queue and the boards.
    """
    sections = input_txt.split("\n\n")

    number_queue_section = sections[0]
    number_queue = [int(el) for el in number_queue_section.split(",")]

    board_sections = sections[1:]
    boards = [parse_board(board_txt) for board_txt in board_sections]

    return number_queue, boards


def part1(input_txt: str) -> int:
    number_queue, boards = parse_input(input_txt)
    won_boards = play_bingo(number_queue, boards)
    return won_boards[0].score


def part2(input_txt: str) -> None:
    number_queue, boards = parse_input(input_txt)
    won_boards = play_bingo(number_queue, boards)
    return won_boards[-1].score


def main():
    input_txt = read_input_txt(__file__)

    part1_answer = part1(input_txt)
    print("Part 1:", part1_answer)

    part2_answer = part2(input_txt)
    print("Part 2:", part2_answer)

from importlib import import_module
from typing import Optional

from invoke import Context, task


@task
def run(ctx, day):
    # type: (Context, str) -> None
    """
    Run the solution for a day.
    Examples:
        inv run 1
        inv run 02
    """

    if len(day) == 1:
        day = "0" + day

    day_module = import_module(f"day{day}.solution")
    day_module.main()


@task
def test(ctx, day=None):
    # type: (Context, Optional[str]) -> None
    """
    Test the solution for a day or for all the days.
    Examples:
        inv test
        inv test -d 1
        inv test -d 02
    """

    if day:
        if len(day) == 1:
            day = "0" + day

        ctx.run(f"pytest day{day}", pty=True)
    else:
        ctx.run("pytest", pty=True)


@task
def lint(ctx):
    # type: (Context) -> None
    """
    Make sure everything is nice and smoothy.
    """
    print("=== BLACK ===")
    ctx.run("black .", pty=True)

    print("=== ISORT ===")
    ctx.run("isort .", pty=True)

    print("=== FLAKE8 ===")
    r = ctx.run("flake8 .", pty=True, warn=True)
    if r.ok:
        print("=== OK ===")
    else:
        print("=== FAIL ===")


SOLUTION_TEMPLATE = """
from common import read_input_txt


def part1(input_txt: str) -> None:
    pass


def part2(input_txt: str) -> None:
    pass


def main():
    input_txt = read_input_txt(__file__)

    part1_answer = part1(input_txt)
    print("Part 1:", part1_answer)

    part2_answer = part2(input_txt)
    print("Part 2:", part2_answer)
""".strip()


SOLUTION_TEST_TEMPLATE = """
from .solution import part1, part2


def test_part1():
    input_txt = ""
    assert part1(input_txt) is None


def test_part2() -> None:
    input_txt = ""
    assert part2(input_txt) is None
""".strip()


@task
def add(ctx, day):
    # type: (Context, str) -> None
    """
    Create files for a new day.
    """
    if len(day) == 1:
        day = "0" + day

    ctx.run(f"mkdir -p day{day}")

    with open(f"day{day}/__init__.py", "w") as f:
        pass

    with open(f"day{day}/solution.py", "w") as f:
        f.write(SOLUTION_TEMPLATE)

    with open(f"day{day}/solution_test.py", "w") as f:
        f.write(SOLUTION_TEST_TEMPLATE)

    with open(f"day{day}/input.txt", "w") as f:
        pass

    print("Created new scripts, running lint...")
    print()

    lint(ctx)

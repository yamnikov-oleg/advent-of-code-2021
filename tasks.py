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

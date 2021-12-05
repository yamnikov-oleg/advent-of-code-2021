from typing import TypeVar

T = TypeVar("T")

class Result:
    ok: bool

class Context:
    def run(self, command: str, pty: bool = False, warn: bool = False) -> Result: ...

def task(f: T) -> T: ...

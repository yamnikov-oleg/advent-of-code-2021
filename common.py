from pathlib import Path


def read_input_txt(dunder_file: str) -> str:
    base_dir = Path(dunder_file).resolve().parent
    return (base_dir / "input.txt").read_text()

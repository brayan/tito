from pathlib import Path

def get_root_dir() -> Path:
    return Path(__file__).resolve().parent.parent.parent.parent

def get_output_dir() -> Path:
    return get_root_dir() / "output"

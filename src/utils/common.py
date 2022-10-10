from pathlib import Path
from typing import Union

from yaml import safe_load


PathLike = Union[str, Path]


def read_sql(filepath: PathLike, **kwargs) -> str:
    with open(filepath) as f:
        return f.read().format(**kwargs)


def read_yaml(filepath: PathLike):
    with open(filepath) as f:
        return safe_load(f)

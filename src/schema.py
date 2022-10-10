from dataclasses import dataclass

from dacite import from_dict

from utils.common import read_yaml


@dataclass
class CalculatedCurrencyConfig:
    code: str
    sql_filename: str
    dependencies: list[str]


@dataclass
class Config:
    downloadable: list[str]
    calculated: list[CalculatedCurrencyConfig]


def load_config(filepath: str) -> Config:
    return from_dict(data_class=Config, data=read_yaml(filepath))

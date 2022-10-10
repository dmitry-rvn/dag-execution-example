from datetime import date
from pathlib import Path
from dataclasses import dataclass
from abc import ABC, abstractmethod
import os

from dotenv import load_dotenv

from external.data import get_currency_rate
from utils.database import execute_query, DB_DATE_FORMAT
from utils.common import read_sql


load_dotenv()

SQL_CALCULATIONS_FOLDER = Path(os.getenv('SQL_CALCULATIONS_FOLDER'))


@dataclass
class Task(ABC):
    currency_code: str

    @abstractmethod
    def execute(self, *args, **kwargs):
        raise NotImplementedError


@dataclass
class TaskDownloadInsert(Task):

    def execute(self, dt: date):
        value = get_currency_rate(self.currency_code, dt)
        execute_query(f"INSERT INTO rates (dt, currency_code, value) "
                      f"VALUES ('{dt.strftime(DB_DATE_FORMAT)}', '{self.currency_code}', {value})")


@dataclass
class TaskCalculateInsert(Task):
    sql_filename: str
    dependencies: list[str]

    def execute(self, dt: date):
        execute_query(read_sql(SQL_CALCULATIONS_FOLDER / self.sql_filename, dt=dt.strftime(DB_DATE_FORMAT)))

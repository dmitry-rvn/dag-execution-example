from pathlib import Path
import os

from dotenv import load_dotenv
from loguru import logger

from utils.common import read_sql
from utils.database import execute_query


load_dotenv()

SQL_INIT_FOLDER = Path(os.getenv('SQL_INIT_FOLDER'))


def init_database():
    for filepath in SQL_INIT_FOLDER.glob('*.sql'):
        logger.info(f'>>> executing {filepath}')
        execute_query(read_sql(filepath), as_script=True)

import os
from datetime import datetime, timedelta

import click
from loguru import logger
from dotenv import load_dotenv

from dag import create_dag as _create_dag, DAG
from init_database import init_database
from utils.database import fetch_data


load_dotenv()


@click.group()
def cli():
    ...


@cli.command(help='Recreate database tables')
def recreate_database():
    logger.info('recreate_database invoked')
    init_database()


@cli.command(help="Create DAG from tasks config file, save DAG and it's image as files")
@click.option('-c', '--config-filepath', required=False, default=os.getenv('CONFIG_FILEPATH'), type=click.Path(exists=True))
@click.option('-o', '--output-dag-filepath', required=False, default=os.getenv('GRAPH_FILEPATH'), type=click.Path())
@click.option('-i', '--output-image-filepath', required=False, default=os.getenv('GRAPH_IMAGE_FILEPATH'), type=click.Path())
def create_dag(*args, **kwargs):
    logger.info(f'create_dag invoked with args: {kwargs}')
    _create_dag(*args, **kwargs)


@cli.command(help='Load DAG from file, run DAG for specified date, save results into database')
@click.option('-f', '--dag-filepath', required=False, default=os.getenv('GRAPH_FILEPATH'), type=click.Path(exists=True))
@click.option('-d', '--date', required=False, type=click.DateTime(['%Y-%m-%d']))
@click.option('-t', '--max-tasks', required=False, default=5, type=click.INT)
def insert_data(dag_filepath: str, date: datetime, max_tasks: int):
    if not date:
        date = (datetime.now() - timedelta(days=1))
    date = date.date()
    logger.info(f'insert_data invoked with args: {dict(date=str(date), dag_filepath=dag_filepath, max_tasks=max_tasks)}')
    dag = DAG.load_from_file(dag_filepath)
    dag.run(dt=date, max_tasks=max_tasks)


@cli.command(help='Export `rates` table into CSV-file')
@click.option('-f', '--output-filepath', required=False, default=os.getenv('DEFAULT_EXPORT_FILEPATH'), type=click.Path())
def export_table(output_filepath: str):
    logger.info(f'export_table invoked with args: {dict(output_filepath=output_filepath)}')
    data = fetch_data()
    data.to_csv(output_filepath, index=False)


if __name__ == '__main__':
    cli()

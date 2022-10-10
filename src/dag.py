from __future__ import annotations
from datetime import date
import pickle

from paradag import DAG as _DAG
from paradag import dag_run, MultiThreadProcessor
from graphviz import Digraph

from tasks import Task, TaskCalculateInsert, TaskDownloadInsert
from schema import load_config


class TaskExecutor:
    def __init__(self, dt: date, tasks: dict[str, Task]):
        self.dt = dt
        self.tasks = tasks

    def param(self, currency_code):
        return currency_code

    def execute(self, currency_code):
        self.tasks[currency_code].execute(self.dt)


class TaskSelector:
    def __init__(self, max_tasks: int = None):
        self.max_tasks = max_tasks

    def select(self, running, idle):
        if self.max_tasks:
            task_number = max(0, self.max_tasks - len(running))
            return list(idle)[:task_number]
        return list(idle)


class DAG:
    def __init__(self, tasks: dict[str, Task]):
        self._dag = _DAG()
        self._tasks = tasks

        self.add_node(*tasks.keys())
        for task in tasks.values():
            if hasattr(task, 'dependencies'):
                for dependency in task.dependencies:
                    self.add_dependency(dependency, task.currency_code)

    def add_node(self, *args):
        self._dag.add_vertex(*args)

    def add_dependency(self, *args):
        self._dag.add_edge(*args)

    def run(self, dt: date, max_tasks: int = None):
        return dag_run(
            self._dag,
            processor=MultiThreadProcessor(),
            selector=TaskSelector(max_tasks=max_tasks),
            executor=TaskExecutor(dt=dt, tasks=self._tasks)
        )

    def save_as_file(self, filepath: str):
        with open(filepath, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load_from_file(cls, filepath: str) -> DAG:
        with open(filepath, 'rb') as file:
            return pickle.load(file)

    def export_image(self, filepath: str) -> str:
        dot = Digraph()

        for node in self._dag.vertices():
            dot.node(node, node)
            for adjacent in self._dag.successors(node):
                dot.edge(node, adjacent)

        return dot.render(outfile=filepath, format='png', cleanup=True)


def create_dag(config_filepath: str,
               output_dag_filepath: str,
               output_image_filepath: str):
    config = load_config(config_filepath)

    tasks = {currency_code: TaskDownloadInsert(currency_code) for currency_code in config.downloadable}
    tasks |= {currency.code: TaskCalculateInsert(currency.code, currency.sql_filename, currency.dependencies) for
              currency in config.calculated}

    dag = DAG(tasks=tasks)

    dag.save_as_file(output_dag_filepath)
    dag.export_image(output_image_filepath)

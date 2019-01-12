import argparse
import os
import random

from gentasche import Dataset


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Generate data for description task scheduling"
    )
    parser.add_argument('tasks_number', type=int, help='number of tasks')
    parser.add_argument('processors_number', type=int, help=
                        'number of processors')
    parser.add_argument('-f', '--file', type=str, help='file to save data')

    args = parser.parse_args()
    n_tasks, n_processors = args.tasks_number, args.processors_number

    assert n_tasks > 0, "Number of tasks must be greater than 0"
    assert n_processors > 0, "Number of processors must be greater than zero"
    assert  n_tasks > n_processors, \
        "Number of task must be greater or equal than number of processors"
    if args.file is not None:
        file = args.file
    else:
        file = 'example_gen_data.data'
    dataset = Dataset.random(n_tasks, n_processors, file)
    dataset.save()

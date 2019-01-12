#!/usr/bin/python3
import argparse
import os
import random


def generate_data(n_tasks, n_processors, file='example_gen_data.data'):
    tasks = [random.randint(500000, 10000000) for _ in range(n_tasks)]
    processors = [random.randint(10, 35) * 100000 for _ in range(n_processors)]
    times_matrix = [[round(t / p, 3) for p in processors] for t in tasks]
    string = '\n'.join([str(n_tasks), str(n_processors)] + [
        ' '.join(map(str, times_row)) for times_row in times_matrix
    ])
    with open(file, 'w+') as f:
        f.write(string)
    print(f"Data saved succesfully in file: {file}")
    

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
    generate_data(n_tasks, n_processors, file)

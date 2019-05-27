Genetic Task Scheduling
=======================

Scheduling multiprocessor tasks with genetic algorithms.


## Goal

The goal of this student project was to resolve multiprocessor tasks scheduling problem using genetic algorithms. According to the task two python scripts have been created:

* gen_data.py - used for random dataset generation
* gentasche.py - used for performing evolution against given dataset.


## How to use

Use commands

    ./gen_data.py --help
    
and

    ./gentasche.py --help
    
to get help on proper using those scripts.


## Usage example

With command below generate dataset of processing times for 150 tasks and 8 processors,
and store it in file `example.data`:

    ./gen_data.py -f example.data 150 8

Then use `gentasche.py` script to run genetic algorithm against newly generated data
with default parameters:

    ./gentasche example.data

As a result you shuld see list of proceeding learning scores (time of processing
all tasks in given task/processor assignment, lower is better).
At the end of processing you should get fitness and score ofbest chromosome
generated through processing algorithm and it's genotype converted to table that
assigns tasks to particular processors.

You can try to get better solution by playing with algorithm parameters (listed
in gentasche.py help page):

    -p POPULATION_SIZE, --population-size POPULATION_SIZE (default 10)
    -c CROSSOVER_OPERATOR, --crossover-operator CROSSOVER_OPERATOR (default 75.0)
    -m MUTATION_OPERATOR, --mutation-operator MUTATION_OPERATOR (default 5.0)
    -r MAX_REPEATS, --max-repeats MAX_REPEATS (default 100)

Use flag `--show-plot` if you want to see results of processing in time on plotted chart.

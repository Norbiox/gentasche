#!/usr/bin/env python3
import argparse
import itertools
import math
import pandas as pd
import random
import time
from matplotlib import pyplot as plt
from pathlib import Path


def random_swap_in(l) -> list:
    assert len(l) >= 2, "list must have at least 2 elements"
    new_l = l.copy()
    i1, i2 = 0, 0
    while i1 == i2:
        i1 = random.randint(0, len(l) - 1)
        i2 = random.randint(0, len(l) - 1)
    new_l[i1], new_l[i2] = l[i2], l[i1]
    return new_l


class Dataset:
    """Dataset - input data for algorithm."""

    def __init__(self, name, n_tasks, n_processors, time_matrix, *args,
                 **kwargs):
        self.name = name
        self.n_tasks = n_tasks
        self.n_processors = n_processors
        self.time_matrix = time_matrix

    @classmethod
    def read(cls, filepath):
        file = Path(filepath)
        with open(file, 'r') as f:
            n_tasks = int(f.readline())
            n_processors = int(f.readline())
            t_matrix = [[float(t) for t in l.split()] for l in f.readlines()]
        return cls(file.name, n_tasks, n_processors, t_matrix)

    @classmethod
    def random(cls, n_tasks, n_processors, name='random_data'):
        if math.log2(n_processors) % 1.0:
            raise ValueError("Number of processors must be power of 2!")
        processors = [1.0e6, 1.5e6, 2.0e6, 2.5e6, 3.0e6, 3.5e6, 4.0e6, 5.0e6]
        if n_processors == 2:
            processors = [processors[1], processors[3]]
        elif n_processors == 4:
            processors = processors[::2]
        elif n_processors > 8:
            processors = sum([
                [p] * (n_processors // 8) for p in processors
            ], [])
        tasks = [random.randint(500000, 10000000) for _ in range(n_tasks)]
        time_matrix = [[round(t / p, 3) for p in processors] for t in tasks]
        print(processors, tasks)
        return cls(name, n_tasks, n_processors, time_matrix)

    def save(self, folder=None):
        if folder is not None:
            path = Path('/'.join([folder, self.name]))
        else:
            path = Path(self.name)
        content = '\n'.join(
            [str(self.n_tasks), str(self.n_processors)] +
            [' '.join([str(t) for t in l]) for l in self.time_matrix]
        )
        path.write_text(content)


class Chromosome(list):
    """Chromosome - tasks schedule representation.

    Chromosome is list of which index are the numbers of subsequent tasks and
    values are number of processors that handles each task.

    Eg. we have 3 processors ad 8 tasks, so possible chromosome may look like:

       [0, 2, 1, 1, 2, 1, 0, 1]

    so the task 4 is handled by processor 2.
    """

    def __init__(self, gens: list, *args, **kwargs):
        assert gens, "Chromosome cannot be empty"
        self.gens = gens
        list.__init__(self, self.gens)
        self._score = None

    @property
    def fitness(self):
        """Fitness - reversed score (processing time) of chromosome."""
        assert self.score is not None, "Chromosome is not scored"
        return 1 / self.score

    @property
    def score(self):
        """Score - overall time of processing tasks."""
        return self._score

    @score.setter
    def score(self, time):
        self._score = time

    @property
    def size(self):
        return len(self.gens)

    @classmethod
    def randomize(cls, n_tasks: int, n_processors: int):
        assert n_tasks > 0, "Number of tasks must be bigger than 0"
        assert n_processors > 0, "Number of processors must be bigger than 0"
        return cls([random.choice(list(range(n_processors)))
                    for i in range(n_tasks)])
 
    def crossover(self, other):
        if self == other:
            other.mutate()
            return [self, other]
        crossing_point = random.randint(1, self.size-1)
        new1 = self.gens[:crossing_point] + other.gens[crossing_point::]
        new2 = other.gens[:crossing_point] + self.gens[crossing_point::]
        return [self.__class__(new1), self.__class__(new2)]

    def mutate(self):
        self.gens[random.randint(0, self.size - 1)] = random.choice(
            list(set(self))
        )
        list.__init__(self, self.gens)

    def __str__(self):
        strings = [
            f"Chromosome with fitness {self.fitness} and score {self.score}",
            f"Table of processors tasks:"
        ]
        for p in set(self.gens):
            strings.append(f"processor {p}: " + ' '.join([
                str(i) for i in range(self.size) if self.gens[i] == p
            ]))
        strings.append(f"Overall processing time: {self.score}s")
        return '\n'.join(strings)


class Population(list):
    """Population - group of chromosomes of one generation."""

    def __init__(self, chromosomes: list, *args, **kwargs):
        self._rated = False
        self._chromosomes = chromosomes
        list.__init__(self, self.chromosomes)

    @property
    def best_chromosome(self):
        return sorted(self._chromosomes, key=lambda c: c.score)[0]

    @property
    def best_score(self):
        return self.best_chromosome.score

    @property
    def best_fitness(self):
        return self.best_chromosome.fitness

    @property
    def chromosomes(self):
        return self._chromosomes

    @property
    def is_rated(self):
        return self._rated

    @property
    def median_score(self):
        return self.scores.median()

    @property
    def scores(self):
        return pd.Series([ch.score for ch in self.chromosomes])

    @property
    def size(self):
        return len(self.chromosomes)

    @property
    def worst_score(self):
        return self.scores.max()

    @classmethod
    def randomize(cls, size, n_tasks, n_processors):
        chromosomes = [Chromosome.randomize(n_tasks, n_processors)
                       for _ in range(size)]
        return cls(chromosomes)

    def rate(self, dataset):
        for chromosome in self._chromosomes:
            processor_times = [0] * dataset.n_processors
            for task, proc in enumerate(chromosome):
                processor_times[proc] += dataset.time_matrix[task][proc]
            chromosome.score = max(processor_times)
        self._chromosomes = sorted(self.chromosomes, key=lambda ch: ch.score)
        list.__init__(self, self.chromosomes)
        self._rated = True

    def select_one(self, test_pick=None):
        assert self.is_rated, "Population must be rated before selection"
        bounds = list(itertools.accumulate(
            ch.fitness for ch in self.chromosomes
        ))
        pick = test_pick or random.random() * bounds[-1]
        return next(chromosome for chromosome,
                    bound in zip(self.chromosomes, bounds) if pick < bound)


class ArchivedPopulation():

    def __init__(self, population):
        self.best_chromosome = population.best_chromosome
        self.best_score = self.best_chromosome.score
        self.best_fitness = self.best_chromosome.fitness
        self.worst_score = population.scores.max()
        self.median_score = population.scores.median()


class GeneticTaskScheduler():

    def __init__(self, population_size=10, crossover_operator=75,
                 mutation_operator=5, max_repeats=100, archive=True,
                 show_plot=True,
                 *args, **kwargs):
        self.population_size = population_size
        self.crossover_operator = crossover_operator
        self.mutation_operator = mutation_operator
        self.max_repeats = max_repeats
        self.archive = archive
        self.show_plot = show_plot
        self.populations = []
        self.working_time = None

    # Genetic Algorithm Steps

    def selection(self, population):
        return sorted(
            [population.select_one() for _ in range(self.population_size)],
            key=lambda c: c.score
        )

    def crossover(self, population):
        new_population, reproducers = [], []
        survivor = population.pop(0)
        for c in population:
            if random.uniform(0, 100) <= self.crossover_operator:
                reproducers.append(c)
            else:
                new_population.append(c)
        if len(reproducers) % 2: new_population.append(reproducers.pop())
        random.shuffle(reproducers)
        for i in range(0, len(reproducers), 2):
            new_population += list(
                reproducers[i].crossover(reproducers[i + 1])
            )
        new_population.append(survivor)
        return new_population

    def mutation(self, population):
        i = 0
        for chromosome in population:
            if random.uniform(0, 100) <= self.mutation_operator:
                chromosome.mutate()
                i += 1
        return population

    # Other important stuff
    @property
    def best_of_all(self):
        return sorted(self.populations,
                      key=lambda p: p.best_score)[0].best_chromosome

    @property
    def repeats(self):
        return len(self.populations)

    @property
    def statistics(self):
        stats = pd.DataFrame([])
        stats['best_score'] = [p.best_score for p in self.populations]
        stats['worst_score'] = [p.worst_score for p in self.populations]
        stats['median_score'] = [p.median_score for p in self.populations]
        return stats

    def feed(self, dataset):
        if not isinstance(dataset, Dataset):
            dataset = Dataset.read(dataset)
        self.dataset = dataset

    def next_population(self):
        assert self.populations, "First create initial population"
        new_population = Population(
            self.mutation(
                self.crossover(
                    self.selection(
                        self.populations[-1]
                    )
                )
            )
        )
        new_population.rate(self.dataset)
        self.populations.append(new_population)
        print(f"Last best score: {new_population.best_chromosome.score}")
        if self.archive:
            previous_population = self.populations[-2]
            ap = ArchivedPopulation(previous_population)
            self.populations[-2] = ap
            del previous_population
        return new_population

    def plot_statistics(self):
        fig = plt.figure(figsize=(12, 6))
        fig.suptitle(
            f"Population size: {self.population_size}, " +
            f"crossover: {self.crossover_operator}%, " +
            f"mutation: {self.mutation_operator}%, " +
            f"processing time: {round(self.working_time, 3)}s",
            fontsize = 12
        )
        best_scores = self.statistics.best_score
        line, = plt.plot(best_scores, color='green', label='best scores')
        y = round(best_scores.min(), 3)
        x = best_scores[best_scores == best_scores.min()].index[0]
        line, = plt.plot(x, y, 'ro', label='best score')
        plt.text(x, y, str(y)+'s', fontsize=14, fontweight='bold')

        #line, = plt.plot(self.statistics.worst_score, color='red',
        #               label='worst scores')
        #line, = plt.plot(self.statistics.median_score, color='blue',
        #         label='median scores')
        plt.grid()
        plt.legend()
        if self.show_plot:
            plt.show()
        return fig

    def prepare(self, dataset=None):
        assert len(self.populations) <= 1, \
            "Cannot prepare already working scheduler"
        if dataset is not None:
            self.feed(dataset)
        if not self.populations:
            new_population = Population.randomize(
                self.population_size,
                self.dataset.n_tasks,
                self.dataset.n_processors
            )
            new_population.rate(self.dataset)
            self.populations.append(new_population)

    def schedule(self, dataset=None):
        t0 = time.time()
        self.prepare(dataset)
        while self.repeats < self.max_repeats:
            self.next_population()
        self.working_time = time.time() - t0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Run GeneticTaskScheduler against dataset"
    )
    parser.add_argument('dataset_file', type=str, help='dataset file path')
    parser.add_argument('-p', '--population-size', type=int, default=10)
    parser.add_argument('-c', '--crossover-operator', type=float, default=75.0)
    parser.add_argument('-m', '--mutation-operator', type=float, default=5.0)
    parser.add_argument('-r', '--max-repeats', type=int, default=100)
    parser.add_argument('--no-optimization', dest='optimize',
                        action='store_false')
    parser.add_argument('--show-plot', dest='show_plot', action='store_true')
    parser.set_defaults(optimize=True, show_plot=False)

    args = parser.parse_args()

    dataset = Dataset.read(args.dataset_file)
    gts = GeneticTaskScheduler(
        args.population_size, args.crossover_operator, args.mutation_operator,
        args.max_repeats, args.optimize, args.show_plot
    )
    gts.schedule(dataset)
    print(gts.best_of_all)
    print(f"Processing time: {gts.working_time}")
    fig = gts.plot_statistics()
    p = Path('images')
    p.mkdir(parents=True, exist_ok=True)
    fig.savefig(p / ('_'.join([
        args.dataset_file.split('/')[-1],
        'P' + str(args.population_size),
        'C' + str(args.crossover_operator).replace('.','_'),
        'M' + str(args.mutation_operator).replace('.', '_'),
        'R' + str(args.max_repeats),
        'T' + str(int(gts.working_time))
    ]) + '.png'))

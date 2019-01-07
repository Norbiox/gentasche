import random
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

    def crossover(self, other, crossing_point=None):
        if crossing_point is None:
            crossing_point = self.size // 2
        else:
            assert 0 < crossing_point < self.size - 1, \
                f"crossing_point must be between 0 and {self.size - 1}"
        new1 = self.gens[:crossing_point] + other.gens[crossing_point::]
        new2 = other.gens[:crossing_point] + self.gens[crossing_point::]
        return [new1, new2]

    def mutate(self):
        self.gens = random_swap_in(self.gens)
        list.__init__(self, self.gens)


class Population(list):
    """Population - group of chromosomes of one generation."""

    def __init__(self, chromosomes: list, *args, **kwargs):
        self.chromosomes = chromosomes
        list.__init__(self, self.chromosomes)

    @classmethod
    def randomize(cls, size, n_tasks, n_processors):
        chromosomes = [Chromosome.randomize(n_tasks, n_processors)
                       for _ in range(size)]
        return cls(chromosomes)


class GeneticTaskScheduler():

    def __init__(self, population_size=10, mutation_ratio=5, repeats=100,
                 *args, **kwargs):
        self.__repeats = 0
        self.population_size = population_size
        self.mutation_ratio = mutation_ratio
        self.repeats = repeats
        self.populations = []
    
    def feed(self, dataset):
        if not isinstance(dataset, Dataset):
            dataset = Dataset.read(dataset)
        self.dataset = dataset

    def next_generation(self):
        pass

    def rate(self, chromosome):
        processor_times = [0] * self.dataset.n_processors
        for task, proc in enumerate(chromosome):
            processor_times[proc] += self.dataset.time_matrix[task][proc]
        chromosome.score = max(processor_times)

    def schedule(self, dataset=None):
        if dataset is not None:
            self.feed(dataset)
        if not populations:
            populations.append(Population.randomize(
                population_size,
                self.dataset.n_tasks,
                self.dataset.n_processors
            ))


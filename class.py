import random

""" tasks example for 4 tasks and 2 processors
tasks = [
	[1,1.5],
	[4,3],
	[2,2.1],
	[6,3,9]
]
"""

FILEPATH = "examples/example1.data"
COUNT = 20
REPEATS = 100
MUTATION_RATIO = 5


def random_swap_in(list) -> list:
	assert len(list) >= 2, "list must have at least 2 elements"
	i1,i2 = 0,0
	while i1 == i2:
		i1 = random.randint(0,len(list)-1)
		i2 = random.randint(0,len(list)-1)
	list[i1],list[i2] = list[i2],list[i1]
	return list


class Chromosome(list):

	def __init__(self, gens:list, *args, **kwargs):
		assert gens, "Chromosome cannot be empty"
		self.gens = gens
		list.__init__(self, self.gens)
		self._score = None


	@property
	def score(self):
		return self._score
	
	@score.setter
	def score(self, points):
		assert isinstance(points, float), "score must be a floating point number"
		self._score = points


	@property
	def size(self):
		return len(self.gens)


	@classmethod
	def random_gens(cls, size:int, gen_types:int):
		assert size > 0, "Chromosome must be at least 1 gen long"
		assert gen_types > 0, "Chromosome must have some gen types defined"
		return cls([random.choice(gen_types) for i in range(size)])


	def crossover(self, other):
		new1 = self.gens[:self.size//2] + other.gens[other.size//2::]
		new2 = other.gens[:other.size//2] + self.gens[self.size//2::]
		return [new1, new2]


	def mutate(self):
		self.gens = random_swap_in(self.gens)



class Population:


	def __new__(cls, size:int, mutation_ratio:int, tasks:list, processors:list, \
		chromosomes=[], *args, **kwargs):
		if not chromosomes:
			chromosomes = cls.randomize(size, tasks, processors)
		return cls(size, mutation_ratio, tasks, processors, chromosomes, *args, **kwargs)


	def __init__(self, size:int, mutation_ratio:int, tasks:list, processors:list, \
		chromosomes:list, *args, **kwargs):
		self.size = size
		self.mutation_ratio = mutation_ratio
		self.tasks = tasks
		self.processors = processors_number
		self._chromosomes = chromosomes
		self.get_scores()


	@classmethod
	def perform_mutations(cls, chromosomes, ratio):
		for chromosome in chromosomes:
			if random.randint(1,100) <= self.mutation_ratio:
				chromosome.mutate()
		return chromosomes


	@classmethod
	def randomize(cls, size, tasks, processors) -> list:
		chromosomes = []
		for i in range(size):
			tasks_number = len(tasks)
			chromosome = Chromosome.random_gens(tasks_number, processors)
			chromosomes.append(chromosome)
		return chromosomes


	def get_scores(self):
		for chromosome in self._chromosomes:
			chrom_scores = [0 for i in range(processors)]
			for i,gen in enumerate(chromosome):
				chrom_scores[gen] += self.tasks[i][gen]
			chromosome.score = max(chrom_scores)


	def next(self):
		best_chromosomes = sorted(self._chromosomes, key=score)[:self.size//2]
		for i in range(0,self.size//2,2):
			chrom1 = best_chromosomes[i]
			chrom2 = best_chromosomes[i+1]
			best_chromosomes += chrom1.crossover(chrom2)
		new_chromosomes = self.perform_mutations(best_chromosomes, self.mutation_ratio)
		return self.__class__(self.size, self.mutation_ratio, self.tasks, \
			self.processors, new_chromosomes)


	def __iter__(self):
		return iter(self._chromosomes)


	def __contains__(self, elem):
		return elem in self._chromosomes
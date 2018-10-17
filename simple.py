import random


FILEPATH = "examples/example1.data"
POPULATIONSIZE = 20
REPEATS = 100
MUTATION_RATIO = 5


def random_chromosome(tasks_number, processors_number):
	return [random.randint(0,processors_number-1) for i in range(tasks_number)]


def score(tasks, processors_number, chromosome):
	proc_time = [0 for i in range(processors_number)]
	for task,processor in enumerate(chromosome):
		proc_time[processor] += tasks[task][processor]
	return round(max(proc_time), 2)


def mutate(population, processors_number):
	for i,chromosome in enumerate(population):
		for j,gene in enumerate(chromosome):
			if random.randint(1,100) <= MUTATION_RATIO:
				population[i][j] = random.randint(0,processors_number-1)
	return population



def cross_population(population, tasks, processors_number):
	scored = sorted(population, key=lambda c: score(tasks, processors_number, c))
	scored = scored[:len(scored)//2]
	random.shuffle(scored)
	for i in range(0, len(scored), 2):
		chrom1 = scored[i]
		chrom2 = scored[i+1]
		scored.append(chrom1[:len(chrom1)//2] + chrom2[len(chrom2)//2::])
		scored.append(chrom2[:len(chrom2)//2] + chrom1[len(chrom1)//2::])
	return scored



def read_input_file(filepath):
	with open(filepath, 'r') as f:
		content = f.readlines()
	tasks_number = int(content[0])
	procs_number = int(content[1])
	tasks = [list(map(float, line.split()[1::])) for line in content[2::]]
	return tasks_number, procs_number, tasks



def main():
	tasks_number, procs_number, tasks = read_input_file(FILEPATH)
	population = [random_chromosome(tasks_number,procs_number) for i in range(POPULATIONSIZE)]
	# TODO: scores are sorted, but no population
	for i in range(REPEATS):
		scores = sorted([score(tasks, procs_number, chrom) for chrom in population])
		print("best of {}: {}".format(i, ' ; '.join(map(str, scores[:10]))))
		population = mutate(population, procs_number)
		population = cross_population(population, tasks, procs_number)


main()
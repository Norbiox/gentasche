import gentasche as gts
import pytest


def test_chromosome_crossover():
    chr1 = gts.Chromosome([0, 0, 0, 0, 0])
    chr2 = gts.Chromosome([1, 1, 1, 1, 1])
    with pytest.raises(AssertionError):
        chr1.crossover(chr2, 0)
    with pytest.raises(AssertionError):
        chr1.crossover(chr2, 5)
    chr3, chr4 = chr1.crossover(chr2)
    assert chr3 == [0, 0, 1, 1, 1]
    assert chr4 == [1, 1, 0, 0, 0]
    chr5, chr6 = chr2.crossover(chr1, 4)
    assert chr5 == [1, 1, 1, 1, 0]
    assert chr6 == [0, 0, 0, 0, 1]


def test_population_sorting():
    pop = gts.Population.randomize(5, 3, 2)
    for chromosome, score in zip(pop, [4, 1, 3, 2, 5]):
        chromosome.score = score
    pop.sort()
    assert [ch.score for ch in pop.chromosomes] == [1, 2, 3, 4, 5]


def test_population_select_one():
    pop = gts.Population.randomize(5, 3, 2)
    for chromosome, score in zip(pop, [1, 2, 3, 4, 5]):
        chromosome.score = score
    selected = pop.select_one(1.9)
    assert selected.score == 4
    selected = pop.select_one()
    assert selected.score in [1, 2, 3, 4, 5]


def test_random_swap_in():
    chromosome = [1, 2, 3, 4, 5, 6]
    new_chromosome = gts.random_swap_in(chromosome)
    assert new_chromosome != chromosome
    assert set(new_chromosome) == set(chromosome)


def test_reading_dataset_file(tmpdir):
    p = tmpdir / 'data.data'
    content = "3\n2\n1 2\n4 5\n7 8"
    p.write(content)
    filepath = p.strpath
    dataset = gts.Dataset.read(filepath)
    assert dataset.name == 'data.data'
    assert dataset.n_tasks == 3
    assert dataset.n_processors == 2
    assert dataset.time_matrix[1][1] == 5.0


def test_randomizing_population():
    pop = gts.Population.randomize(12, 4, 2)
    assert len(pop) == 12
    assert len(pop[0]) == 4
    assert 3 not in pop[0]


def test_scheduler_rating_function():
    chromosome = gts.Chromosome([0, 1, 0])
    dataset = gts.Dataset('test_dataset', 3, 2, [[1, 2], [3, 4], [5, 6]])
    GTS = gts.GeneticTaskScheduler()
    GTS.feed(dataset)
    GTS.rate(chromosome)
    assert chromosome.score == 6.0


def test_scheduler_selection():
    population = gts.Population.randomize(12, 3, 2)
    dataset = gts.Dataset('test_dataset', 3, 2, [[1, 2], [3, 4], [5, 6]])
    GTS = gts.GeneticTaskScheduler()
    GTS.feed(dataset)
    GTS.rate_population(population)
    new_population = GTS.selection(population)
    assert len(new_population) == GTS.population_size
    for ch in new_population:
        assert ch in population


def test_scheduler_next_population():
    dataset = gts.Dataset('test_dataset', 3, 2, [[1, 2], [3, 4], [5, 6]])
    GTS = gts.GeneticTaskScheduler()
    GTS.prepare(dataset)
    GTS.next_population()
    assert len(GTS.populations) == 2
    pop1, pop2 = GTS.populations[0], GTS.populations[1]
    assert pop1.size == pop2.size

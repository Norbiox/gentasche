import gentasche as gts


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
    chromosome = gts.Chromosome([0,1,0])
    dataset = gts.Dataset('test_dataset', 3, 2, [[1, 2], [3, 4], [5, 6]])
    GTS = gts.GeneticTaskScheduler()
    GTS.feed(dataset)
    GTS.rate(chromosome)
    assert chromosome.score == 6.0

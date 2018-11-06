import unittest
from copy import copy
from gentasche.lib import *


class RandomSwapInTestCase(unittest.TestCase):

	def test_ok_with_list_of_numbers_from_0_to_10(self):
		lista = list(range(10))
		lista2 = random_swap_in(lista)
		self.assertEqual(len(lista), len(lista2))
		for i in lista:
			self.assertIn(i, lista2)

	def test_raises_when_list_is_empty(self):
		lista = []
		with self.assertRaises(AssertionError):
			random_swap_in(lista)

	def test_raises_when_list_has_only_one_element(self):
		lista = [1]
		with self.assertRaises(AssertionError):
			random_swap_in(lista)


class ChromosomeTestCase(unittest.TestCase):


	def test_randomize_chromosome(self):
		chromosome = Chromosome.random_gens(1000, 5)
		self.assertEqual(len(chromosome), 1000)
		for gen in chromosome:
			self.assertIn(gen, list(range(5)))

	def test_crossover(self):
		chrom1 = Chromosome([0,1,2,3,4,5,6,7,8,9])
		chrom2 = Chromosome([10,11,12,13,14,15,16,17,18,19])
		chrom3,chrom4 = chrom1.crossover(chrom2)
		chrom5,chrom6 = chrom2.crossover(chrom1)
		self.assertEqual(chrom3, Chromosome([0,1,2,3,4,15,16,17,18,19]))
		self.assertEqual(chrom4, Chromosome([10,11,12,13,14,5,6,7,8,9]))
		self.assertEqual(chrom3, chrom6)
		self.assertEqual(chrom4, chrom5)

	def test_mutate(self):
		chrom = Chromosome([1,2,3,4,5,6])
		new_chrom = copy(chrom)
		new_chrom.mutate()
		self.assertNotEqual(chrom, new_chrom)


class SmallPopulationTestCase(unittest.TestCase):

	def setUp(self):
		size = 10
		self.tasks = [
			[1,2,3,4],
			[5,6,7,8],
			[9,10,11,12],
			[13,14,15,16]
		]
		self.chromosomes = [Chromosome.random_gens(4, 4) for i in range(size)]
		self.population = Population(0, size=size, mutation_ratio=2, processors=4, \
			tasks=self.tasks, chromosomes=self.chromosomes)


	def test_population_autoscores(self):
		for chrom in self.population:
			self.assertGreater(chrom.score, 0)


	def test_population_get_scores(self):
		tasks = [[1,2],[3,4]]
		chroms = [
			Chromosome([0,0]), 
			Chromosome([0,1]), 
			Chromosome([1,1]), 
			Chromosome([1,0])
		]
		pop = Population(1, 4, 5, 2, tasks, chroms)
		expected_scores = [4, 4, 6, 3]
		for i,chrom in enumerate(pop):
			self.assertEqual(chrom.score, expected_scores[i])
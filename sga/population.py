from .chromosome import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import figure
import numpy as np


class Population(object):

    def __init__(self, m: int, n: int, chromosome_class: Chromosome):
        self._m = m
        self._n = n
        self._chromosome = chromosome_class
        self._population = [self._chromosome.random_chromosome() for _ in range(m)]
        self._current_fitness = None

    @property
    def population(self):
        return self._population

    @property
    def fitness(self):
        return self._current_fitness

    @fitness.setter
    def fitness(self, x):
        self._current_fitness = x

    def calculate_fitness(self, fitness_function, *args, **kwargs):
        if "archive" in kwargs:
            result = []
            for member in self._population:
                if kwargs["archive"]["chromosome"].str.contains(member).any():
                    result.append(kwargs["archive"]["fitness"][kwargs["archive"]["chromosome"] == member])
                else:
                    result.append(fitness_function(*self._chromosome.parameters(member), *args))
        else:
            return [fitness_function(*self._chromosome.parameters(member), *args) for member in self._population]

    def crossover(self, crossover_function, *args):
        children_population = Population(self.m, self.n, self._chromosome)
        children_population.contestants = crossover_function(self._population, self.n, *args)
        return children_population

    def mutate(self, rate=0.001):
        for idx, individual in enumerate(self._population):
            self._population[idx] = self._chromosome.mutate(individual) if random.uniform(0, 1) <= rate else \
                self._population[idx]

    # def selection_function(m, contestants, fitness, *args):
    def selection(self, selection_function, *args):
        idx_selected, selected = selection_function(self.m, self.contestants, self.fitness, *args)
        return idx_selected, selected

    @property
    def m(self):
        return self._m

    @property
    def n(self):
        return self._n

    @property
    def contestants(self):
        return self._population

    @contestants.setter
    def contestants(self, x):
        self._population = x


class BatchPopulation(Population):

    def __init__(self, m: int, n: int, chromosome_class: Chromosome):
        super().__init__(m, n, chromosome_class)

    def crossover(self, crossover_function, *args):
        children_population = BatchPopulation(self.m, self.n, self._chromosome)
        children_population.contestants = crossover_function(self._population, self.n, *args)
        return children_population

    def calculate_fitness(self, fitness_function, *args, **kwargs):
        result = []
        for member in self._population:
            # print(kwargs["archive"])

            if kwargs["archive"]["chromosome"].str.contains(member).any():  # Get from archive if present.
                # print(kwargs["archive"]["fitness"][kwargs["archive"]["chromosome"] == member].iloc[0])
                result.append(kwargs["archive"]["fitness"][kwargs["archive"]["chromosome"] == member].iloc[0])


            else:
                result.append(fitness_function(*self._chromosome.parameters(member), *args))

        # print(result)
        return result

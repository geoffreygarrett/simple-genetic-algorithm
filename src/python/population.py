from chromosome import *


class Population(object):

    def __init__(self, m: int, n: int, chromosome_class: Chromosome):
        self._m = m
        self._n = n
        self._chromosome = chromosome_class
        self._population = [self._chromosome.random_chromosome() for _ in range(m)]

    def fitness(self, fitness_function, *args):
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

    def selection(self, selection_function, fitness_function, *args):
        return selection_function(self.m, self.contestants, self.fitness(fitness_function), *args)

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


def convergence_termination(population_fitness, convergence_ratio):
    return True if abs((np.max(population_fitness) - np.mean(population_fitness)) / np.mean(
        population_fitness)) <= convergence_ratio / 2 else False


class EvolutionaryStrategy(object):
    def __init__(self, population, fitness_function, crossover_function, selection_function,
                 termination_criteria):
        self.population = population
        self.fitness_function = fitness_function
        self.crossover_function = crossover_function
        self.selection_function = selection_function
        self.termination_criteria = termination_criteria
        self.generation_number = 0
        self.children = None

    def perform_crossover(self, population):
        return population.crossover(self.crossover_function)

    def perform_mutation(self, population):
        population.mutate()

    def perform_selection(self, population):
        population.contestants = population.selection(self.selection_function, self.fitness_function)

    def get_population_fitness(self):
        return self.population.fitness(self.fitness_function)

    def get_average_fitness(self):
        return float(np.mean(self.get_population_fitness()))

    def get_maximum_fitness(self):
        return np.max(self.get_population_fitness())

    def get_fittest_chromosome(self):
        return np.array(self.population.contestants)[
            np.array(self.get_population_fitness()) == self.get_maximum_fitness()][0]

    def get_fittest_solution(self):
        return self.population._chromosome.parameters(self.get_fittest_chromosome())

    def evolve(self, verbose=False):
        while self.termination_criteria(self.population.fitness(self.fitness_function), 0.01) is False:
            self.children = self.perform_crossover(self.population)
            self.perform_mutation(self.children)
            self.population.contestants += self.children.contestants
            self.perform_selection(self.population)
            self.generation_number += 1
            if verbose:
                print("GEN: ",
                      str(self.generation_number).ljust(5),
                      "   ||   ",
                      "MAX_FIT: ",
                      str(np.round(self.get_maximum_fitness(), 4)).ljust(10),
                      "   ||   ",
                      "AVG_FIT: ",
                      str(np.round(self.get_average_fitness(), 4)).ljust(10),
                      "   ||   ",
                      "CHROMOSOME: ",
                      str(self.get_fittest_chromosome()).ljust(15),
                      "   ||   ",
                      "BEST_SOLN: ",
                      str(self.get_fittest_solution())
                      ),


if __name__ == "__main__":
    from gene import *
    from chromosome import *
    from helper import *

    # Acts as a singleton class. Only one is instantiated.
    ChromosomeTest = Chromosome(
        [
            LinearRangeGene(0, 5, 320),  # Parameter 1
            LinearRangeGene(0, 5, 320)  # Parameter 2
        ]
    )

    # Population definition
    PopulationTest = Population(100, 20, ChromosomeTest)

    # Evolutionary Strategy Test
    EvolutionaryStrategyTest = EvolutionaryStrategy(PopulationTest, fitness_function_himmelblau, polygamous_crossover,
                                                    selection_function_elite, convergence_termination)

    # Evolve Test
    EvolutionaryStrategyTest.evolve(verbose=True)

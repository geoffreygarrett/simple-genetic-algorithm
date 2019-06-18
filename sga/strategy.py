import numpy as np
import pandas as pd


class EvolutionaryStrategy(object):
    def __init__(self, population, fitness_function, crossover_function, selection_function,
                 termination_criteria, mutation_rate, colonize=False):
        """
        :param population:
        :param fitness_function:
        :param crossover_function:
        :param selection_function:
        :param termination_criteria:
        :param mutation_rate:
        :param colonize:
        """
        self.population = population
        self.fitness_function = fitness_function
        self.crossover_function = crossover_function
        self.selection_function = selection_function
        self.termination_criteria = termination_criteria
        self.mutation_rate = mutation_rate
        self.generation_number = 0
        self.children = None
        self._archive = pd.DataFrame(columns=["fitness", "chromosome"])

    def perform_crossover(self, population, *args):
        """
        :param population:
        :return:
        """
        return population.crossover(self.crossover_function, *args)

    def perform_mutation(self, population):
        population.mutate(self.mutation_rate)

    def perform_selection(self, population):
        idx_selected, selected = population.selection(self.selection_function)
        population.contestants = list(selected)
        population.fitness = list(np.array(population.fitness)[idx_selected])

    def get_average_fitness(self):
        return float(np.mean(self.population.fitness))

    def get_maximum_fitness(self):
        return np.max(self.population.fitness)

    def get_minimum_fitness(self):
        return np.min(self.population.fitness)

    def get_fittest_chromosome(self):
        return list(set(np.array(self.population.contestants)[
                            np.array(self.population.fitness) == self.get_maximum_fitness()]))

    def get_fittest_solution(self):
        return list(set([tuple(self.population._chromosome.parameters(c)) for c in self.get_fittest_chromosome()]))

    def evolve(self, verbose=False, return_log=False, **kwargs):
        if return_log:
            log = []

        self.population.fitness = self.population.calculate_fitness(self.fitness_function, archive=self._archive, **kwargs)

        while self.termination_criteria(self.population.fitness, self.generation_number) is False:

            if verbose:
                print("GEN: ",
                      str(self.generation_number).ljust(5),
                      "   ||   ",
                      "MAX_FIT: ",
                      str(np.round(self.get_maximum_fitness(), 4)).ljust(10),
                      "   ||   ",
                      "MIN_FIT: ",
                      str(np.round(self.get_minimum_fitness(), 4)).ljust(10),
                      "   ||   ",
                      "AVG_FIT: ",
                      str(np.round(self.get_average_fitness(), 4)).ljust(10),
                      "   ||   ",
                      "CHROMOSOME: ",
                      str(self.get_fittest_chromosome()).ljust(15),
                      "   ||   ",
                      "BEST_SOLN: ",
                      str(self.get_fittest_solution()),
                      ),

            if return_log:
                log.append([self.generation_number,
                            np.round(self.get_maximum_fitness(), 3),
                            np.round(self.get_minimum_fitness(), 3),
                            np.round(self.get_average_fitness(), 3),
                            self.get_fittest_chromosome()[0],
                            np.round(self.get_fittest_solution()[0], 3)])

            self._archive = self._archive.append(pd.DataFrame({
                "fitness": self.population.fitness,
                "chromosome": self.population.contestants,
                "generation": [self.generation_number] * len(self.population.contestants)
            })).drop_duplicates()

            # Make children from first initial generation of (16)
            self.children = self.perform_crossover(self.population)

            # Potentially mutate all children.
            self.perform_mutation(self.children)

            # Add list of children to initial population.
            self.population.contestants += self.children.contestants

            # Calculate and add the children fitness to population list.
            self.population.fitness += self.children.calculate_fitness(self.fitness_function, archive=self._archive, **kwargs)

            # Comment.
            self.perform_selection(self.population)

            # Increase gen count.
            self.generation_number += 1

        if verbose:
            print("\n" + "--" * 100 + "\n")

        if return_log:
            df = pd.DataFrame(log,
                              columns=
                              """Generation,Maximum Fitness,Minimum Fitness,Average Fitness,Chromosome,Best Solution""".split(
                                  ","))

            df = df.set_index("Generation")
            return df

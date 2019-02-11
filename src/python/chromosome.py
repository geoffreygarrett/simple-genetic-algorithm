import bitarray
import struct
import numpy
import re
import random


class Chromosome(object):

    def __init__(self, genes):
        self._genes = genes

    def mutate(self, chromosome):
        gene_list = chromosome.split(' ')
        idx = random.choice(range(len(gene_list)))
        gene_list[idx] = self._genes[idx].mutate(gene_list[idx])
        return ' '.join(gene_list)

    def random_chromosome(self):
        return ' '.join([gene.random_gene() for gene in self._genes])

    def parameters(self, chromosome):
        gene_list = chromosome.split(' ')
        return [gene.transform(_gene) for gene, _gene in zip(self._genes, gene_list)]

    def crossover(self, chromosome1, chromosome2):
        sequence1 = chromosome1.split(' ')
        sequence2 = chromosome2.split(' ')
        array = [sequence1, sequence2]
        transpose = [1, 0]
        idx_child1 = [random.randint(0, 1) for _ in range(len(sequence1))]
        idx_child2 = [transpose[i] for i in idx_child1]
        child1 = [array[idx_child1[i]][i] for i, j in enumerate(idx_child1)]
        child2 = [array[idx_child2[i]][i] for i, j in enumerate(idx_child2)]
        return ' '.join(child1), ' '.join(child2)


if __name__ == "__main__":
    from gene import *

    # Acts as a singleton class. Only one is instantiated.
    ChromosomeTest = Chromosome(
        [
            LinearRangeGene(0, 5, 32),  # Parameter 1
            LinearRangeGene(0, 5, 32)  # Parameter 2
            # LinearRangeGene(0, 0.5, 0.001),  # Parameter 3
            # LinearRangeGene(0, 0.5, 0.001),  # Parameter 4
            # BinaryGene(),  # Parameter 5
            # BinaryGene(),  # Parameter 6
            # BitarrayGene(10)  # Parameter 7
        ]
    )

    # Singleton class generates a binary form of a chromosome.
    generatedChromosome = ChromosomeTest.random_chromosome()

    # Mutation Testing
    mutatedChromosome = generatedChromosome
    print("MUTATION TESTING")
    for _ in range(10):
        mutatedChromosome = ChromosomeTest.mutate(mutatedChromosome)
        print(mutatedChromosome)
        print(ChromosomeTest.parameters(mutatedChromosome))
        # Roughly Verified
    #
    # print('\n')
    #
    # childChromosome1 = generatedChromosome
    # childChromosome2 = mutatedChromosome
    #
    # # Crossover Testing
    # for i in range(30):
    #     print("-" * 90)
    #     print("Test ", i)
    #     print("Parent 1: ".ljust(20), childChromosome1)
    #     print("Parent 2: ".ljust(20), childChromosome2)
    #     print("=" * 90)
    #     childChromosome1, childChromosome2 = ChromosomeTest.crossover(childChromosome1, childChromosome2)
    #     print("Child 1: ".ljust(20), childChromosome1)
    #     print("Child 2: ".ljust(20), childChromosome2)

import bitarray
import random
import numpy as np
import math


class _BaseGene(object):
    """

    """

    @staticmethod
    def mutate(_gene):
        """
        :param _gene:
        :return:
        """
        binary_list = list(_gene)
        idx = random.choice(range(len(_gene)))
        binary_list[idx] = '0' if binary_list[idx] is '1' else '1'
        return ''.join(binary_list)

    @staticmethod
    def random_gene():
        """

        :return:
        """
        raise NotImplemented("random() Not implemented in _BaseGene")

    def __repr__(self):
        return type(self).__name__ + "(" + "val=" + str(self.value) + ", " + "gene=" + str(self) + ")"

    def __str__(self):
        return str()

    def transform(self, _gene):
        return _gene

    @property
    def value(self):
        return self.transform(_gene=self._gene)


class BinaryGene(_BaseGene):
    """
    Single boolean
    """

    @staticmethod
    def random_gene():
        return str(random.randint(0, 1))


class BitarrayGene(_BaseGene):
    """
    Sequence of booleans
    """

    def __init__(self, n_bits):
        self._n_bits = n_bits

    def random_gene(self):
        return bitarray.bitarray('0' * self._n_bits, endian='little').to01()


class LinearRangeGene(_BaseGene):
    """
    -32,767 to 32,767
    """

    def __init__(self, start, stop, num, endpoint=True, retstep=False, dtype=None):
        """
        :param start: Lower bound for search
        :param stop: Upper bound for search
        :param a_res: Minimum absolute resolution required
        :param endpoint:
        :param retstep:
        :param dtype:
        """
        self._num = num
        self._linear_space = np.linspace(start, stop, num=self._num, endpoint=endpoint, retstep=retstep,
                                         dtype=dtype)
        self._lower_bound = start
        self._upper_bound = stop

    # Inherited mutate member function must be over-written for linear boundaries.
    def mutate(self, _gene):
        """
        :param _gene:
        :return:
        """
        mutated = _BaseGene.mutate(_gene)
        while True:
            try:
                self.transform(mutated)
            except IndexError:
                mutated = _BaseGene.mutate(_gene)
            else:
                break
        return mutated

    def random_gene(self):
        _format = '{' + '0:0{}b'.format(len(bin(self._num)[2:])) + '}'
        return _format.format(random.randint(0, self._num))

    def transform(self, _gene):
        return self._linear_space[int(_gene, 2)-1]

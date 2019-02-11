import numpy as np


def selection_function_elite(m, contestants, fitness, *args):
    return list(np.array(contestants)[np.argpartition(np.array(fitness), -m)[-m:]])


def fitness_function_himmelblau(x, y):  # execute himmelblau function
    f = (x ** 2. + y - 11.) ** 2. + (x + y ** 2. - 7.) ** 2.
    return - f


def polygamous_crossover(parents, n_children, *args):
    gene_lst = []
    child_ls = []
    for gene_idx in range(len(parents[0].split(' '))):
        gene_col = np.random.choice(np.array([parent.split(' ') for parent in parents])[:, gene_idx], n_children)
        gene_lst.append(gene_col)
        # gene_mat = np.concatenate((gene_mat, gene_col), axis=1) if gene_mat is not None else gene_col
    gene_arr = np.array(gene_lst).T
    for child_idx in range(len(gene_arr[:, 0])):
        child_new = ' '.join(list(gene_arr[child_idx, :]))
        child_ls.append(child_new)
    return child_ls

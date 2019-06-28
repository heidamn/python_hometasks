import numpy
import multiprocessing


def divider(tree: list):
    ''' Делит дерево на две половины'''
    small_trees = []
    for i, branch in enumerate(tree[1]):
        if isint(branch):
            if i + 1 == len(tree):
                small_trees.append([branch])
            elif isint(tree[1][i+1]):
                small_trees.append(branch)
        else:
            small_trees.append(branch)
    return small_trees

def isint(s: any):
    ''' Проверка int или []'''
    try:
        int(s)
        return True
    except:
        return False

def leaf(tree: list):
    '''поиск листьев в дереве'''
    leaves = []
    for i, branch in enumerate(tree):
        if isint(branch):
            if i + 1 == len(tree):
                leaves.append(branch)
            elif isint(tree[i+1]):
                leaves.append(branch)
        else:
            leaves.extend(leaf(branch))
    return leaves

def mpleaf(tree: list, return_list: list):
    """собираем данные в словарь"""
    return_list.append(leaf(tree))

def leaf_sum(leaves: list):
    '''суммируем'''
    return numpy.sum(leaves)

def main(tree: list):
    small_trees = divider(tree)
    manager = multiprocessing.Manager()
    return_list = manager.list()
    jobs = []

    for small_tree in small_trees:
        p = multiprocessing.Process(target=mpleaf, args=(small_tree, return_list))
        jobs.append(p)
        p.start()
    for proc in jobs:
        proc.join()
    return leaf_sum(return_list)

if __name__ == '__main__':
    tree = [1, [2, [4, [7, 8]], 3, [5, 6, [9]]]]
    print(main(tree))
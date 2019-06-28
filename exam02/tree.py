import numpy

tree = [1, [2, [4, [7, 8]], 3, [5, 6, [9]]]]


def leaf(tree: list):
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

def isint(s: any):
    try:
        int(s)
        return True
    except:
        return False


print(numpy.sum(leaf(tree)))
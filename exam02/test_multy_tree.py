from typing import Dict, Set
from operator import itemgetter
from collections import Counter
import unittest
import multy_tree


class Test_Tree(unittest.TestCase):
    def setUp(self):
        self.tree = [1, [2, [4, [7, 8]], 3, [5, 6, [9]]]]

    def test_can_divide(self):
        tree = self.tree
        divided = multy_tree.divider(tree)
        self.assertEqual(divided, [[4, [7, 8]], [5, 6, [9]]])

    def test_int_check(self):
        self.assertEqual(multy_tree.isint(1), True)
        self.assertEqual(multy_tree.isint([1,2]), False)
        self.assertEqual(multy_tree.isint([1]), False)


    def test_find_sum(self):
        self.assertEqual(multy_tree.main(self.tree), 29)


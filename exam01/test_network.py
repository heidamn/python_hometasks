from typing import Dict, Set
from operator import itemgetter
from collections import Counter
import igraph
import unittest

from network import Network

class TestNetwork(unittest.TestCase):
    def setUp(self):
        self.users = [i for i in range(15)]
        self.friendships = [
            (1, 2), (2, 1),
            (1, 3), (3, 1),
            (1, 4), (4, 1),
            (1, 5), (5, 1),
            (1, 6), (6, 1),
            (1, 7), (7, 1),
            (1, 8), (8, 1),
            (1, 9), (9, 1),
            (1, 10), (10, 1),
            (2, 13), (13, 2),
            (13, 14), (14, 13),
            (14, 15), (15, 14),
            (10, 7), (7, 10),
            (14, 6), (6, 14),
        ]

    def test_can_add_user(self):
        net = Network()
        net.add_person(1)
        net.add_person(20)
        for i in range(5,8):
            net.add_person(i)
        users = net.users
        self.assertEqual([1, 20, 5, 6, 7], users)

    def test_can_add_friendship(self):
        net = Network()
        net.users = self.users
        net.friendships = self.friendships
        net.add_relation(11, 10)
        self.assertEqual(30, len(net.friendships))

    def test_can_find_route(self):
        net = Network()
        net.users = self.users
        net.friendships = self.friendships
        route1 = net.find_route(11, 10)
        route2 = net.find_route(14, 1)
        route3 = net.find_route(2, 13)
        self.assertEqual(0, route1[1])
        self.assertEqual([14, 6, 1], route2[0])
        self.assertEqual(3, route2[1])
        self.assertEqual([2, 13], route3[0])
        self.assertEqual(2, route3[1])

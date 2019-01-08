"""
Экзаменационная работа по программированию, Шоломов Даниил, k3140, ИТМО, 2018
Программма создает подобие социальной сети, имеются возможности добавления пользователей и дружеских
связей, вывода информации о пользователях и поиска пути между двумя пользователями.
"""
from typing import Tuple, Any
import igraph

class Network:
    """
    Социальная сеть
    """

    def __init__(self):
        self.users = []
        self.friendships = []

    def add_person(self, person_id: int) -> None:
        """
        Регистрация нового пользователя в социальной сети

        :param person_id: Идентификатор пользователя
        """
        self.users.append(person_id)

    def add_relation(self, from_person: int, to_person: int) -> None:
        """
        Добавление отношения дружбы между двумя пользователями

        :param from_person: Идентификатор первого пользователя
        :param to_person: Идентификатор второго пользователя
        """
        self.friendships.append((from_person, to_person))
        self.friendships.append((to_person, from_person))

    def find_route(self, from_person: int, to_person: int)-> Tuple[Any, int]:
        """
        Поиск кратчайшего пути между двумя пользователями

        :param from_person: Идентификатор первого пользователя
        :param to_person: Идентификатор второго пользователя
        """
        graph = igraph.Graph(self.friendships)
        path = graph.get_shortest_paths(from_person, to=to_person) # лучше будет нааписать алгоритм поиска самому, к ihraph могут придраться
        path_to_return = (path[0], len(path[0]))
        if not path[0]:
            path_to_return[0].append('пути не существует')
        return path_to_return

    def print_distribution(self)-> None:
        """
        Построение столбчатой диаграммы распределения связей.

        Давайте проверим известную теорию о распределении связей в
        различных сетях. Мы значем, что есть знаменитости, у которых много
        подписчиков или друзей, но основное большинство пользователей
        имеет небольшое количество связей. Вашей задачей является
        визуализация распределения связей.
        """
        friends_num = [0 for _ in range(len(self.friendships))]
        for user in self.users:
            user_friends = 0
            for friendship in self.friendships:
                if friendship[0] == user:
                    user_friends += 1
            friends_num[user_friends] += 1
        num_max_digits = len(str(len(friends_num) - 1))
        friends_max_digits = len(str(max(friends_num)))
        diagram = 'Диаграмма(#связей, #пользователей):\n===================================\n'
        for num, friends in enumerate(friends_num):
            if friends != 0:
                friends_digits = len(str(friends))
                friends_space = ' ' * (friends_max_digits - friends_digits)
                num_digits = len(str(num))
                num_space = ' ' * (num_max_digits - num_digits)
                diagram += '{}{}|{}{} '.format(num_space, num, friends_space, friends)
                for _ in range(friends):
                    diagram += '█'
                diagram += '\n'
        print(diagram)


network = Network()
for Id in range(20):
    network.add_person(Id)

network.add_relation(1, 2)
network.add_relation(2, 3)
network.add_relation(3, 4)
network.add_relation(3, 5)
network.add_relation(4, 6)
network.add_relation(5, 6)

for Id in range(7, 20):
    network.add_relation(6, Id)

print(list(network.find_route(1, 6)))
network.print_distribution()

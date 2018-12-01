from api import get_friends
import numpy as np
import igraph
import time


def get_network(users, as_edgelist=True):
    if as_edgelist:
        vertices = [user.id for user in users]
        vertices_names = [user.first_name + ' ' + user.last_name for user in users]
        edges = []
        for user in users:
            friends = get_friends(user.id, 'bdate')
            if friends:
                for friend in friends:
                    try:
                        vertices.index(friend.id)
                    except:
                        pass
                    else:
                        edges.append((vertices.index(user.id), vertices.index(friend.id)))
    else:
        vertices = [user.id for user in users]
        vertices_names = [user.first_name + ' ' + user.last_name for user in users]
        edges_map = [[0 for col in range(len(vertices))] for row in range(len(vertices))]
        edges = []
        for user in users:
            friends = get_friends(user.id, 'bdate')
            if friends:
                for friend in friends:
                    try:
                        vertices.index(friend.id)
                    except:
                        pass
                    else:
                        edges_map[vertices.index(user.id)][vertices.index(friend.id)] = 1
                        edges_map[vertices.index(friend.id)][vertices.index(user.id)] = 1
        for rown, row in enumerate(edges_map):
            for coln, el in enumerate(row):
                if el == 1:
                    edges.append((rown, coln))
    for edge in edges:
        if edge[0] == edge[1]:
            edges.remove(edge)
    graph = (vertices_names, edges)
    return graph


def plot_graph(graph):
    vertices = graph[0]
    edges = graph[1]
    g = igraph.Graph( vertex_attrs={"label": vertices}, edges=edges, directed=False)
    g.es["width"] = 1
    g.simplify(combine_edges={"width": "sum"})
    g.simplify(multiple=True, loops=True)
    N = len(vertices)
    clusters = g.community_multilevel()
    print(clusters)
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
    visual_style = {"vertex_size": 20,
                    "bbox": (2000, 2000),  # размер поля
                    "margin": 100,  # расстояние от края до вершин
                    "vertex_label_dist": 2,  # расстояние между вершинами
                    "edge_color": "gray",
                    "autocurve": True,  # кривизна ребер
                    "layout": g.layout_fruchterman_reingold(maxiter=1000, area=N ** 2, repulserad=N ** 2)
                    }
    igraph.plot(g, **visual_style)

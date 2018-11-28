from api import get_friends
import numpy as np
import igraph
import time


def get_network(users, as_edgelist=True):
    if as_edgelist:
        vertices = [user['id'] for user in users]
        vertices_names = [user['first_name'] + ' ' + user['last_name'] for user in users]
        edges = []
        for user in users:

            friends = get_friends(user['id'], 'first_name')
            if friends:
                for friend in friends:
                    try:
                        vertices.index(friend['id'])
                    except:
                        pass
                    else:
                        edges.append((vertices.index(user['id']), vertices.index(friend['id'])))
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
    visual_style = {}
    visual_style["layout"] = g.layout_fruchterman_reingold(maxiter=1000, area=N ** 2, repulserad=N ** 2)
    igraph.plot(g, **visual_style)

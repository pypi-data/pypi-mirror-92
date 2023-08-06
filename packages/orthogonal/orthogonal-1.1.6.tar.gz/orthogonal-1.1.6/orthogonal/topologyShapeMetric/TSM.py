
import math as m

import networkx as nx


def convert_pos_to_embedding(G, pos):
    """
        Only straight line in G.
    """
    emd = nx.PlanarEmbedding()
    for node in G:
        neigh_pos = {
            neigh: (pos[neigh][0]-pos[node][0], pos[neigh][1]-pos[node][1]) for neigh in G[node]
        }
        neighbors_sorted = sorted(G.adj[node], key=lambda v: m.atan2(neigh_pos[v][1], neigh_pos[v][0]))  # counter clockwise
        last = None
        for neigh in neighbors_sorted:
            emd.add_half_edge_ccw(node, neigh, last)
            last = neigh
    emd.check_structure()
    return emd


def number_of_cross(G, pos, print_it=False):
    """
    Not accurate, may be equal to actual number or double
    This static method is deprecated.  It has been moved to it single usage class as
    Planarization.numberOfCrossings(..)
    """
    def is_cross(pa, pb, pc, pd):
        def xmul(v1, v2):
            return v1[0] * v2[1] - v1[1] * v2[0]

        def f(pa, pb, p):
            return (pa[1] - pb[1]) * (p[0] - pb[0]) - (p[1] - pb[1]) * (pa[0] - pb[0])

        ca = (pa[0] - pc[0], pa[1] - pc[1])
        cb = (pb[0] - pc[0], pb[1] - pc[1])
        cd = (pd[0] - pc[0], pd[1] - pc[1])
        # return xmul(ca, cd) >= 0 and xmul(cd, cb) >= 0 and f(pa, pb, pc) * f(pa, pb, pd) < 0  # PyCharm Optimization
        return xmul(ca, cd) >= 0 > f(pa, pb, pc) * f(pa, pb, pd) and xmul(cd, cb) >= 0
    count = 0
    for a, b in G.edges:
        for c, d in G.edges:
            if a not in (c, d) and b not in (c, d):
                if is_cross(pos[a], pos[b], pos[c], pos[d]):
                    count += 1
                    if print_it:
                        print(a, b, c, d)
    return count

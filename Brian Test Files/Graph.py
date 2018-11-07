from scipy.sparse import csgraph
from scipy.sparse.csgraph import *
import numpy as np


d_graph = np.array([
    [0,0,1],
    [0,0,0],
    [1,0,0]])

s_graph = csgraph_from_dense(d_graph)

print(s_graph)


d_graph = np.array([
    [0,0,1,0,1],
    [0,0,0,0,0],
    [1,0,0,0,0],
    [0,0,0,0,0],
    [1,0,0,0,0]])

s_graph = csgraph_from_dense(d_graph)
print(depth_first_order(s_graph, 2))



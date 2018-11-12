from scipy.sparse import csgraph
from scipy.sparse.csgraph import *
import numpy as np
import sys



d_graph = np.array([
    [0,0,1],
    [0,0,0],
    [1,0,0]])

s_graph = csgraph_from_dense(d_graph)

#print(s_graph)


d_graph = np.array([
    [0,0,1,0,1,0],
    [0,0,0,0,0,0],
    [0,1,0,0,0,0],
    [0,0,0,0,0,1],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0]])
s_graph = csgraph_from_dense(d_graph)
print(depth_first_tree(s_graph, 0, True))
#print(sys.getsizeof(s_graph))
#print(sys.getsizeof(d_graph))



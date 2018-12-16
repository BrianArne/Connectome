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
   # 0,1,2,3,4,5,6,7
    [0,0,1,0,1,0,0,0], #0
    [0,0,0,0,0,0,0,0], #1
    [0,0,0,0,0,0,0,0], #2
    [0,0,0,0,0,1,0,0], #3
    [0,0,0,0,0,1,1,0], #4
    [0,0,0,0,0,0,0,0], #5
    [0,0,0,0,0,0,0,1], #6
    [0,0,0,0,0,0,0,0]])#7
s_graph = csgraph_from_dense(d_graph)
for i in range(len(d_graph[0])):
    print(depth_first_order(s_graph, i, True, True))
#print(sys.getsizeof(s_graph))
#print(sys.getsizeof(d_graph))



from MatlabConnectome import MatlabConnectome
from NodeParser import NodeParser

from scipy.sparse import csgraph
from scipy.sparse.csgraph import depth_first_order, csgraph_from_dense



'''Main'''
# Load in file
#parsed_data = NodeParser("SetOne.mat", "SetOne")
#parsed_data = NodeParser("SetTwo.mat", "SetTwo")
#parsed_data = NodeParser("SetThree.mat", "SetThree")
#parsed_data = NodeParser("Test.mat", "Test")
parsed_data = NodeParser("T.mat", "T")


parsed_data.load_data()
parsed_data.construct_node_container()

# Initialize MatlabConnectome matrix
connect = MatlabConnectome(parsed_data._node_container)
connect.fill_matrix();

# csgraph depth_first_search
s_graph = csgraph_from_dense(connect._matrix)

for key in connect._hash_lookup:
    print(depth_first_order(s_graph, connect._hash_lookup[key], True, True)[1])

# Display matrix array
for i in connect._matrix:
  print i


# Print hash look up
for key in connect._hash_lookup:
  print(str(key), connect._hash_lookup[key])

'''
# Display hash matrix
total = 0
for i in connect._hash_lookup:
  print(i, connect._hash_lookup[i])
  total += 1
print("Total Nodes: ", total)
print("Total in container: ", len(parsed_data._node_container))
'''



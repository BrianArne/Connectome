import sys
from MatlabConnectome import MatlabConnectome
from NodeParser import NodeParser

from scipy.sparse import csgraph
from scipy.sparse.csgraph import depth_first_order, csgraph_from_dense, depth_first_tree

# Picks file to run
var = input("Which test file? " + 
    "1) SetOne "+ 
    "2) SetTwo "+ 
    "3) SetThree "+ 
    "4) Test "+ 
    "5) T ")
if var == 1:
  file_name = "SetOne.mat"
  var_name = "SetOne"
elif var == 2:
  file_name = "SetTwo.mat"
  var_name = "SetTwo"
elif var == 3:
  file_name = "SetThree.mat"
  var_name = "SetThree"
elif var == 4:
  file_name = "Test.mat"
  var_name = "Test"
elif var == 5:
  file_name = "T.mat"
  var_name = "T"
else:
  print("Bad input = SetOne")
  file_name = "SetOne.mat"
  var_name = "SetOne"

# File loaded in
parsed_data = NodeParser(file_name, var_name)
parsed_data.load_data()
parsed_data.construct_node_container()

# Initialize MatlabConnectome matrix
connect = MatlabConnectome(parsed_data._node_container)
connect.fill_matrix();

# csgraph depth_first_search run on matrix from MatlabConnectome
s_graph = csgraph_from_dense(connect._matrix)
print("***Print of compressed graph connectivity***")
print(s_graph)

# Printing each node's connectivity
print("")
print("***Printing each node and its connectivity***")
for node in connect._nodes:
    print(str(node), connect._hash_lookup[node])
    print(depth_first_order(s_graph, connect._hash_lookup[node], True, True))
    print('\n')

# Prints size of matrix
print("***Printing size of each matrix***")
print("Size of matrix uncompressed: ", sys.getsizeof(connect._matrix))
print("Size of matrix compressed: ", sys.getsizeof(s_graph))

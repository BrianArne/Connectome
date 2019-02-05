import Globals #Mostly testing variables
import re #Regex
import sys


from Containers.AdjacencyMatrix import AdjacencyMatrix
from Parsers.MatlabNodeParser import MatlabNodeParser
from igraph import *
from scipy.sparse import csgraph
from scipy.sparse.csgraph import depth_first_order, csgraph_from_dense


# Picks file to run
var = input("Which test file? " + 
            "1) SetOne "+ 
            "2) SetTwo "+ 
            "3) SetThree "+ 
            "4) Test "+ 
            "5) T ")
if var == 1:
  file_name = Globals.TESTING_DIR  + "SetOne.mat"
  var_name = "SetOne"
elif var == 2:
  file_name = Globals.TESTING_DIR + "SetTwo.mat"
  var_name = "SetTwo"
elif var == 3:
  file_name = Globals.TESTING_DIR + "SetThree.mat"
  var_name = "SetThree"
elif var == 4:
  file_name = Globals.TESTING_DIR + "Test.mat"
  var_name = "Test"
elif var == 5:
  file_name = Globals.TESTING_DIR + "T.mat"
  var_name = "T"
else:
  print("Bad input = SetOne")
  file_name = "SetOne.mat"
  var_name = "SetOne"

# File loaded in
parsed_data = MatlabNodeParser(file_name, var_name)
try:
  parsed_data.load_data()
except IOError:
    print("Terminating...")
    exit()

# Create nodes
parsed_data.construct_node_container()

# Initialize AdjacencyMatrix
connect = AdjacencyMatrix(parsed_data._node_container)
connect.fill_matrix();

'''
Converts str(csgraph) to a list of integer pairs to be used by visual igraph
'''
def to_int_pairs(cs_str):
  str_pairs = re.findall('\(\d*, \d*\)', cs_str)
  num_pairs_list = []
  for s in str_pairs:
    n_arr = re.findall('\d', s)
    pair = (int(n_arr[0]), int(n_arr[1]))
    num_pairs_list.append(pair)
  return num_pairs_list
# End to_int_pairs();


# Prints connectivity pairs
cs_graph = csgraph_from_dense(connect._matrix)
print("***Print of compressed graph connectivity***")
int_pairs = to_int_pairs(str(cs_graph))
print(int_pairs)


# Printing each node's connectivity
print("")
print("***Printing each node and its connectivity***")
for i, n in enumerate(connect._nodes):
    if connect._nodes[i]._layer is 1:
        print(i, str(n))
        print(depth_first_order(cs_graph, i, True, True)[1])
        print('\n')


g = Graph()
g.add_vertices(len(connect._nodes))
g.add_edges(int_pairs)
print(g)

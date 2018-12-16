from MatlabConnectome import MatlabConnectome
from NodeParser import NodeParser

# Load in file
parsed_data = NodeParser("Test.mat", "Test")
parsed_data.load_data()
parsed_data.construct_node_container()

# Initialize MatlabConnectome matrix
connect = MatlabConnectome(parsed_data._node_container)
print(connect.layer_lens())
print(connect.max_child_node())
connect.construct_empty_matrix()
connect.fill_matrix();

# Print matrix array
for i in connect._matrix:
  print i
#print(connect._matrix)
for i in range(1, len(connect._nodes)+1):
  print(connect._hash_lookup[i])




from MatlabConnectome import MatlabConnectome
from NodeParser import NodeParser

'''Main'''
# Load in file
parsed_data = NodeParser("Test.mat", "Test")
parsed_data.load_data()
parsed_data.construct_node_container()

# Initialize MatlabConnectome matrix
connect = MatlabConnectome(parsed_data._node_container)
connect.fill_matrix();

# Display matrix array
for i in connect._matrix:
  print i


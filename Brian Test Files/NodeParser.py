from scipy import io
from Node import *

class NodeParser:

  def __init__(self, file_name, var_name):
    self._file_name = file_name
    self._var_name = var_name
    self._data = io.loadmat(file_name, squeeze_me = True)
    self._total_nodes = len(self._data[var_name])
    self._node_container = []

  '''
  Returns a container with all nodes and their data
  '''
  def construct_node_container(self):
    for i in range(self._total_nodes):
      node = Node(self.get_data_layer(i), self.get_data_current_node(i), self.get_data_input_nodes(i))
      self._node_container.append(node)
    return self._node_container

  '''
  Reurns layer of node input parameter
  '''
  def get_data_layer(self,node):
    node_data = self._data[self._var_name][node]
    arr = node_data.tolist()
    return arr[0]

  '''
  Returns the number/id of node input parameter
  '''
  def get_data_current_node(self, node):
    node_data = self._data[self._var_name][node]
    arr = node_data.tolist()
    return arr[1]

  '''
  Returns list of input nodes for node input parameter
  '''
  def get_data_input_nodes(self, node):
    node_data = self._data[self._var_name][node]
    a = node_data.tolist()
    arr = []
    for val in a[2]:
      arr.append(val)
    return arr



####TESTING####
'''
test = NodeParser("Test.mat", "Test")
cont = test.construct_node_container()
for i in cont:
  print(i)
'''

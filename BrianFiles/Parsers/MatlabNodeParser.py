from scipy import io
from Containers.Node import *
from Parsers.NodeParser import NodeParser

'''
The MatlabNodeParser class is responsible for constructing a node container from .mat files
'''
class MatlabNodeParser(NodeParser):

  '''
  Constructor. Might be matlab specific currently with argument requirements
  '''
  def __init__(self, file_name, var_name):
    super(MatlabNodeParser, self).__init__(file_name)
    self._var_name = var_name
    self._data = None
    self._total_nodes = None
  # End __init__();

  '''
  Initializes self. _total_nodes container with all nodes and their data
  '''
  def construct_node_container(self):
    last_layer = 1
    i_nodes = []
    for i in range(self._total_nodes):
      node = Node(self.get_data_layer(i), self.get_data_current_node(i), self.get_data_input_nodes(i))
      if node._layer is not last_layer:
        last_layer = node._layer
        i_nodes[:] = []
      for n in node._input_nodes:
        i_nodes.append(n)
        self._node_container.append(node)

    i_nodes.sort()
    self.construct_i_nodes(last_layer, i_nodes)
  # End construct_node_container();
  
  '''
  Appends final i_nodes that do not have a cell associated with the .mat file
  '''
  def construct_i_nodes(self, last_previous_layer, i_nodes):
    input_layer = last_previous_layer + 1
    for n in i_nodes:
        node = Node(input_layer, n, [])
        self._node_container.append(node)
  # End construct_i_nodes();

  '''
  Reurns layer of node input parameter
  '''
  def get_data_layer(self,node):
    node_data = self._data[self._var_name][node]
    arr = node_data.tolist()
    return arr[0]
  # End get_data_layer();

  '''
  Returns the number/id of node input parameter
  '''
  def get_data_current_node(self, node):
    node_data = self._data[self._var_name][node]
    arr = node_data.tolist()
    return arr[1]
  # End get_data_current_node();

  '''
  Returns list of input nodes for node input parameter
  '''
  def get_data_input_nodes(self, node):
    node_data = self._data[self._var_name][node]
    a = node_data.tolist()
    arr = []
    if type(a[2]) == int:
      arr.append(a[2])
    else:
      for val in a[2]:
        arr.append(val)
    return arr
  # End get_data_input_nodes();

  '''
  Reads in file data to _data
  '''
  def load_data(self):
    self._data = io.loadmat(self._file_name, squeeze_me = True)
    self._total_nodes = len(self._data[self._var_name])
  # End load_data();

# End NodeParser Class;

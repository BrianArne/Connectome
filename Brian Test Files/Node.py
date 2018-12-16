
'''
The Node class is a container for a data with a id number, layer, and input nodes
'''
class Node:

  '''
  Constructor for node
  '''
  def __init__(self, layer, current_number, input_nodes):
    self._layer = layer
    self._current_number = current_number
    self._input_nodes = input_nodes
  # End __init__();

  '''
  Helper method for printing Nodes
  '''
  def __str__(self):
    return "Layer: " + str(self._layer) + \
           " Node: " + str(self._current_number) + \
           " Input Nodes: " + str(self._input_nodes)
  # End __str__();

'''
The Node class is a container for a data with a id number, layer, and input nodes
'''
class Node:

  '''
  Constructor for node
  '''
  def __init__(self, layer, node_number, input_nodes):
    if (not Node.validate(layer, node_number, input_nodes)):
      raise ValueError("Nodes and layers must be greater than 0.")
    self._layer = layer
    self._node_number = node_number
    self._input_nodes = input_nodes
  # End __init__();

  '''
  Helper method for printing Nodes
  '''
  def __str__(self):
    return "Layer: " + str(self._layer) + \
           " Node: " + str(self._node_number) + \
           " Input Nodes: " + str(self._input_nodes)
  # End __str__();

  '''
  Validates 1 indexed data
  '''
  @staticmethod
  def validate(layer, node_number, input_nodes):
    if type(input_nodes) == int:
      if (layer < 1 or node_number < 1 or input_nodes < 1):
        return False
    else:
      for n in input_nodes:
        if n < 1:
          return False
      if (layer < 1 or node_number < 1):
        return False
    return True
  # End validate();

#End Node Class;

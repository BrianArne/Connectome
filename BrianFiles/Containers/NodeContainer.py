
'''
The NodeContainer class is reposible for holding a list of Node objects and important 
information about the inputs and outputs of the neural network
'''
class NodeContainer:

  def __init__(self, node_list):
    self._input_node_positions = []
    self._max_layer = None
    self._nodes = node_list
    self._output_nodes = []

    self.max_layer()
    self.find_outputs()
    self.find_inputs()
  # End __init__();

  '''
  Finds and sets all _input_nodes
  '''
  def find_inputs(self):
    self._input_node_positions = [n for n in self._nodes if n._layer == self._max_layer]
  # End find_outputs();

  '''
  Finds and sets _output_nodes
  '''
  def find_outputs(self):
    self._output_nodes = [n for n in self._nodes if n._layer is 1]
  # End find_outputs();

  '''
  Finds and sets max_layer
  '''
  def max_layer(self):
    #Checks for empty init list
    if self._nodes == []:
      return

    self._max_layer = 0
    for n in self._nodes:
      if n._layer > self._max_layer:
        self._max_layer = n._layer
  # End max_layer

# End NodeContainer Class;

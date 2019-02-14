from copy import deepcopy
from scipy.sparse import csgraph # Can probably be removed. Only needed for print_connectivity
from scipy.sparse.csgraph import * # Can probably be removed. Only needed for print_connectivity

'''
The AdjacencyMatrix class is designed to turn a node container supplied 
into a list of all possible paths and edges from output to input nodes. Typical usage is to
fill_matirx() and then create paths
'''
class AdjacencyMatrix:

  '''
  Constructor taking a class NodeContainer
  '''
  def __init__(self, node_list):
    self._layer_hash = {}
    self._position_hash = {}
    self._matrix = None
    self._max_layer = None
    self._nodes = node_list
    self._output_nodes = []
    self._input_node_positions = []
    self._output_paths = {}
    self._paths = []
  # End __init__();
  
  '''
  Checks if the input_node terminates before reaching original inputs
  @returns True if the input node has a corresponding node in the _nodes list
  '''
  def check_termination(self, node_number, layer):
      layer_hash = self._layer_hash[layer]
      return node_number in layer_hash.keys()
  # End check_termination

  '''
  Constructs an empty adjacency matrix and initilizes all hashes for lookup
  '''
  def construct_empty_matrix(self):
    self.init_position_hash()
    self._matrix = [[0] * (len(self._nodes)) for n in range (len(self._nodes))]
  # End construct_empty_matrix();

  '''
  Does a depth first traversal to generate all paths from outputs to inputs, appends to global paths
  @Returns all paths for a given node to the inputs
  '''
  def create_paths(self, node, edges_l):
    # base case: at a input node, append to path and recurse back out
    if (len(node._input_nodes) is 0 and self._position_hash[node] in self._input_node_positions):
      self._paths.append(deepcopy(edges_l))
      return
    # recurse case: Not at an input, add edge to current path and call again
    else:
      for i in node._input_nodes:
        pos_hash = self._layer_hash[node._layer + 1]
        if int(i) not in pos_hash:
          continue
        input_position = pos_hash[i]
        edge = (self._position_hash[node], input_position)
        if edge not in edges_l:
          edges_l.append(edge)
        new_node = self._nodes[input_position]
        self.create_paths(new_node, edges_l)

        # Remove edge after backing out of recursive call
        edges_l.remove(edge)
  # End create_paths();

  '''
  Fills matrix to make adjacency matrix and initializes input and output node list
  '''
  def fill_matrix(self):
    self.construct_empty_matrix()
    for i, n in enumerate(self._nodes):
        for j in n._input_nodes:
            if (n._layer + 1) <= self._max_layer and self.check_termination(j, n._layer+1):
                l_hash = self._layer_hash[n._layer+1]
                pos = l_hash[j]
                self._matrix[i][pos] = 1
        # Adds to ouputs or inputs if node is applicable
        if n._layer is 1 and n not in self._output_nodes:
            self._output_nodes.append(n)
        if n._layer is self._max_layer and i not in self._input_node_positions:
            self._input_node_positions.append(i)
                
  # End fill_matrix();

  '''
  Adds a list of all edges assocated with each output node to _output_paths dictionary
  '''
  def generate_all_output_paths(self):
    for n in self._output_nodes:
      edge_l = []
      self.create_paths(n, edge_l)
      new_edge_l = []
      for l in self._paths:
        for e in l:
          new_edge_l.append(e)
      self._output_paths[n] = new_edge_l
      self._paths[:] = []
  # End append_output_paths();

  '''
  Initializes hash with @key = layer, @value = layer_hash
  Calls init_layer_hash()
  '''
  def init_hash(self):
      for i in range(1, self._max_layer + 1):
          self._layer_hash[i] = {}
          self.init_layer_hash(self._layer_hash[i], i)
  # End init_hash();
  
  '''
  Initializes hash with @key = node_number, @value = position in matrix
  '''
  def init_layer_hash(self, origin_hash, layer):
      for n in self._nodes:
          if n._layer is layer:
              origin_hash[n._node_number] = self._position_hash[n]
  # End init_layer_hash();

  '''
  Initializes hash with @key = node, @value = position in the matrix
  Calls init_hash()
  '''
  def init_position_hash(self):
      self.max_layer()
      for i, n in enumerate(self._nodes):
          self._position_hash[n] = i
      self.init_hash()
  # End init_position_hash();

  '''
  Sets the _max_layer to the highest layer from the nodes
  '''
  def max_layer(self):
      m_layer = 0
      for n in self._nodes:
          if n._layer > m_layer:
            m_layer = n._layer
      self._max_layer = m_layer
  # End max_layer_node();

  '''
  Prints all nodes connectivity
  @Depricated. Not used with current current model.
  '''
  def print_connectivity(self):
    print("***Printing each node and its connectivity***")
    csr_graph = csgraph_from_dense(self._matrix)
    for i, n in enumerate(self._nodes):
        if n._layer is self._max_layer: continue # Connect._max_layer is kinda global, change.
        print(i, str(n))
        print(depth_first_order(csr_graph, i, True, True)[1])
        print('\n')
  # End print_connectivity();
  
# End AdjacencyMatrix Class;

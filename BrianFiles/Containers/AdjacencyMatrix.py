from copy import deepcopy

'''
The AdjacencyMatrix class is designed to turn a node container supplied 
into a list of all possible paths and edges from output to input nodes. Typical usage is to
fill_matirx() and then create paths
'''
class AdjacencyMatrix:

  '''
  Constructor taking a class NodeContainer
  '''
  def __init__(self, node_container):
    self._layer_hash = {}
    self._paths = []
    self._position_hash = {}
    self._matrix = None
    self._node_container = node_container
    self._output_paths = {}

    self.init_position_hash()

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
    self._matrix = [[0] * (len(self.get_nodes())) for n in range (len(self.get_nodes()))]
  # End construct_empty_matrix();

  '''
  Does a depth first traversal to generate all paths from outputs to inputs, appends to global paths
  @Returns all paths for a given node to the inputs
  '''
  def create_paths(self, node, edges_l):
    # base case: at a input node, append to path and recurse back out
    if (len(node._input_nodes) is 0 and (node in self.get_input_nodes())):
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
        new_node = self.get_nodes()[input_position]
        self.create_paths(new_node, edges_l)

        # Remove edge after backing out of recursive call
        edges_l.remove(edge)
  # End create_paths();

  '''
  Returns a list of unique edges
  '''
  def extract_unique_edges(self, user_query):
    edges= []
    for q in user_query:
      for e in self._output_paths[self.get_output_nodes()[q-1]]:
        if e not in edges:
          edges.append(e)
    return edges
  # End extract_unique_edges();

  '''
  Fills matrix to make adjacency matrix
  '''
  def fill_matrix(self):
    self.construct_empty_matrix()
    for i, n in enumerate(self.get_nodes()):
        for j in n._input_nodes:
            if (n._layer + 1) <= self.get_max_layer() and self.check_termination(j, n._layer+1):
                l_hash = self._layer_hash[n._layer+1]
                pos = l_hash[j]
                self._matrix[i][pos] = 1
  # End fill_matrix();

  '''
  Returns input node list from the NodeContainer
  '''
  def get_input_nodes(self):
    return self._node_container._input_nodes
  # End get_input_nodes();

  '''
  Returns max_layer from NodeContainer
  '''
  def get_max_layer(self):
    return self._node_container._max_layer
  # End get_max_layer();

  '''
  Returns node list from the the NodeContainer
  '''
  def get_nodes(self):
    return self._node_container._nodes
  # End get_nodes();

  '''
  Returns output node list from the NodeContainer
  '''
  def get_output_nodes(self):
    return self._node_container._output_nodes
  # End get_output_nodes();

  '''
  Adds a list of all edges assocated with each output node to _output_paths dictionary
  '''
  def generate_all_output_paths(self):
    for n in self.get_output_nodes():
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
      for i in range(1, self.get_max_layer() + 1):
          self._layer_hash[i] = {}
          self.init_layer_hash(self._layer_hash[i], i)
  # End init_hash();
  
  '''
  Initializes hash with @key = node_number, @value = position in matrix
  '''
  def init_layer_hash(self, origin_hash, layer):
      for n in self.get_nodes():
          if n._layer is layer:
              origin_hash[n._node_number] = self._position_hash[n]
  # End init_layer_hash();

  '''
  Initializes hash with @key = node, @value = position in the matrix
  Calls init_hash()
  '''
  def init_position_hash(self):
      for i, n in enumerate(self.get_nodes()):
          self._position_hash[n] = i
      self.init_hash()
  # End init_position_hash();

# End AdjacencyMatrix Class;

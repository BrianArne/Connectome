import numpy as np
from scipy.sparse import csgraph
from scipy.sparse.csgraph import *

'''
The AdjacencyMatrix class is designed to turn a node container supplied 
on initialization into a sparse csgraph to allow a depth first search
to be run on the sparse csgraph
'''
class AdjacencyMatrix:

  '''
  Constructor taking file name and variable inside file to be processed
  '''
  def __init__(self, node_list):
    self._layer_hash = {}
    self._position_hash = {}
    self._matrix = None
    self._max_layer = None
    self._nodes = node_list
    self._output_nodes = []
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
  Fills matrix to make adjacency matrix
  '''
  def fill_matrix(self):
    self.construct_empty_matrix()
    for i, n in enumerate(self._nodes):
        for j in n._input_nodes:
            if (n._layer + 1) <= self._max_layer and self.check_termination(j, n._layer+1):
                l_hash = self._layer_hash[n._layer+1]
                pos = l_hash[j]
                self._matrix[i][pos] = 1
            if n._layer is 1 and n not in self._output_nodes:
                self._output_nodes.append(n)
  # End fill_matrix();

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
  
# End AdjacencyMatrix Class;

# TODO Combine max_layer_node() and final_max_inode() to be more efficient

import numpy as np
from scipy.sparse import csgraph
from scipy.sparse.csgraph import *

'''
The MatlabConnectome class is designed to turn a node container supplied 
on initialization into a sparse csgraph allow a depth first search
to be run on the sparse csgraph
'''
class MatlabConnectome:

  '''
  Constructor taking file name and variable inside file to be processed
  '''
  def __init__(self, node_list):
    self._hash_lookup = {}
    self._matrix = None
    self._max_layer_node = {} 
    self._nodes = node_list
  # End __init__();


  '''
  Constructs an adjacency matrix and return it
  '''
  def construct_empty_matrix(self):
    self.max_layer_node()
    total_layer_nodes = 0
    for key in self._max_layer_node:
      total_layer_nodes += self._max_layer_node[key]
    self._matrix = [[0] * (total_layer_nodes+1) for n in range (total_layer_nodes+1)]
  # End construct_empty_matrix();

  '''
  Converts dense matrix to cs_sparse_graph
  '''
  def convert_sparse(self, matrix):
    return csgraph_from_dense(matrix);
  # End convert_sparse();

  '''
  Fills matrix from each node's data
  '''
  def fill_matrix(self):
    self.construct_empty_matrix()
    print("Max layer node: ", self._max_layer_node)
    # Old_offest represents current layer being processed
    old_offset = 0
    # Offset represents the i_node layer below current layer
    offset = self._max_layer_node[1]
    layer = 1
    for n in self._nodes:
      if n._layer != layer:
        old_offset += offset
        offset += self._max_layer_node[layer + 1]
        layer = n._layer
      for j in n._input_nodes:
        print("Offset: ", offset)
        if layer != 1:
          self._hash_lookup[n] = n._node_number + old_offset
          self._matrix[n._node_number + old_offset][j + offset] = 1
        else:
          self._hash_lookup[n] = n._node_number
          self._matrix[n._node_number][j + offset] = 1
  # End fill_matrix();

  '''
  Returns dictionary layers and their highest node number
  '''
  def max_layer_node(self):
    for i in self._nodes:
      if i._layer in self._max_layer_node:
        if i._node_number > self._max_layer_node[i._layer]:
          self._max_layer_node[i._layer] = i._node_number
      else:
        self._max_layer_node[i._layer] = i._node_number
    self.final_max_inode()
  # End max_layer_node();

  '''
  Sets highest final layer max i_node value
  '''
  def final_max_inode(self):
    holder = {}
    for i in self._nodes:
      if i._layer < max(self._max_layer_node.keys()):
        continue
      if i._layer in holder:
        if max(i._input_nodes) > holder[i._layer]:
          holder[i._layer] = max(i._input_nodes)
        continue
      holder[i._layer] = max(i._input_nodes)
    self._max_layer_node[max(holder.keys()) + 1] = holder[max(holder.keys())]
  # End final_max_inode();

# End MatlabConnectome Class;

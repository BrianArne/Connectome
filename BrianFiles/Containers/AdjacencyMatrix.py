# TODO
#     - Combine max_layer_node() and final_max_inode() to be more efficient
#     - Check comments and change as necessary
#     - Implement way to apply hash look up with data from depth_first_order
#     - Rename classes to better reflect what they do

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
    self._hash_lookup = {}
    self._matrix = None
    self._max_layer_node = {} 
    self._nodes = node_list
  # End __init__();


  '''
  Constructs an adjacency matrix
  '''
  def construct_empty_matrix(self):
    self.max_layer_node()
    total_layer_nodes = 0
    for key in self._max_layer_node:
      total_layer_nodes += self._max_layer_node[key]
    self._matrix = [[0] * (total_layer_nodes+1) for n in range (total_layer_nodes+1)]
  # End construct_empty_matrix();

  '''
  Fills matrix with node connectivity
  '''
  def fill_matrix(self):
    self.construct_empty_matrix()

    # Old_offest represents current layer being processed
    old_offset = 0
    # Offset represents the i_node layer below current layer
    offset = self._max_layer_node[1]

    layer = 1
    for n in self._nodes:
      # Checks for layer change, changes offsets if there is layer change
      if n._layer != layer:
        old_offset = offset
        offset += self._max_layer_node[layer + 1]
        layer = n._layer
      
      # Gives nodes a hash_lookup value
      if layer != 1:
        self._hash_lookup[n] = n._node_number + old_offset
      else:
        self._hash_lookup[n] = n._node_number

      # Inputs node with hash_lookup value to matrix
      for j in n._input_nodes:
        self._matrix[self._hash_lookup[n]][j + offset] = 1
  # End fill_matrix();

  '''
  Init. _max_layer_node dictionary with layers and their highest node number for offset calculation
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
  Sets highest final layer (input layer) max i_node value for offset calculation
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
      if len(i._input_nodes) > 0:
        holder[i._layer] = max(i._input_nodes)
    self._max_layer_node[max(holder.keys()) + 1] = holder[max(holder.keys())]
  # End final_max_inode();

# End AdjacencyMatrix Class;

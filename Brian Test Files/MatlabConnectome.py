# TODO
# Map hash_lookup to the actual matrix data

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
    self._all_paths = []
    self._matrix = None
    self._hash_lookup = {}
    self._layer_offset = {}
    self._layer_max_child = {}
    self._nodes = node_list
    self._layer_lens = {} 
  # End __init__();


  '''
  Constructs an adjacency matrix and return it
  '''
  def construct_empty_matrix(self):
    self.layer_lens()
    self.max_child_node()
    total_layer_nodes = 0
    for key in self._layer_max_child:
      total_layer_nodes += self._layer_max_child[key]
    self._matrix = [[0] * (total_layer_nodes+1) for n in range (total_layer_nodes+1)]
  # End construct_empty_matrix();

  '''
  Converts dense matrix to cs_sparse_graph
  '''
  def convert_sparse(self, matrix):
    return csgraph_from_dense(matrix);
  # End convert_sparse();

  '''
  Creates offset hash for referencing nodes in matrix
  '''
  def create_offset_hash(self):
    offset = 0
    self._layer_offset[1] = offset
    for i in range(2, len(self._layer_max_child) + 1):
      if i == 2 : offset += self._layer_max_child[1]
      offset += self._layer_max_child[i]
      self._layer_offset[i] = offset
  # End create_offset_hash();

  '''
  Fills matrix from each node's data
  '''
  def fill_matrix(self):
    self.construct_empty_matrix()
    offset = 0
    layer = 1
    for n in self._nodes:
      if n._layer != layer:
        offset += self._layer_max_child[layer]
        layer = n._layer
      for j in n._input_nodes:
        self._hash_lookup[n._node_number] = n._node_number + offset
        self._matrix[n._node_number + offset][j+offset] = 1
  # End fill_matrix();

  '''
  Returns dictionary layers and their lengths
  '''
  def layer_lens(self):
    for i in self._nodes:
      if i._layer in self._layer_lens:
        self._layer_lens[i._layer] += 1
      else:
        self._layer_lens[i._layer] = 1
  # End layer_lens();

  '''
  Returns max node value for a layer
  '''
  def max_child_node(self):
    for i in self._nodes:
      if i._layer in self._layer_max_child:
        continue
      self._layer_max_child[i._layer] = max(i._input_nodes)
    self.create_offset_hash()
  # End max_child_node();

  '''
  Prints all_paths to console
  '''
  def print_all_paths(self):
    for i in range(len(self.get_all_paths())):
        print("Path",i,self.get_all_paths()[i])
  # End print_all_paths();

# End MatlabConnectome Class;

# TODO
# Node class and Node Praser have been implemented
# Need to clean up Connectome class and make methods work
# Emphasis on hash table to original nodes

from Node import Node
from NodeParser import NodeParser
import numpy as np
from scipy.sparse import csgraph
from scipy.sparse.csgraph import *


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


  '''
  Constructs an adjacency matrix and return it
  '''
  def construct_empty_matrix(self):
    total_layer_nodes = 0
    for key in self._layer_max_child:
      total_layer_nodes += self._layer_max_child[key]
    self._matrix = [[0] * (total_layer_nodes+1) for n in range (total_layer_nodes+1)]
    return self._matrix

  '''
  Converts dense matrix to cs_sparse_graph
  '''
  def convert_sparse(self, matrix):
    return csgraph_from_dense(matrix);

  '''
  Fills matrix from each node's data
  '''
  def fill_matrix(self):
    if self._matrix == None:
      print("You need to construct an empty matrix first.")
    else:
      offset = 0
      layer = 1
      for n in self._nodes:
        if n._layer != layer:
          offset += self._layer_max_child[layer]
          layer = n._layer
        for j in n._input_nodes:
          self._hash_lookup[n._current_number] = n._current_number + offset
          self._matrix[n._current_number + offset][j+offset] = 1
      return self._matrix

  '''
  Returns dictionary layers and their lengths
  '''
  def layer_lens(self):
    for i in self._nodes:
      if i._layer in self._layer_lens:
        self._layer_lens[i._layer] += 1
      else:
        self._layer_lens[i._layer] = 1
    return self._layer_lens

  '''
  Returns max node value for a layer
  '''
  def max_child_node(self):
    for i in self._nodes:
      if i._layer in self._layer_max_child:
        continue
      self._layer_max_child[i._layer] = max(i._input_nodes)
    self.create_offset_hash()
    return self._layer_max_child

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
    return

  '''
  Prints all_paths to console
  '''
  def print_all_path(self):
    for i in range(len(self.get_all_paths())):
        print("Path",i,self.get_all_paths()[i])


########################
########TESTING#########
########################
parsed_data = NodeParser("Test.mat", "Test")
parsed_data.construct_node_container()
connect = MatlabConnectome(parsed_data._node_container)
print(connect.layer_lens())
print(connect.max_child_node())
connect.construct_empty_matrix()
matrix = connect.fill_matrix();
for i in matrix:
  print i
#print(connect._matrix)
for i in range(1, len(connect._nodes)+1):
  print(connect._hash_lookup[i])

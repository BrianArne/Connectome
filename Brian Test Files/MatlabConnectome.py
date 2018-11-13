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
  def fill_matrix(self, max_child_node):
    if self.matrix == None:
      print("You need to construct an empty matrix first.")
    else:
      offset = 0
      layer = 1
      for i in range(1, self.total_nodes()+1):
        current_node = self.current_node(i)
        child_node = self.child_nodes(i)
        node_layer = self.layer_of_node(self.node_data(i))
        if node_layer != layer:
          offset += max_child_node[layer]
          layer = node_layer
        for j in child_node:
          self.hash_lookup[current_node] = current_node + offset
          self.matrix[current_node+offset][j+offset] = 1
      return self.matrix

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
  ***Initializing offset is in here too***
  '''
  def max_child_node(self):
    for i in self._nodes:
      if i._layer in self._layer_max_child:
        continue
      self._layer_max_child[i._layer] = max(i._input_nodes)
    return self._layer_max_child

    '''
    offset = 0
    self.layer_offset[1] = offset
    for i in range(2, len(layer_max) + 1):
      if i == 2 : offset += layer_max[1]
      offset += layer_max[i]
      self.layer_offset[i] = offset
    '''

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
print(len(connect._matrix))
print(len(connect._matrix[0]))

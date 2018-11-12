# TODO
# Node class and Node Praser have been implemented
# Need to clean up Connectome class and make methods work
# Emphasis on hash table to original nodes

import NodeParser import *
#import numpy as np
from scipy.sparse import csgraph
from scipy.sparse.csgraph import *


class MatlabConnectome:

  '''
  Constructor taking file name and variable inside file to be processed
  '''
  def __init__(self):
    self.all_paths = []
    self.matrix = None
    self.hash_lookup = {}
    self.layer_offset = {}
    self.nodes = None


  '''
  Constructs an adjacency matrix and return it
  '''
  def construct_empty_matrix(self, layer_max):
    total_layer_nodes = 0
    for key in layer_max:
      total_layer_nodes += layer_max[key]
    self.matrix = [[0] * (total_layer_nodes+1) for n in range (total_layer_nodes+1)]
    return self.matrix

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
  Converts dense matrix to cs_sparse_graph
  '''
  def convert_sparse(self, matrix):
    return csgraph_from_dense(matrix);
  
  '''
  Returns all_paths
  '''
  def get_all_paths(self):
    return self.all_paths


  '''
  Returns hash_lookup
  '''
  def get_hash_lookup(self):
    return self.hash_lookup

  '''
  Returns layer_offset
  '''
  def get_layer_offset(self):
    return self.layer_offset

  '''
  Returns matrix
  '''
  def get_matrix(self):
    return self.matrix

  '''
  Returns dictionary layers and their lengths
  '''
  def layer_lens(self):
    layer_dict = {}
    for i in range(self.total_nodes()):
      data = self.node_data(i)
      layer = self.layer_of_node(data)
      if layer in layer_dict:
        layer_dict[layer] += 1
      else:
        layer_dict[layer] = 1
    return layer_dict

  '''
  Returns max node value for a layer
  ***Initializing offset is in here too***
  '''
  def max_child_node(self):
    layer_max = {}
    for i in range(self.total_nodes()):
        data = self.node_data(i)
        layer = self.layer_of_node(data)

        if layer == 1 and 1 in layer_max:
          if layer_max[layer] < self.current_node(i):
            layer_max[layer] = self.current_node(i)
        elif layer == 1 and 1 not in layer_max:
            layer_max[layer] = self.current_node(i)

        if layer in layer_max and layer != 1:
          if layer_max[layer] < max(self.child_nodes(i)):
            layer_max[layer] = max(self.child_nodes(i))
        else:
          layer_max[layer] = self.current_node(i)

    offset = 0
    self.layer_offset[1] = offset
    for i in range(2, len(layer_max) + 1):
      if i == 2 : offset += layer_max[1]
      offset += layer_max[i]
      self.layer_offset[i] = offset
       
    return layer_max


  '''
  Prints all_paths to console
  '''
  def print_all_path(self):
    for i in range(len(self.get_all_paths())):
        print("Path",i,self.get_all_paths()[i])


########################
########TESTING#########
########################


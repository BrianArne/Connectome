# TODO
# I think we can save a lot of processing if we just made a node class with their associated methods and had the MatlabConnectome carry around a container of them
# Need to write the method converting it to sparse graph
# Need to write method doing the depth_first_search
# The mapping out of the matrix needs to be done



from scipy import io


class MatlabConnectome:

  MATLAB_OFFSET = 1

  '''
  Constructor taking file name and variable inside file to be processed
  '''
  def __init__(self, file_name, var_name):
    self.file_name = file_name
    self.var_name = var_name
    self.all_paths = []
    self.matrix = None

  '''
  Returns array of child nodes for a node
  '''
  def child_nodes(self, node):
    node_data = self.node_data(node)
    a = node_data.tolist()
    arr = []
    for val in a[2]:
      arr.append(val)
    return arr

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
  Returns actual node value
  '''
  def current_node(self, node):
    node_data = self.node_data(node)
    a = node_data.tolist()
    return a[1]

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
          self.matrix[current_node+offset][j+offset] += 1
      return self.matrix

  
  '''
  Returns all_paths
  '''
  def get_all_paths(self):
    return self.all_paths

  '''
  Returns file name
  '''
  def get_file(self):
    return self.file_name

  '''
  Returns matrix
  '''
  def get_matrix(self):
    return self.matrix

  '''
  Returns variable name
  '''
  def get_var(self):
    return self.var_name

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
  Returns the layer number of the node
  '''
  def layer_of_node(self, node_data):
    a = node_data.tolist()
    return a[0]

  '''
  Returns max node value for a layer
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
    return layer_max

  '''
  Returns a ndarray of node data
  '''
  def node_data(self, node):
    var = io.loadmat(self.file_name, squeeze_me=True)
    data = var[self.var_name][node - MatlabConnectome.MATLAB_OFFSET]
    return data

  '''
  Prints all_paths to console
  '''
  def print_all_path(self):
    for i in range(len(self.get_all_paths())):
        print("Path",i,self.get_all_paths()[i])

  '''
  Gets the total number of nodes in the matlab file
  '''
  def total_nodes(self):
      var = io.loadmat(self.file_name, squeeze_me=True)
      return len(var[self.var_name])

########################
########TESTING#########
########################

t_obj = MatlabConnectome("Test.mat", "Test")

max_layer_dict = t_obj.max_child_node()
print(max_layer_dict)
t_obj.construct_empty_matrix(max_layer_dict)

matrix = t_obj.fill_matrix(max_layer_dict)


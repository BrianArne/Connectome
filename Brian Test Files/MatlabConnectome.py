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
  def construct_matrix(self):
    matrix = [[0] * self.total_nodes()] * self.total_nodes()
    prev_nodes = 0
    #for i in range(self.total_nodes()):
    
    #prev_nodes += self.layer_lens[i]

    return matrix

  '''
  Returns actual node value
  '''
  def current_node(self, node):
    node_data = self.node_data(node)
    a = node_data.tolist()
    return a[1]
  
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

        if layer+1 in layer_max:
          if layer_max[layer+1] < max(self.child_nodes(i)):
            layer_max[layer+1] = max(self.child_nodes(i))
        else:
          layer_max[layer+1] = self.current_node(i)
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

t_obj = MatlabConnectome("T.mat", "T")
#t_obj.construct_matrix()



for i in range(1, t_obj.total_nodes()):
  print(t_obj.child_nodes(i))

print(t_obj.max_child_node())

print(t_obj.construct_matrix())



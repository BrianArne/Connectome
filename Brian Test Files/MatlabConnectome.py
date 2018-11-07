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

  def print_all_path(self):
    for i in range(len(self.get_all_paths())):
        print("Path",i,self.get_all_paths()[i])
  
  '''
  Returns a ndarray of node data
  '''
  def node_data(self, node):
    var = io.loadmat(self.file_name, squeeze_me=True)
    data = var[self.var_name][node - MatlabConnectome.MATLAB_OFFSET]
    return data

  '''
  Returns all_paths
  '''
  def get_all_paths(self):
    return self.all_paths

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
  Returns actual node value
  '''
  def current_node(self, node):
    node_data = self.node_data(node)
    a = node_data.tolist()
    return a[1]

  '''
  Returns file name
  '''
  def get_file(self):
    return self.file_name

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
  Gets the total number of nodes in the matlab file
  '''
  def total_nodes(self):
      var = io.loadmat(self.file_name, squeeze_me=True)
      return len(var[self.var_name])

  #############################
  ###     Matt's Methods    ###
  #############################

  def load_data_noPreprocessing_MS2(self, lay1Len, lay2Len, lay3Len, lay4Len):
    #My Code
    '''
    layer_lens = self.layer_lens()
    print(layer_lens[1])
    layers = []
    for i in range(len(layer_lens)):
      layers.append([])

    for i in range(len(layer_lens)):
      print(i)
      print("Layer " + str(layer_lens[i + 1]))
      for j in range(layer_lens[i+1] + 1):
        layers[i].append([1000 * i])
    print(layers)
    '''
        
    layers = [[],[],[],[],[]]
    for i in range(lay1Len):
      layers[0].append([1000])
    for i in range(lay2Len):
      layers[1].append([2000])
    for i in range(lay3Len):
      layers[2].append([3000])
    for i in range(lay4Len):
      layers[3].append([4000])
    for i in range(300):
      layers[4].append([5000])

    for i in range(MatlabConnectome.MATLAB_OFFSET, self.total_nodes() + MatlabConnectome.MATLAB_OFFSET):
      these_inodes = self.child_nodes(i)
      position = self.current_node(i)
      this_layer = self.layer_of_node(self.node_data(i))
      layers[this_layer-1][position-1] = these_inodes
    return layers


  def getChildren(self, path, index, currentLayer, layers):
    #If the current layer is 4, return all of the possible paths.
    if (index>= len(layers[currentLayer])): return

    inodes = layers[currentLayer][index]
        
    if currentLayer == 4 and max(inodes) < 500:
      paths = []
      for i in range(len(inodes)):
        thisPath = path[:]
        thisPath.append(inodes[i])

        self.all_paths.append(thisPath)
        print("\t\t\t\tPATH",thisPath)
                                                                         
  #otherwise, continue to the next layer:
    else:
      if currentLayer == 0 and max(inodes) < 500:
        print("firstlayer:",index+1,inodes)
      if currentLayer == 1 and max(inodes) < 500:
        print("\tsecondlayer:",index+1,inodes)
      if currentLayer == 2 and max(inodes) < 500:
        print("\t\tthirdlayer:",index+1,inodes)
      if currentLayer == 3 and max(inodes) < 500:
        print("\t\t\tfourthlayer:",index+1,inodes)
      for i in range(len(inodes)):
        if inodes[i] < 500:
          newPath = path[:]
          newPath.append(inodes[i])
          self.getChildren(newPath,inodes[i]-1,currentLayer +1,layers)

  '''
  Returns variable name
  '''
  def get_var(self):
    return self.var_name



########################
########TESTING#########
########################

t_obj = MatlabConnectome("T.mat", "T")
#num_data = t_obj.node_data(88)
#num = t_obj.layer_of_node(num_data)
#t_obj.print_a_path()

#print(num)
#Mine
#layers = t_obj.load_data_noPreprocessing_MS2(6,11,16,21)
#Matts
layers = t_obj.load_data_noPreprocessing_MS2(4,6,11,50)

print("\n\n")
t_obj.getChildren([1],0,0,layers)
print("---------------")
t_obj.getChildren([2],1,0,layers)
print("---------------")
t_obj.getChildren([3],2,0,layers)
print("---------------")
t_obj.getChildren([4],3,0,layers)

#Prints list of all paths
t_obj.print_all_path()

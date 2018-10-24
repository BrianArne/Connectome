from scipy import io

'''
Gets the total number of nodes in the matlab file
'''
def total_nodes(file_name): #Do not include .mat extension
    file_with_extension = file_name + '.mat'
    var = io.loadmat(file_with_extension, squeeze_me=True)
    return len(var[file_name])

'''
Returns a ndarray of node data
'''
def access_node_data(file_name, node):

  file_with_extension = file_name + '.mat'
  var = io.loadmat(file_with_extension, squeeze_me=True)
  data = var[file_name][node]
  return data

'''
Returns the layer of the node
'''
def get_layer_of_node(node_data):
  a = node_data.tolist()
  return a[0]



#Testing Garbage
num = 11
data = access_node_data('Test', num)
print(get_layer_of_node(data))
#print(data.index(0))




#TODO Current node method, child nodes of current node method



'''
Gets access to the current node. Changes on a 1:1 ratio
current_node = var[file_name][0,15]['current_node']
#                               ^controls current node number
print(current_node[0][0][0][0])
#                           ^extracts value


Gets access to the layer of the current node.
Changes on a 1:len(child_node) ratio
layer = var[file_name][0,10]['layer']
#                         ^extracts layer but sorts in blocks of 5 (0,5,10,15)
print(layer[0][0][0][0])
#                    ^extracts value
'''


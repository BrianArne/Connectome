# TODO Current node method 
# I think all these should be pull into a matlab parser class constructed with a file_name and variable name
# Potentially move out new methods into Matt's old code and see if it works
# Look at python naming conventions

from scipy import io

MATLAB_OFFSET = 1

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
  data = var[file_name][node - MATLAB_OFFSET]
  return data

'''
Returns the layer number of the node
'''
def get_layer_of_node(node_data):
  a = node_data.tolist()
  return a[0]

'''
Returns array of child nodes for a node
'''
def get_child_nodes(file_name, node):
  node_data = access_node_data(file_name, node)
  a = node_data.tolist()
  return a[2]

'''
Returns dictionary layers and their lengths
'''
def get_layer_lens(file_name):
  layer_dict = {}
  for i in range(total_nodes(file_name)):
    data = access_node_data(file_name, i)
    layer = get_layer_of_node(data)
    if layer in layer_dict:
      layer_dict[layer] += 1
    else:
      layer_dict[layer] = 1
  return layer_dict


'''Primitive Testing'''

#Testing globals
brian_test = 'Test'
matt_test = 'T'
num = 1 #must be a number < total_nodes() in both brian_test and matt_test

print
print("***Testing Total Nodes***")
print('Total nodes in ' + brian_test + ': ' + str(total_nodes(brian_test)))
print('Total nodes in ' + matt_test + ': ' + str(total_nodes(matt_test)))

print
print("***Testing Layer***")
matt_data = access_node_data(matt_test, num)
brian_data = access_node_data(brian_test, num)
print('Layer for node ' + str(num) + ' in ' + matt_test + ': ' + str(get_layer_of_node(matt_data)))
print('Layer for node ' + str(num) + ' in ' + brian_test + ': ' + str(get_layer_of_node(brian_data)))

print
print("***Testing child nodes***")
print('Child nodes for node ' + str(num) + ' in ' + matt_test + ': ' + str(get_child_nodes(matt_test, num)))
print('Child nodes for node ' + str(num) + ' in ' + brian_test + ': ' + str(get_child_nodes(brian_test, num)))

print
print("***Testing Get Layer Lens***")
print('Length of layers for ' + matt_test + ': ' + str(get_layer_lens(matt_test)))
print('Length of layers for ' + brian_test + ': ' + str(get_layer_lens(brian_test)))


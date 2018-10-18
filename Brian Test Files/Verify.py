from scipy import io


'''Extracts matlab matricies'''
file_name = "Test"
var = io.loadmat("Test.mat")


'''
Gets access to child node. Can remove the changing value to just get the length
Changes on a 1:5 ratio
'''
#print(var["Test"])
child_nodes = var[file_name][0,5]['child_nodes']
#                              ^somehow controls the block of child_nodes
print(child_nodes[0][0][1][0])
#                       ^is the index of the child nodes


'''
Gets access to the current node. Changes on a 1:1 ratio
'''
current_node = var[file_name][0,1]['current_node']
#                               ^controls current node number
print(current_node[0][0][0][0])
#                           ^extracts value


'''
Gets access to the layer of the current node.
Changes on a 1:len(child_node) ratio
'''
layer = var[file_name][0,10]['layer']
#                         ^extracts layer but sorts in blocks of 5 (0,5,10,15)
print(layer[0][0][0][0])
#                    ^extracts value

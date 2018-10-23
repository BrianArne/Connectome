from scipy import io

'''
Gets the total number of nodes in the matlab file
'''
def total_nodes(file_name): #Do not include .mat extension
    file_with_extension = file_name + '.mat'
    var = io.loadmat(file_with_extension, squeeze_me=True)
    return len(var[file_name])

print(total_nodes('Test'))
print(total_nodes('T'))


#TODO Layer Method, current node method, child nodes of current node method
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

from Containers.Node import *
from Parsers.NodeParser import NodeParser

'''
The JsonNodeParser class is responsible for constructing a node conatiner from a .json file
'''
class JsonNodeParser(NodeParser):

  '''
  Constructor.
  '''
  def __init__(self):
    super(JsonNodeParser, self).__init__(file_name_)
    ...
    # End __init__();

  '''
  Creates a container with all nodes and their data
  '''
  def construct_node_container(self):
    ...
  # End construct_node_container();

# End JsonNodeParser();

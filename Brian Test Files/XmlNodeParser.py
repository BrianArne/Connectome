from Node import *
from NodeParser import NodeParser

'''
The XmlNodeParser class is responsible for constructing a conde conatiner from a .xml file
'''
class XmlNodeParser(NodeParser):

  '''
  Constructor.
  '''
  def __init__(self):
    super(XmlNodeParser, self).__init__(file_name)
    ...

  # End __init__();

  '''
  Creates a container with all nodes and their data
  '''
  def construct_node_container(self):\
    ...
  # End construct_node_container();

# End XmlNodeParser();

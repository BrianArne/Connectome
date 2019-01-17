import abc

# TODO What does __metaclass__ do??

'''
The NodeParser abstract class contains a method for constructing a node container.
'''
class NodeParser(object):

  '''
  Constructor
  '''
  @abc.abstractmethod
  def __init__(self, file_name):
    self._file_name = file_name
    self._node_container = []
  # End __init__();

  '''
  Returns a container with all nodes and their data
  '''
  @abc.abstractmethod
  def construct_node_container(self):
    pass
  # End construct_node_container();

# End NodeParser(ABC) Class;

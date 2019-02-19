import unittest
from Containers.Node import Node
from Containers.NodeContainer import NodeContainer

class TestNodeContainer(unittest.TestCase):

  def setUp(self):
    self._n_one = Node(1, 1, [1,2])
    self._n_two = Node(2, 10, [3, 75])
    self._n_three = Node(3, 30, [])
    self._n_four = Node(3, 75, [])
    self._test_list = [self._n_one, self._n_two, self._n_three, self._n_four]

    self._n_five = Node(1, 1, [])
    self._test_list_two = [self._n_five]

    self._test_empty = []
  # End setup();

  def tearDown(self):
    self._test_list = None
    self._test_list_two = None
    self._test_empty = None
    self._n_one = None
    self._n_two = None
    self._n_three = None
    self._n_four = None
    self._n_five = None

  def test_init(self):

    cont_one = NodeContainer(self._test_list)
    cont_two = NodeContainer(self._test_list_two)
    cont_three = NodeContainer(self._test_empty)

    self.assertEqual(self._test_list, cont_one._nodes)
    self.assertIn(self._n_three, cont_one._input_node_positions)
    self.assertIn(self._n_four, cont_one._input_node_positions)
    self.assertIn(self._n_one, cont_one._output_nodes)
    self.assertEqual(3, cont_one._max_layer)
  
    # This assumes NodeContainers of 1, the 1 is both an input and an output
    self.assertEqual(self._test_list_two, cont_two._nodes)
    self.assertIn(self._n_five, cont_two._output_nodes)
    self.assertIn(self._n_five, cont_two._input_node_positions)
    self.assertEqual(1, cont_two._max_layer)

    self.assertEqual([], cont_three._nodes)
    self.assertEqual([], cont_three._input_node_positions)
    self.assertEqual([], cont_three._output_nodes)
    self.assertEqual(None, cont_three._max_layer)


  # End test_init();

# End TestNodeContainer

import unittest
from Node import *

class TestNode(unittest.TestCase):

  def test_init(self):
    node = Node(1, 1, 1)
    self.assertEqual(1, node._layer)
    self.assertEqual(1, node._node_number)
    self.assertEqual(1, node._input_nodes)

    i_node_arr = Node(5, 11, [5,6])
    self.assertEqual(5, i_node_arr._layer)
    self.assertEqual(11, i_node_arr._node_number)
    self.assertEqual([5,6], i_node_arr._input_nodes)
  # End test_init();

  def test_value_error_layer(self):
    with self.assertRaises(ValueError):
      Node(0, 1, 5)

  def test_value_error_single_inode(self):
    with self.assertRaises(ValueError):
      Node(1, 1, 0)

  def test_value_error_mult_inode(self):
    with self.assertRaises(ValueError):
      Node(1,1, [1,2,3, -7])
  # End test_init();

  def test_str(self):
    node = Node(1, 1, 1)
    correct_str = "Layer: 1 Node: 1 Input Nodes: 1"
    self.assertEqual(correct_str, str(node))

# End TestNode();

if __name__ ==  '__main__':
  unittest.main()

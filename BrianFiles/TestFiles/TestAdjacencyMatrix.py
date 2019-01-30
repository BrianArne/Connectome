import unittest
from Containers.AdjacencyMatrix import AdjacencyMatrix
import Globals


class TestAdjacencyMatrix(unittest.TestCase):

  def setUp(self):
    self._test_nodes = []
    self._test_nodes.append(Node(1, 1, [1,2]) # 0
    self._test_nodes.append(Node(2, 1, [1,2]) # 1
    self._test_nodes.append(Node(2, 2, [7, 30]) # 2
    self._test_nodes.append(Node(3, 1, []) # 3
    self._test_nodes.append(Node(3, 2, []) # 4
    self._test_nodes.append(Node(3, 7, []) # 5
    self._test_nodes.append(Node(3, 30, []) # 6

  # End setUp();


  def tearDown(self):
    self._test_nodes = None
  # End tearDown();

  def test_init(self):


  # End test_init();

  def test_check_termination(self):


  # End test_check_termination();

  def test_construct_empty_matrix(self):


  # End test_construct_empty_matrix();

  def test_fill_matrix(self):


  # End test_fill_matrix();

  def test_init_hash(self):


  # End test_init_hash();

  def test_init_layer_hash(self):


  # End test_init_layer_hash();

  def test_init_position_hash(self):


  # End test_init_position_hash();
  
  def test_max_layer(self):


  # End test_max_layer();

# End TestAdjacencyMatrix();

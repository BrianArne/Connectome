import unittest
from Containers.AdjacencyMatrix import AdjacencyMatrix
from Containers.Node import Node
from Containers.NodeContainer import NodeContainer
import Globals


class TestAdjacencyMatrix(unittest.TestCase):

  def setUp(self):
    self._test_nodes = []
    self._test_nodes.append(Node(1, 1, [1,2]))
    self._test_nodes.append(Node(2, 1, [1,2]))
    self._test_nodes.append(Node(2, 2, [7, 30]))
    self._test_nodes.append(Node(3, 1, []))
    self._test_nodes.append(Node(3, 2, []))
    self._test_nodes.append(Node(3, 7, []))
    self._test_nodes.append(Node(3, 30, []))
    self._test_container_one = NodeContainer(self._test_nodes)
    
    self._test_nodes_two = []
    self._test_nodes_two.append(Node(1, 1, [45,1000]))
    self._test_nodes_two.append(Node(2, 45, []))
    self._test_nodes_two.append(Node(2, 1000, []))
    self._test_container_two = NodeContainer(self._test_nodes_two)
  # End setUp();


  def tearDown(self):
    self._test_nodes = None
    self._test_nodes_two = None
    self._test_container_one = None
    self._test_container_two = None
  # End tearDown();

  def test_init(self):
    adj_matrix = AdjacencyMatrix(self._test_container_one)
    self.assertEqual({} ,adj_matrix._layer_hash)
    self.assertEqual({} ,adj_matrix._position_hash)
    self.assertIsNone(adj_matrix._matrix)
    self.assertEqual(7 ,len(adj_matrix.get_nodes()))
  # End test_init();

  def test_check_termination(self):
    matrix = AdjacencyMatrix([])

    matrix._layer_hash = { 1: {} , 2: {}, 3: {}}
    matrix._layer_hash[1] = {10 : 0, 37 : 1, 40 : 2}
    matrix._layer_hash[2] = {1 : 3, 5 : 4}
    matrix._layer_hash[3] = {20 : 5}

    self.assertTrue(matrix.check_termination(10, 1))
    self.assertTrue(matrix.check_termination(40, 1))
    self.assertTrue(matrix.check_termination(5, 2))
    self.assertTrue(matrix.check_termination(20, 3))

    self.assertFalse(matrix.check_termination(100, 1))
    self.assertFalse(matrix.check_termination(4, 1))
    self.assertFalse(matrix.check_termination(2, 2))
    self.assertFalse(matrix.check_termination(6, 2))
    self.assertFalse(matrix.check_termination(21, 3))
  # End test_check_termination();

  def test_construct_empty_matrix(self):
    adj_matrix = AdjacencyMatrix(self._test_container_one)
    adj_matrix.construct_empty_matrix()
    empty_arr = [0, 0, 0, 0, 0, 0, 0]
    self.assertTrue(7, len(adj_matrix._matrix))
    for i in range(len(adj_matrix._matrix)):
        self.assertEqual(empty_arr, adj_matrix._matrix[i])

    adj_matrix_two = AdjacencyMatrix(self._test_container_two)
    adj_matrix_two.construct_empty_matrix()
    empty_arr_two = [0, 0, 0]
    self.assertTrue(3, len(adj_matrix_two._matrix))
    for i in range(len(adj_matrix_two._matrix)):
      self.assertEqual(empty_arr_two, adj_matrix_two._matrix[i])
  # End test_construct_empty_matrix();

  def test_fill_matrix(self):
    matrix = AdjacencyMatrix(self._test_container_one)
    matrix.fill_matrix()
    correct_matrix = [
        [0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]]
    self.assertEqual(correct_matrix, matrix._matrix)

    matrix_two = AdjacencyMatrix(self._test_container_two)
    matrix_two.fill_matrix()
    correct_matrix_two = [
        [0, 1, 1],
        [0, 0, 0],
        [0, 0, 0]]
    self.assertEqual(correct_matrix_two, matrix_two._matrix)
  # End test_fill_matrix();

  def test_init_hash(self):
    adj_matrix = AdjacencyMatrix(self._test_container_one)
    adj_matrix.fill_matrix()
    for i in range(1, adj_matrix.get_max_layer()+1):
      self.assertTrue(i in adj_matrix._layer_hash.keys())


    adj_matrix_two = AdjacencyMatrix(self._test_container_two)
    adj_matrix_two.fill_matrix()
    for i in range(1, adj_matrix_two.get_max_layer()+1):
      self.assertTrue(i in adj_matrix_two._layer_hash.keys())
  # End test_init_hash();

  def test_init_layer_hash(self):
    adj_matrix = AdjacencyMatrix(self._test_container_one)
    position = 0
    for n in adj_matrix.get_nodes():
      adj_matrix._position_hash[n] = position
      position += 1
    check_dict = {}
    adj_matrix.init_layer_hash(check_dict, 1)
    self.assertEqual(adj_matrix._position_hash[adj_matrix.get_nodes()[0]], check_dict[1])
    check_dict = {}
    adj_matrix.init_layer_hash(check_dict, 3)
    self.assertEqual(adj_matrix._position_hash[adj_matrix.get_nodes()[6]], check_dict[30])


    adj_matrix_two = AdjacencyMatrix(self._test_container_two)
    position = 0
    for n in adj_matrix_two.get_nodes():
      adj_matrix_two._position_hash[n] = position
      position += 1
    check_dict = {}
    adj_matrix_two.init_layer_hash(check_dict, 2)
    self.assertEqual(adj_matrix_two._position_hash[adj_matrix_two.get_nodes()[2]], check_dict[1000])
  # End test_init_layer_hash();

  def test_init_position_hash(self):
    adj_matrix = AdjacencyMatrix(self._test_container_one)
    adj_matrix.init_position_hash()
    self.assertNotEqual({}, adj_matrix._position_hash)
    position = 0 
    for i in adj_matrix.get_nodes():
      self.assertEqual(position, adj_matrix._position_hash[i])
      position += 1
    
    
    adj_matrix_two = AdjacencyMatrix(self._test_container_two)
    adj_matrix_two.init_position_hash()
    self.assertNotEqual({}, adj_matrix_two._position_hash)
    position = 0 
    for i in adj_matrix_two.get_nodes():
      self.assertEqual(position, adj_matrix_two._position_hash[i])
      position += 1
  # End test_init_position_hash();
  
# End TestAdjacencyMatrix();

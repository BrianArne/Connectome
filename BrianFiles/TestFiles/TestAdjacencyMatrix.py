import Globals
import unittest

from Containers.AdjacencyMatrix import AdjacencyMatrix
from Containers.Node import Node
from Containers.NodeContainer import NodeContainer


class TestAdjacencyMatrix(unittest.TestCase):

  def setUp(self):
    self._test_nodes = []
    self._test_nodes.append(Node(1, 1, [1,2])) # 0
    self._test_nodes.append(Node(2, 1, [1,2])) # 1
    self._test_nodes.append(Node(2, 2, [7, 30])) # 2
    self._test_nodes.append(Node(3, 1, [])) # 3
    self._test_nodes.append(Node(3, 2, [])) # 4
    self._test_nodes.append(Node(3, 7, [])) # 5
    self._test_nodes.append(Node(3, 30, [])) # 6
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
    self.assertIsNotNone(adj_matrix._layer_hash)
    self.assertIsNotNone(adj_matrix._position_hash)
    self.assertIsNone(adj_matrix._matrix)
    self.assertEqual(7 ,len(adj_matrix.get_nodes()))
  # End test_init();
  
  # DEPRICATED: Nothing uses this method
  def test_check_termination(self):
    cont = NodeContainer(self._test_nodes)
    matrix = AdjacencyMatrix(cont)

    matrix._layer_hash = { 1: {} , 2: {}, 3: {}}
    matrix._layer_hash[1] = {10 : 0, 37 : 1, 40 : 2}
    matrix._layer_hash[2] = {1 : 3, 5 : 4}
    matrix._layer_hash[3] = {20 : 5}

    self.assertTrue(matrix.check_termination(37, 1))
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

  def test_create_paths(self):
    adj_matrix = AdjacencyMatrix(self._test_container_one)
    adj_matrix.fill_matrix()
    edges = []
    adj_matrix.create_paths(adj_matrix.get_nodes()[0], edges)
    cont_one_paths = [
                     [(0,1), (1,3)],
                     [(0,1), (1,4)],
                     [(0,2), (2,5)],
                     [(0,2), (2,6)]]
    for path in cont_one_paths:
      self.assertIn(path, adj_matrix._paths)

    adj_matrix_two = AdjacencyMatrix(self._test_container_two)
    adj_matrix_two.fill_matrix()
    edges = []
    adj_matrix_two.create_paths(adj_matrix_two.get_nodes()[0], edges)
    cont_two_paths = [
                     [(0,1)],
                     [(0,2)]]
    for path in cont_two_paths:
      self.assertIn(path, adj_matrix_two._paths)
  # End test_create_paths();

  def test_extract_unique_edges(self):
    USER_QUERY = [1]
    adj_matrix = AdjacencyMatrix(self._test_container_one)
    adj_matrix._output_paths[adj_matrix.get_output_nodes()[0]] = [(0,1), (0,1), (0,2)]
    op_edges = adj_matrix.extract_unique_edges(USER_QUERY)
    self.assertEqual([(0,1), (0,2)], op_edges)
  # End test_extract_unique_edges();

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

  def test_get_input_nodes(self):
    input_list = [
        Node(3, 1, []),
        Node(3, 2, []),
        Node(3, 7, []),
        Node(3, 30, [])]
    matrix_one = AdjacencyMatrix(self._test_container_one)
    i = 0
    for n in matrix_one.get_input_nodes():
      self.assertEqual(n._layer, input_list[i]._layer)
      self.assertEqual(n._node_number, input_list[i]._node_number)
      self.assertEqual(n._input_nodes, input_list[i]._input_nodes)
      i += 1
    self.assertEqual(4, len(matrix_one.get_input_nodes()))

    input_list_two = [
        Node(2, 45, []),
        Node(2, 1000, [])]
    matrix_two = AdjacencyMatrix(self._test_container_two)
    i = 0
    for n in matrix_two.get_input_nodes():
      self.assertEqual(n._layer, input_list_two[i]._layer)
      self.assertEqual(n._node_number, input_list_two[i]._node_number)
      self.assertEqual(n._input_nodes, input_list_two[i]._input_nodes)
      i += 1
    self.assertEqual(2, len(matrix_two.get_input_nodes()))
  # End test_get_input_nodes();

  def test_get_max_layer(self):
    matrix_one = AdjacencyMatrix(self._test_container_one)
    self.assertEqual(3, matrix_one.get_max_layer())

    matrix_two = AdjacencyMatrix(self._test_container_two)
    self.assertEqual(2, matrix_two.get_max_layer())
  # End test_get_max_layer();

  def test_get_nodes(self):
    matrix_one = AdjacencyMatrix(self._test_container_one)
    self.assertEqual(self._test_nodes, matrix_one.get_nodes())

    matrix_two = AdjacencyMatrix(self._test_container_two)
    self.assertEqual(self._test_nodes_two, matrix_two.get_nodes())
  # End test_get_nodes();

  def test_get_output_nodes(self):
    output_list = [Node(1, 1, [1,2])]
    matrix_one = AdjacencyMatrix(self._test_container_one)
    i = 0
    for n in matrix_one.get_output_nodes():
      self.assertEqual(n._layer, output_list[i]._layer)
      self.assertEqual(n._node_number, output_list[i]._node_number)
      self.assertEqual(n._input_nodes, output_list[i]._input_nodes)
      i += 1
    self.assertEqual(1, len(matrix_one.get_output_nodes()))


    output_list_two = [Node(1, 1, [45,1000])]
    matrix_two = AdjacencyMatrix(self._test_container_two)
    i = 0
    for n in matrix_two.get_output_nodes():
      self.assertEqual(n._layer, output_list_two[i]._layer)
      self.assertEqual(n._node_number, output_list_two[i]._node_number)
      self.assertEqual(n._input_nodes, output_list_two[i]._input_nodes)
      i += 1
    self.assertEqual(1, len(matrix_two.get_output_nodes()))

  # End test_get_output_nodes();

  def test_generate_all_output_paths(self):
    adj_matrix = AdjacencyMatrix(self._test_container_one)
    adj_matrix.fill_matrix()
    adj_matrix.generate_all_output_paths()

    node_one_paths = adj_matrix._output_paths[adj_matrix.get_output_nodes()[0]]
    self.assertIn((0,1), node_one_paths)
    self.assertIn((1,3), node_one_paths)
    self.assertIn((1,4), node_one_paths)
    self.assertIn((0,2), node_one_paths)
    self.assertIn((2,5), node_one_paths)
    self.assertIn((2,6), node_one_paths)


    adj_matrix_two = AdjacencyMatrix(self._test_container_two)
    adj_matrix_two.fill_matrix()
    adj_matrix_two.generate_all_output_paths()
    node_one_paths_two = adj_matrix_two._output_paths[adj_matrix_two.get_output_nodes()[0]]
    self.assertIn((0,1), node_one_paths_two)
    self.assertIn((0,2), node_one_paths_two)
  # End test_generate_all_output_paths();

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

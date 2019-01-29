import unittest
from Parsers.MatlabNodeParser import MatlabNodeParser
import Globals

class TestMatlabNodeParser(unittest.TestCase):

  def setUp(self):
      set_one_file_name = "SetOne.mat"
      set_one_var_name = "SetOne"
      self.set_one_data = MatlabNodeParser(Globals.TESTING_DIR + set_one_file_name, set_one_var_name)

      set_two_file_name = "SetTwo.mat"
      set_two_var_name = "SetTwo"
      self.set_two_data = MatlabNodeParser(Globals.TESTING_DIR+ set_two_file_name, set_two_var_name)

      set_three_file_name = "SetThree.mat"
      set_three_var_name = "SetThree"
      self.set_three_data = MatlabNodeParser(Globals.TESTING_DIR + set_three_file_name, set_three_var_name)

      set_test_file_name = "Test.mat"
      set_test_var_name = "Test"
      self.set_test_data = MatlabNodeParser(Globals.TESTING_DIR + set_test_file_name, set_test_var_name)

      set_t_file_name = "T.mat"
      set_t_var_name = "T"
      self.set_t_data = MatlabNodeParser(Globals.TESTING_DIR + set_t_file_name, set_t_var_name)

      self._containers = []
      self._containers.append(self.set_one_data)
      self._containers.append(self.set_two_data)
      self._containers.append(self.set_three_data)
      self._containers.append(self.set_test_data)
      self._containers.append(self.set_t_data)

  # End setUp();

  def tearDown(self):
    for c in self._containers:
      c = None
  # End tearDown();

  def test_init(self):

      self.assertEqual(self.set_one_data._var_name,"SetOne")
      self.assertEqual(self.set_two_data._var_name, "SetTwo")
      self.assertEqual(self.set_three_data._var_name, "SetThree")
      self.assertEqual(self.set_test_data._var_name, "Test")
      self.assertEqual(self.set_t_data._var_name, "T")

      self.assertEqual(self.set_one_data._file_name, Globals.TESTING_DIR + "SetOne.mat")
      self.assertEqual(self.set_two_data._file_name, Globals.TESTING_DIR + "SetTwo.mat")
      self.assertEqual(self.set_three_data._file_name, Globals.TESTING_DIR + "SetThree.mat")
      self.assertEqual(self.set_test_data._file_name, Globals.TESTING_DIR + "Test.mat")
      self.assertEqual(self.set_t_data._file_name, Globals.TESTING_DIR + "T.mat")
  # End test_init();

  def test_construct_i_nodes(self):
    i_nodes = [5, 6, 7]

    for c in self._containers:
      c.construct_i_nodes(4, i_nodes)

    for c in self._containers:
      self.assertEqual(3, len(c._node_container))
      self.assertEqual(5, c._node_container[0]._node_number)
      self.assertEqual(7, c._node_container[2]._node_number)
      self.assertEqual(5, c._node_container[0]._layer)
      self.assertEqual(5, c._node_container[2]._layer)
  # End test_construst_i_nodes();
    
  def test_zero_i_nodes(self):
    i_nodes = []
    for c in self._containers:
      c.construct_i_nodes(4, i_nodes)
    for c in self._containers:
      self.assertEqual([], c._node_container)
  # End test_zero_i_nodes

  def test_construct_node_container(self):
    for c in self._containers:
      c.load_data()
      c.construct_node_container()

    # Checks constructed node length 
    self.assertEqual(9, len(self._containers[0]._node_container))
    self.assertEqual(7, len(self._containers[1]._node_container))
    self.assertEqual(5, len(self._containers[2]._node_container))

    # Checks _total_nodes
    self.assertEqual(6 , self._containers[0]._total_nodes)
    self.assertEqual(5 , self._containers[1]._total_nodes)
    self.assertEqual(3 , self._containers[2]._total_nodes)
    self.assertEqual(20 , self._containers[3]._total_nodes)
    self.assertEqual(88 , self._containers[4]._total_nodes)
    
    # Checks _data
    self.assertIsNotNone(self._containers[0]._data)
    self.assertEqual(type(self._containers[0]._data), dict)
    self.assertIsNotNone(self._containers[1]._data)
    self.assertEqual(type(self._containers[1]._data), dict)
    self.assertIsNotNone(self._containers[2]._data)
    self.assertEqual(type(self._containers[2]._data), dict)
    self.assertIsNotNone(self._containers[3]._data)
    self.assertEqual(type(self._containers[3]._data), dict)
    self.assertIsNotNone(self._containers[4]._data)
    self.assertEqual(type(self._containers[4]._data), dict)
  # End construct_node_container();

  def test_get_data_layer(self):
    for c in self._containers:
      c.load_data()
    
    self.assertEqual(1 , self._containers[0].get_data_layer(0))
    self.assertEqual(2 , self._containers[0].get_data_layer(2))
    self.assertEqual(3 , self._containers[0].get_data_layer(5))
    self.assertEqual(int , type(self._containers[0].get_data_layer(5)))
    self.assertRaises(IndexError, self._containers[0].get_data_layer(6))
        
    self.assertEqual(1 , self._containers[1].get_data_layer(0))
    self.assertEqual(1 , self._containers[1].get_data_layer(1))
    self.assertEqual(3 , self._containers[1].get_data_layer(4))
    self.assertEqual(int , type(self._containers[1].get_data_layer(4)))
    self.assertRaises(IndexError, self._containers[1].get_data_layer(5))

    self.assertEqual(1 , self._containers[2].get_data_layer(0))
    self.assertEqual(2 , self._containers[2].get_data_layer(1))
    self.assertEqual(2 , self._containers[2].get_data_layer(2))
    self.assertEqual(int , type(self._containers[1].get_data_layer(0)))
    self.assertRaises(IndexError, self._containers[2].get_data_layer(3))

    # Need matlab to implement
    '''
    self.assertEqual(1 , self._containers[0].get_data_layer(0))
    self.assertEqual(2 , self._containers[0].get_data_layer(2))
    self.assertEqual(3 , self._containers[0].get_data_layer(5))

    self.assertEqual(1 , self._containers[0].get_data_layer(0))
    self.assertEqual(2 , self._containers[0].get_data_layer(2))
    self.assertEqual(3 , self._containers[0].get_data_layer(5))
    '''
  # End test_get_data_layer();

  def test_get_data_current_node(self):
    for c in self._containers:
      c.load_data()

    self.assertEqual(1 , self._containers[0].get_data_current_node(0))
    self.assertEqual(30 , self._containers[0].get_data_current_node(3))
    self.assertEqual(40 , self._containers[0].get_data_current_node(5))
    self.assertEqual(int , type(self._containers[0].get_data_current_node(5)))
    self.assertRaises(IndexError, self._containers[0].get_data_layer(6))
        
    self.assertEqual(1 , self._containers[1].get_data_current_node(0))
    self.assertEqual(4 , self._containers[1].get_data_current_node(2))
    self.assertEqual(15 , self._containers[1].get_data_current_node(4))
    self.assertEqual(int , type(self._containers[1].get_data_current_node(0)))
    self.assertRaises(IndexError, self._containers[1].get_data_layer(5))

    self.assertEqual(1 , self._containers[2].get_data_current_node(0))
    self.assertEqual(1 , self._containers[2].get_data_current_node(1))
    self.assertEqual(5 , self._containers[2].get_data_current_node(2))
    self.assertEqual(int , type(self._containers[2].get_data_current_node(1)))
    self.assertRaises(IndexError, self._containers[2].get_data_layer(3))

    # Need matlab to implement
    '''
    self.assertEqual(1 , self._containers[0].get_data_layer(0))
    self.assertEqual(2 , self._containers[0].get_data_layer(2))
    self.assertEqual(3 , self._containers[0].get_data_layer(5))

    self.assertEqual(1 , self._containers[0].get_data_layer(0))
    self.assertEqual(2 , self._containers[0].get_data_layer(2))
    self.assertEqual(3 , self._containers[0].get_data_layer(5))
    '''
  # End test_get_data_current_node();

  def test_get_data_input_nodes(self):
    for c in self._containers:
      c.load_data()

    self.assertEqual([1, 7] , self._containers[0].get_data_input_nodes(0))
    self.assertEqual([42] , self._containers[0].get_data_input_nodes(3))
    self.assertEqual([100] , self._containers[0].get_data_input_nodes(5))
    self.assertEqual(list , type(self._containers[0].get_data_input_nodes(0)))
    self.assertEqual(list , type(self._containers[0].get_data_input_nodes(5)))
    self.assertRaises(IndexError, self._containers[0].get_data_layer(6))
    
    self.assertEqual([4] , self._containers[1].get_data_input_nodes(0))
    self.assertEqual([15] , self._containers[1].get_data_input_nodes(3))
    self.assertEqual([1, 2] , self._containers[1].get_data_input_nodes(4))
    self.assertEqual(list , type(self._containers[1].get_data_input_nodes(0)))
    self.assertEqual(list , type(self._containers[1].get_data_input_nodes(4)))
    self.assertRaises(IndexError, self._containers[1].get_data_layer(5))

    self.assertEqual([1, 5] , self._containers[2].get_data_input_nodes(0))
    self.assertEqual([9] , self._containers[2].get_data_input_nodes(1))
    self.assertEqual([2] , self._containers[2].get_data_input_nodes(2))
    self.assertEqual(list , type(self._containers[2].get_data_input_nodes(0)))
    self.assertEqual(list , type(self._containers[2].get_data_input_nodes(2)))
    self.assertRaises(IndexError, self._containers[2].get_data_layer(3))

    # Need matlab to implement
    '''
    self.assertEqual(1 , self._containers[0].get_data_layer(0))
    self.assertEqual(2 , self._containers[0].get_data_layer(2))
    self.assertEqual(3 , self._containers[0].get_data_layer(5))

    self.assertEqual(1 , self._containers[0].get_data_layer(0))
    self.assertEqual(2 , self._containers[0].get_data_layer(2))
    self.assertEqual(3 , self._containers[0].get_data_layer(5))
    '''
  # End test_get_data_input_nodes();

  def test_load_data(self):
    bad_file = "bad"
    bad_var = ""
    bad_load = MatlabNodeParser(bad_file, bad_var)
    self.assertRaises(IOError, bad_load.load_data())
  # End test_load_data();

# End TestMatlabNodeParser();

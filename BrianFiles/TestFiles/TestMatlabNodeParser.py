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

      for c in self._containers:
          c.load_data()
          c.construct_node_container()

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

  def test_construct_node_container(self):
      for c in self._containers:
          self.assertIsNotNone(c._node_container)
          self.assertGreater(len(c._node_container), 0)
  # End construct_node_container();

  def test_get_data_layer(self):
    pass

  # End test_get_data_layer();

  def test_get_data_current_node(self):
    pass

  # End test_get_data_current_node();

  def test_get_data_input_nodes(self):
    pass

  # End test_get_data_input_nodes();

  def test_load_data(self):
    pass


  # End test_load_data();




# End TestMatlabNodeParser();

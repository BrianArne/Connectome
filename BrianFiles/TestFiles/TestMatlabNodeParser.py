import unittest
from Parsers.MatlabNodeParser import MatlabNodeParser
import Globals

class TestMatlabNodeParser(unittest.TestCase):

  def setUp(self):
    set_one_file_name = "SetOne.mat"
    set_one_var_name = "SetOne"
    set_one_data = MatlabNodeParser(Globals.TESTING_DIR, set_one_var_name)

  def test_init(self):
    pass

  # End test_init();

  def test_construct_node_container(self):
    pass

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

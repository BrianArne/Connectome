import os.path
import sys
import unittest


from Containers.AtlasMatrix import AtlasMatrix
from Containers.Node import Node
from Containers.NodeContainer import NodeContainer


class TestAtlasMatrix(unittest.TestCase):

  def setUp(self):
    self._file = "./TestFiles/aalTest.csv"
    self._n_one = Node(1, 1, [])
    self._n_two = Node(1, 2, [])
    self._n_three = Node(1, 3, [])
    self._list = [self._n_one, self._n_two, self._n_three]
  # End setUp();

  def tearDown(self):
    self._n_one = None
    self._n_two = None 
    self._n_three = None
    self._list = None 
  # End tearDown();

  def test_init(self):
    atlas = AtlasMatrix(self._file, self._list)
    correct_matrix = {
                      1 : (0,1),
                      2 : (0,2),
                      3 : (1,2)}
    self.assertEqual(correct_matrix, atlas._feature_to_matrix_hash)

    f = open('atlas.node', 'r')
    self.assertIsNotNone(f.readline())

    correct = [
              [0, 1, 2],
              [0, 0, 3],
              [0, 0, 0]]
    self.assertEqual(correct, atlas._atlas_matrix)

    self.assertIsNotNone(atlas._regions_list)
  # End test_init();

  def test_add_features_to_matrix(self):
    atlas = AtlasMatrix(self._file, self._list)
    correct = [
              [0, 1, 2],
              [0, 0, 3],
              [0, 0, 0]]
    self.assertEqual(atlas._atlas_matrix, correct)
    self.assertEqual(atlas._feature_to_matrix_hash[1], (0,1))
    self.assertEqual(atlas._feature_to_matrix_hash[2], (0,2))
    self.assertEqual(atlas._feature_to_matrix_hash[3], (1,2))
  # End test_add_features_to_matrix();

  def test_create_atlas_region_list(self):
    atlas = AtlasMatrix(self._file, self._list)
    atlas.create_atlas_region_list(self._file)
    self.assertEqual(3, len(atlas._regions_list))

    self.assertEqual(str(1.0), atlas._regions_list[0][0])
    self.assertEqual(str(-4.0), atlas._regions_list[1][0])
    self.assertEqual(str(7.7), atlas._regions_list[2][0])

    self.assertEqual(str(3.0), atlas._regions_list[0][2])
    self.assertEqual(str(-5.0), atlas._regions_list[1][1])
    self.assertEqual(str(9.9), atlas._regions_list[2][2])

    self.assertEqual('Region_1\n', atlas._regions_list[0][3])
    self.assertEqual('Region_2\n', atlas._regions_list[1][3])
    self.assertEqual('Region_3\n', atlas._regions_list[2][3])
  # End test_create_atlas_region_list();

  def test_create_surfice_node_file(self):
    atlas = AtlasMatrix(self._file, self._list)

    line_one = '1.0\t2.0\t3.0\t1\t2.2\tRegion_1\n'
    line_two = '-4.0\t-5.0\t-6.0\t1\t2.2\tRegion_2\n'
    line_three = '7.7\t8.8\t9.9\t1\t2.2\tRegion_3\n'

    f = open('atlas.node', 'r')
    one = f.readline()
    self.assertEqual(one, line_one)

    two = f.readline()
    self.assertEqual(two, line_two)
    
    three = f.readline()
    self.assertEqual(three, line_three)
  # End test_create_surfice_node_file();

# End Class TestAtlasMatrix();

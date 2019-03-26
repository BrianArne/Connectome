class AtlasMatrix:

  '''
  Responsible for parsing atlas csv files creating a connectivity adjacency matrix, hash lookup
  for each feature number in that matrix, and creating a .node file to be used by SurfIce
  '''
  def __init__(self, file_name, input_nodes):
    self._feature_to_matrix_hash = None
    self._atlas_matrix = None
    self._regions_list = None

    # Init functions
    self.create_atlas_region_list(file_name)
    self.add_features_to_matrix()
    self.create_surfice_node_file(input_nodes)
  # End __init__();

  '''
  Fills _atlas_matrix with features for each (x,y) in the top half of _atlas_matrix
  Initializes the _feature_to_matrix_hash for looking up (x,y) for a given feature number
  '''
  def add_features_to_matrix(self):
    self._atlas_matrix = [[0] * len(self._regions_list) \
                   for n in range(len(self._regions_list))]
    feature_id = 1 # 1 index because all nodes are 1 indexed
    offset = 1
    self._feature_to_matrix_hash = {}
    for i in range(len(self._atlas_matrix)):
      for j in range(offset, len(self._atlas_matrix[i])):
          self._atlas_matrix[i][j] = feature_id
          self._feature_to_matrix_hash[feature_id] = (i, j)
          feature_id += 1
      offset += 1
  # End add_features_to_matrix();

  '''
  Creates a list of rgions from the atlas file supplied
  !Regions names will be strings terminating in \n
  '''
  def create_atlas_region_list(self, file_name):
    with open(str(file_name)) as f:
        self._regions_list = [map(str, i.split(',')) for i in f]
  # End create_atlas_region_list();


  '''
  Uses _feature_to_matrix_hash to create a .node file used in SurfIce script
  Should user be able to supply node file name?
  '''
  def create_surfice_node_file(self, input_nodes):
    # Creates list of unique input regions for each input tuple of connectivity
    l_nodes = []
    for n in input_nodes:
      draw_nodes = self._feature_to_matrix_hash[n._node_number]
      if draw_nodes[0] not in l_nodes:
        l_nodes.append(draw_nodes[0])
      if draw_nodes[1] not in l_nodes:
        l_nodes.append(draw_nodes[1])

    # Writes data to file
    try:
      f = open("atlas.node", "w+")
    except IOError:
      print("Error opening atlas file. Terminating...")

    for index in l_nodes:
      reg = self._regions_list[index]
      x = reg[0]
      y = reg[1]
      z = reg[2]
      name = reg[3]
      f.write(x + '\t' + y + '\t' + z + '\t' + str(1) + '\t' + str(2.2) + '\t' + name)
    f.close()
  # End create_surfice_node_file();

# End class AtlasMatrix;

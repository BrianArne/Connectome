class AtlasMatrix:

  '''
  Responsible for parsing atlas csv files creating a connectivity adjacency matrix, hash lookup
  for each feature number in that matrix, and creating a .node file to be used by SurfIce
  '''
  def __init__(self, file_name, input_nodes):
    self._feature_to_matrix_hash = None
    self._atlas_matrix = None
    self._regions_list = None
    self._l_nodes = []
    
    #TODO: figure if _edge_matrix is still needed
    self._edge_matrix = None #?? NEEDED??

    # Init functions
    self.create_atlas_region_list(file_name)
    self.add_features_to_matrix()
    self.create_surfice_node_file(input_nodes)
    self.create_surfice_edge_file()
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
    self._l_nodes = []
    for n in input_nodes:
      draw_nodes = self._feature_to_matrix_hash[n._node_number]
      if draw_nodes[0] not in self._l_nodes:
        self._l_nodes.append(draw_nodes[0])
      if draw_nodes[1] not in self._l_nodes:
        self._l_nodes.append(draw_nodes[1])

    # Writes data to file
    try:
      f = open("atlas.node", "w+")
    except IOError:
      print("Error opening atlas file. Terminating...")
    
    for index in self._l_nodes:
      #self._ATLAS_NODE_LINES+=1
      reg = self._regions_list[index]
      x = reg[0]
      y = reg[1]
      z = reg[2]
      name = reg[3]
      f.write(x + '\t' + y + '\t' + z + '\t' + str(0.0) + '\t' + str(0.0) + '\t' + name)
    f.close()
  # End create_surfice_node_file();
  
  '''
  Modify atlas.node file's size and color values for selected region pairs.  The method is designed to iterate through a list of region pairs, performing the same operation defined in the second argument to each region's line in the atlas.node file.
  
  Input value selected_lines is a list of tuples, each tuple being the two lines in the atlas.node file corresponding to the pair of regions.  The list of tuples will be iterated through, changing the values as defined by val_ops.
  
  Input value val_ops is a string that gets interpreted as the operation(s) to be performed on the color and/or size value(s) of each line defined by the selected_lines tuples.  The string is interpreted as a MAX OF TWO operations, one to be performed on the color value and the other on the size value, ordering does not matter.  Format for each operation is two leading character and a float value.  First character is the attribute to be changed, either 'c' for color or 's' for size.  Second character is the operation to be performed, either '+' for adding to current value, '-' for subtracting from current value, '=' for simply setting a new value. The float value is what is being added to, subtracted from, or defining the current value in the file.  Value must be in decimal float format, like 2.0 or 6.876, as there seem to be unexpected errors if otherwise.
  
  Ex1: selected_lines = [(1,3),(0,2),(0,4)], val_ops = "c+2.0,s=3.2" would iterate through the three tuple indexes in selected_lines, changing the nodes' colors to whatever the values were plus 2.0, and setting the sizes to 3.2.  Since line 0 is found in two tuples, 2.0 will be added twice to its original color value.
  
  Ex2: "c-3.1,s+1.1" and "s+1.1,c-3.1" give the same results.
  
  Ex3: "c=5.0,", "c=5.0,s", "c=5.0,s=", and "c=5.0,s=2.0a" all would result in an error, as the second operation string is not of the formats defined above. also, 
  
  Note: the lowest value of threshold Surf-Ice will admit is 0.0.  If the size value of a node in the atlas.node file is "0.0" the node disappears from the Surf Ice graph, regardless if choosing "Threshold based on size" or "Threshold based on color" and the range of 0.0 is allowed, since radius of 0.0 is sizeless anyhow.  Color set to 0.0 still shows up, as the range for "Threshold based on color" allows for it and the physical rendering of that object doesn't make it non-existent, like the size.  Negative values in either size or color, however, will still allow the node to appear if 1.) exclusively either size or color is negative, and 2.) size is not 0.0.  ***This can be avoided as long as the atlas.node file is originally formatted with create_surfice_node_file() to have "0.0" placed in those fields, and change_node_file_values() can catch potentially negative values and deal with them accordingly.***
  
  TODO: 1. set it up so method throws errors if val_ops not of correct format, too many operations parsed, both operations to the same attribute, or catches if resulting size value would be negative (nodes still get displayed if size is negative, just inverted sides or interior/exterior).
  2. improve iteration to perform all operations to be performed on a given line in one pass
  '''
  def change_node_file_values(self, selected_lines, val_ops):
    val_ops = val_ops.split(',')
    
    try:
        f = open("atlas.node", "r+")
        f_lines = f.readlines()
        for line_tuple in selected_lines: #should improve to do all iterations over a certain line in one pass
            for line_num in line_tuple:
                x, y, z, color, size, region = f_lines[line_num].split('\t')
                for ops in val_ops:
                    if ops[0] == 'c': #try-catch EOF for incorrect strings in evals()?
                        if ops[1] == '=':
                            color = float(eval(ops[2:]))
                        else:
                            color = eval('float(color)' + ops[1:])
                    elif ops[0] == 's':
                        if ops[1] == '=':
                            size = float(eval(ops[2:]))
                        else:
                            size = eval('float(size)' + ops[1:])
                    else:
                        #throw EOF or something, maybe just f.close() instead of f.writelines(f_lines) first?
                        print "error, ops[0] not 'c' or 's': %c" % ops[0]
                        
                out_string = str(x + '\t' + y + '\t' + z + '\t' + str(color) + '\t' + str(size) + '\t' + region)
                f_lines[line_num] = out_string
        
        f.seek(0)
        f.writelines(f_lines)
        f.close()
    except IOError:
        print("Error opening and/or editing atlas file.")
        exit()
    
  # End change_node_file_values();
  
  '''
  Creates the atlas.edge file used to define the edges to be drawn between specific nodes.  File is formatted as a '\t'-spaced n x n matrix, with index (x,y) denoting lines x and y of the atlas.node file and the corresponding regions to be connected.  Surf-Ice seems to only read the top half of the matrix ("above" x=y line), and that is the format this method is designed to write (all values "below" x=y line are 0.0).
  
  TODO: figure if need to self. the _edge_matrix for further use or not.
  '''
  def create_surfice_edge_file(self): #creates file array of 0's
    #get rid of self._edge_matrix and just use this in for loop?
    self._edge_matrix = [[0.0] * len(self._l_nodes) for n in range(len(self._l_nodes))]
    
    write_list = []
    for i in range(len(self._l_nodes)):
        line = '\t'.join(str(self._edge_matrix[i][n]) for n in range(len(self._l_nodes))) + '\n'
        write_list.append(line)
    
    try:
        f = open("atlas.edge", "w+")
        f.writelines(write_list)
        f.close()
    except IOError:
        print("Error opening and/or editing edge file. Terminating...")
  # End create_surfice_edge_file();
  
  '''
  Modify atlas.edge file's size values for selected region pairs.  Designed to iterate through a list of region pairs, setting the corresponding value to val_ops.
  
  Input value selected_lines is a list of tuples, each tuple being the coordinates in the atlas.edge file's '\t'-spaced n x n formatting corresponding the edge connecting the (x,y) regions; the value at that coordinate is the edge's thickness.  The list of tuples will be iterated through, changing the values as defined by val_ops.
  
  Currently the val_ops argument is just a float value that you wish to set the edge's weight as.
  
  Note: setting weight as 0.0 makes the edge not appear in Surf-Ice.  Setting weight to negative value seems to just create another "Edges" section and sets color to the next selection under what the original "Edges" section has set.  Selecting the last selection for the original "Edges" section causes an error, probably from requesting an out-of-bounds index from the list.  ***Make sure to not allow values in atlas.edge to be set to below 0.0.***
  
  TODO: 1. make val_ops variable and interpretation like that of change_node_file_values()
  2. add catches and input data checks
  3. improve efficiency
  '''
  def change_edge_file_values(self, selected_lines, val_ops):

    try: 
        f = open("atlas.edge", "r+")
        f_lines = f.readlines()
        
        for line_tuple in selected_lines:
            x = line_tuple[0]
            y = line_tuple[1]
            
            if(x < y):
                temp = x
                x = y
                y = temp
                temp = None
            #elif(x == y): #should never be the same
                #throw error
            
            
            yline = f_lines[y] #may be better method
            yline = yline.split('\t') #for loop iterating through instead?
            #for 
            yline[x] = str(val_ops)
            yline = '\t'.join(yline[n] for n in range(len(yline)))
            if yline[-1] != '\n':
                yline = yline + '\n'
            f_lines[y] = yline
        
        f.seek(0)
        f.writelines(f_lines)
        f.close
    except IOError:
        print("Error opening and/or editing edge file. Terminating...")
    
  #End change_edge_file_values();
# End class AtlasMatrix;

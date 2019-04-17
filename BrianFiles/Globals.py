import sys
from Parsers.MatlabNodeParser import MatlabNodeParser

# Largely used just for testing
WORKING_DIR = sys.path[0]
TESTING_FILES_DIR = "/Test/MatlabFiles/"
TESTING_DIR = WORKING_DIR + TESTING_FILES_DIR

# Used for subprocess call in Connectome.py
SURFICE_DIR = '/home/workstation6/sw/surfice/Surf_Ice/surfice'
ATLASNODE_DIR = sys.path[0] + '/atlas.node'
SURFICE_SCRIPT = 'BEGIN RESETDEFAULTS;MESHLOAD(\'BrainMesh_ICBM152.mz3\');NODELOAD(\'' + ATLASNODE_DIR + '\');SHADERXRAY(0.5, 0.1);END.'
###################
## Query Methods ##
###################
'''
Ask the user for a file path to atlas file
'''
def query_atlas_file():
  atlas_file_path = raw_input("Please enter the relative location of the atlas file: ")
  return sys.path[0] + atlas_file_path
# End query_atlas_file()

'''
Ask the user for a file path and loads data
'''
def query_file():
  file_path = raw_input("Please enter the relative location of matlab node file: ")
  file_path = sys.path[0] + file_path
  print(file_path)
  var_name = raw_input("Which variable from " + file_path + " would you like to process? ")
  parsed_data = MatlabNodeParser(file_path, var_name)
  try:
    parsed_data.load_data()
  except IOError:
    print("Bad user data. Terminating...")
    exit()
  return parsed_data
# End query_file()

'''
Ask the user for a file and loads data
@Returns NodeParser
'''
def query_test_file(jupyter=False):
  # File options
  var = input("Which test file? " + 
              "1) SetOne "+ 
              "2) SetTwo "+ 
              "3) SetThree "+ 
              "4) Test "+ 
              "5) T ")
  if var == 1:
    file_name = TESTING_DIR  + "SetOne.mat"
    var_name = "SetOne"
  elif var == 2:
    file_name = TESTING_DIR + "SetTwo.mat"
    var_name = "SetTwo"
  elif var == 3:
    file_name = TESTING_DIR + "SetThree.mat"
    var_name = "SetThree"
  elif var == 4:
    file_name = TESTING_DIR + "Test.mat"
    var_name = "Test"
  elif var == 5:
    file_name = TESTING_DIR + "T.mat"
    var_name = "T"
  else:
    print("Bad input = SetOne")
    file_name = "SetOne.mat"
    var_name = "SetOne"

  if(jupyter):
    file_name = '.' + file_name

  # Load data
  parsed_data = MatlabNodeParser(file_name, var_name)
  try:
    parsed_data.load_data()
  except IOError:
      print("Terminating...")
      exit()

  return parsed_data
# End query_test_file();

'''
Ask user forrequested outputs
@Returns list of integers representing outputs
'''
def query_outputs(outputs):
  list_output_nums = [n._node_number for n in outputs]
  query = [int(n) for n in raw_input("Select which outputs would you like to see, seperate by a space " + str(list_output_nums) + ": ").split()]
  for q in query:
    if q not in list_output_nums:
      raise Exception("Number provided: " + str(q) + " is not an available output:")
  return query
# End query_outputs;

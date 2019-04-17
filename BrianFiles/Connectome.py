import Globals
import subprocess
import sys

from Containers.AtlasMatrix import AtlasMatrix
from Containers.NodeContainer import NodeContainer
from Containers.AdjacencyMatrix import AdjacencyMatrix
from GUI.ChordGraph import ChordGraph

# Picks file to run
data = Globals.query_test_file()
data.construct_node_container()

# Init. AdjacencyMatrix to generate all graph traverseals
container = NodeContainer(data._node_container)
connect = AdjacencyMatrix(container)
user_query = Globals.query_outputs(connect.get_output_nodes())

# Creates all paths
connect.generate_all_output_paths()

# Create Edges
edges = connect.extract_unique_edges(user_query)
edges.sort(key=lambda tup: tup[0])

# Create Atlas Connectivty Matrix, Freature Mapping, and .Node file
atlas = AtlasMatrix(sys.path[0] + "/Atlas/aal.csv", connect.get_input_nodes())
'''User chosen atlas file. Uncomment'''
# atlas = AtlasMatrix(query_atlas_file(), connect.get_input_nodes())

# Graph Chord Diagram
chord = ChordGraph(connect.get_nodes(), edges, connect.get_max_layer(), atlas)
chord.draw()

# Displays 3D surfice rendering
# NOTE: Path to SurfIce will be system dependent.
subprocess.call([Globals.SURFICE_DIR,'-S', Globals.SURFICE_SCRIPT])

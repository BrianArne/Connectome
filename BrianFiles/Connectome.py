import Globals #Mostly testing variables
import sys
import numpy as np
import plotly
import plotly.graph_objs as go
import subprocess

from Containers.NodeContainer import NodeContainer
from Containers.AdjacencyMatrix import AdjacencyMatrix
from Parsers.MatlabNodeParser import MatlabNodeParser
from igraph import *

'''
List of copied functions from plot.ly
1) dist(A,B)
2) get_idx_interv(d, D)
3) BezierCv(b, nr)
4) deCasteljau
5) InvalidInputError
'''

'''
Class used in deCasteljau for exception throwing
'''
class InvalidInputError(Exception):
  pass
# End Class InvalidInputError()

#############################
######## FUNCTIONS  #########
#############################

'''
Used to create aesthetic curve from node to node
'''
def BezierCv(b, nr=5):
  t=np.linspace(0, 1, nr)
  return np.array([deCasteljau(b, t[k]) for k in range(nr)]) 
# End BezierCv();

'''
Used to create aesthetic curve from node to node
'''
def deCasteljau(b,t): 
  N=len(b) 
  if(N<2):
    raise InvalidInputError("The  control polygon must have at least two points")
  a=np.copy(b) #shallow copy of the list of control points 
  for r in range(1,N): 
    a[:N-r,:]=(1-t)*a[:N-r,:]+t*a[1:N-r+1,:]                             
  return a[0,:]
# End deCasteljau();

'''
@Returns the distance between 2 points A and B
'''
def dist (A,B):
  return np.linalg.norm(np.array(A)-np.array(B))
# End dist();


'''
Returns index of the interval the distance d belongs to
'''
def get_idx_interv(d, D):
  k=0
  while(d>D[k]): 
    k+=1
  return  k-1
# End get_idx_interv();

'''
Ask the user for a file and loads data
@Returns NodeParser
'''
def query_file():
  # File options
  var = input("Which test file? " + 
              "1) SetOne "+ 
              "2) SetTwo "+ 
              "3) SetThree "+ 
              "4) Test "+ 
              "5) T ")
  if var == 1:
    file_name = Globals.TESTING_DIR  + "SetOne.mat"
    var_name = "SetOne"
  elif var == 2:
    file_name = Globals.TESTING_DIR + "SetTwo.mat"
    var_name = "SetTwo"
  elif var == 3:
    file_name = Globals.TESTING_DIR + "SetThree.mat"
    var_name = "SetThree"
  elif var == 4:
    file_name = Globals.TESTING_DIR + "Test.mat"
    var_name = "Test"
  elif var == 5:
    file_name = Globals.TESTING_DIR + "T.mat"
    var_name = "T"
  else:
    print("Bad input = SetOne")
    file_name = "SetOne.mat"
    var_name = "SetOne"

  # Load data
  parsed_data = MatlabNodeParser(file_name, var_name)
  try:
    parsed_data.load_data()
  except IOError:
      print("Terminating...")
      exit()

  return parsed_data
# End query_file();

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

#############################
######  Atlas  Matrix  ######
#############################

# Makes empty matrix
num_regions = 78
atlas_matrix = [[0] * num_regions for n in range(num_regions)]

feature_id = 1 # 1 index because all nodes are 1 indexed
offset = 1
feature_to_matrix_hash = {}
for i in range(len(atlas_matrix)):
  for j in range(offset, len(atlas_matrix[i])):
      atlas_matrix[i][j] = feature_id
      feature_to_matrix_hash[feature_id] = (i, j)
      feature_id += 1
  offset += 1

#############################
######  Parse  Atlas   ######
#############################

# Generates list of x, y, z, name for each region
with open('aal.csv') as f:
    regions = [map(str, i.split(',')) for i in f]


#############################
#########   MAIN   ##########
#############################

# Picks file to run
data = query_file()
data.construct_node_container()

# Initialize AdjacencyMatrix and makes into csr_graph
container = NodeContainer(data._node_container)
connect = AdjacencyMatrix(container)
connect.fill_matrix();
user_query = query_outputs(connect.get_output_nodes())

# Creates all paths
connect.generate_all_output_paths()

# Create Edges
#edges = extract_unique_edges(connect.get_output_nodes(), connect._output_paths, user_query)
edges = connect.extract_unique_edges(user_query)
edges.sort(key=lambda tup: tup[0])


#############################
######   .Node File    ######
#############################
l_nodes = []
for n in connect.get_input_nodes():
  draw_nodes = feature_to_matrix_hash[n._node_number]
  if draw_nodes[0] not in l_nodes:
    l_nodes.append(draw_nodes[0])
  if draw_nodes[1] not in l_nodes:
    l_nodes.append(draw_nodes[1])


f = open("atlas.node", "w+")
for index in l_nodes:
  reg = regions[index]
  x = reg[0]
  y = reg[1]
  z = reg[2]
  name = reg[3]
  f.write(x + '\t' + y + '\t' + z + '\t' + str(1) + '\t' + str(2.2) + '\t' + name)
f.close()

#####################
### Graph Related ###
#####################
'''
The following needs to be moved into a class
'''
g = Graph()
g.add_vertices(len(connect.get_nodes()))
g.add_edges(edges)
g.vs["Layer"] = [l._layer for l in connect.get_nodes()]
g.vs["Node"] = [n._node_number for n in connect.get_nodes()]
g.es["Weight"] = 1
g.vs.select(_degree=0).delete() # Removes blank nodes
E = [e.tuple for e in g.es] # Get the edge list as list of tuples having as elements the end node 
                            # indecies
V = list(g.vs)
labels = []
# Creates hover labels for verticies
for v in V:
  # Hovering over inputs shows two regions from Connectivity Atlas Matrix
  if v["Layer"] is connect.get_max_layer():
    connect_pair = feature_to_matrix_hash[v["Node"]]
    reg_one = regions[connect_pair[0]][3].strip('\n')
    reg_two = regions[connect_pair[1]][3]
    title = reg_one + " <--> " + reg_two
    labels.append(title)
  # Hovering shows node number and layer
  else:
    title = "Layer: " + str(v["Layer"]) + " Node: " + str(v["Node"])
    labels.append(title)
layt = g.layout('circular')
L = len(layt)

node_color =[]
list_cofc_colors = ['#b634bb',
                    '#ed2939',
                    '#72c7e7',
                    '#024731',
                    '#7ab800',
                    '#f69240',
                    '#d95e00',
                    '#cd894e',
                    '#0083be',
                    '#dbceac',
                    '#a79e70',
                    '#beb9a6']
# Colors Inputs and Outputs uniquely. Other layers assigned from color list
for v in g.vs:
  if v["Layer"] is connect.get_max_layer():
    node_color.append('#660000')
  elif v["Layer"] is 1:
    node_color.append('#f0ab00')
  else:
    node_color.append(list_cofc_colors[v["Layer"] % (len(list_cofc_colors)-1)])

line_color = ['#FFFFFF' for v in g.vs]
edge_colors=['#d4daff','#84a9dd', '#5588c8', '#6d8acf']

Xn = [layt[k][0] for k in  range(L)]
Yn = [layt[k][1] for k in  range(L)]
Weights = map(int, g.es["Weight"])

Dist=[0, dist([1,0], 2*[np.sqrt(2)/2]), np.sqrt(2),
      dist([1,0],  [-np.sqrt(2)/2, np.sqrt(2)/2]), 2.0]
params = [1.2, 1.5, 1.8, 2.1]

lines=[]# the list of dicts defining   edge  Plotly attributes
edge_info=[]# the list of points on edges where  the information is placed

for j, e in enumerate(E):
  A=np.array(layt[e[0]])
  B=np.array(layt[e[1]])
  d=dist(A, B)
  K=get_idx_interv(d, Dist)
  b=[A, A/params[K], B/params[K], B]
  color=edge_colors[K]
  pts=BezierCv(b, nr=5)
  text=str(V[e[0]]['Layer'])+' to '+str(V[e[1]]['Node'])+' '+str(Weights[j])+' pts'
  mark=deCasteljau(b,0.9)
  edge_info.append(go.Scatter(x=[mark[0]], 
                              y=[mark[1]], 
                              mode='markers', 
                              marker=dict( size=0.5,  color=edge_colors), 
                              text=text, hoverinfo='text'))
  lines.append(go.Scatter(x=pts[:,0],
              y=pts[:,1],
              mode='lines',
              line=dict(color=color, shape='spline', width=Weights[j]),
              hoverinfo='none'))
trace2=go.Scatter(x=Xn,
                  y=Yn,
                  mode='markers',
                  name='',
                  marker=dict(symbol='circle', 
                              size=15, 
                              color=node_color, 
                              line=dict(color=line_color, width=0.5)),
                  text=labels,
                  hoverinfo='text',
                  )
axis=dict(showline=False,
    zeroline=False,
    showgrid=False,
    showticklabels=False,
    title='')

def make_annotation(anno_text, y_coord):
  return dict(showarrow=False,
              text=anno_text,
              xref='paper',
              yref='paper',
              x=0,
              y=y_coord,
              xanchor='left',
              yanchor='bottom',
              font=dict(size=12))
width = 1450
height = 1500
title = "Connectome Graph"

layout=go.Layout(title=title,
                font = dict(size=12),
                showlegend = False,
                autosize = False,
                width = width,
                height = height,
                xaxis = dict(axis),
                yaxis = dict(axis),
                margin = dict(l = 40,
                              r = 40,
                              b = 85,
                              t = 100),
                hovermode = 'closest')

data = lines + edge_info + [trace2]
fig = go.Figure(data=data, layout=layout)
#plotly.offline.init_notebook_mode()
plotly.offline.plot(fig, filename="Connectome Graph")

# SurfIce
subprocess.call(['/home/workstation6/sw/surfice/Surf_Ice/surfice','-S', 'BEGIN RESETDEFAULTS;MESHLOAD(\'BrainMesh_ICBM152.mz3\');NODELOAD(\'/data2/Connectome2018_project/BrianFiles/atlas.node\');SHADERXRAY(0.5, 0.1);END.']) 

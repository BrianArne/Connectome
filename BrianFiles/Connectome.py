import Globals #Mostly testing variables
import sys
import numpy as np
import plotly
import plotly.graph_objs as go

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
Returns a list of unique edges
'''
def extract_unique_edges(output_nodes, edges_dict, user_query):
  edges= []
  for q in user_query:
    for e in edges_dict[output_nodes[q-1]]: # This may have to be changed. Offset 1 if always ordered
      if e not in edges:
        edges.append(e)
  return edges
# End extract_unique_edges();

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
#########   MAIN   ##########
#############################

# Picks file to run
data = query_file()
data.construct_node_container()

# Initialize AdjacencyMatrix and makes into csr_graph
connect = AdjacencyMatrix(data._node_container)
connect.fill_matrix();
user_query = query_outputs(connect._output_nodes)

# Creates all paths
connect.generate_all_output_paths()

# Create Edges
edges = extract_unique_edges(connect._nodes, connect._output_paths, user_query)


#####################
### Graph Related ###
#####################
'''
The following needs to be moved into a class
'''
g = Graph()
g.add_vertices(len(connect._nodes))
g.add_edges(edges)
g.vs["Layer"] = [l._layer for l in connect._nodes]
g.vs["Node"] = [n._node_number for n in connect._nodes]
g.es["Weight"] =  1
E = [e.tuple for e in g.es] # Get the edge list as list of tuples haveing as elements the end node 
                            # indecies
V = list(g.vs)
labels = []
for v in V:
  title = "Layer: " + str(v["Layer"]) + " Node: " + str(v["Node"])
  labels.append(title)
layt = g.layout('circular')
L = len(layt)

node_color = ['#CCCCCC' for v in g.vs]
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

anno_text1 = "This is a test graph"
anno_text2 = "Do we get a graph?"
anno_text3 = "How long till we get a graph?"
width = 800
height = 850
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
                hovermode = 'closest',
                annotations = list([make_annotation(anno_text1, -0.07),
                                    make_annotation(anno_text2, -0.09),
                                    make_annotation(anno_text3, -0.11)])
                )
data = lines + edge_info + [trace2]
fig = go.Figure(data=data, layout=layout)
#plotly.offline.init_notebook_mode()
#plotly.offline.iplot(fig, filename="Connectome Graph")

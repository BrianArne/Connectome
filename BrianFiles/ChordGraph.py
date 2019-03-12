import numpy as np
import plotly
import plotly.graph_objs as go

from igraph import *

class ChordGraph:

  '''
  Constructs graph and necessary html tags
  '''
  def __init__(self, nodes, edges, max_layer, atlas):

    # Visual Concerns
    self._height = 1500
    self._width = 1450
    self._list_cofc_colors = ['#b634bb',
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
    self._title =  "Connectome"

    # Member vars need for final draw()
    # Will be initialized by following init functions
    self._edge_info = []
    self._graph = None
    self._hover_labels = []
    self._layout = None
    self._lines = []
    self._node_color = []
    self._trace2 = None
    self._vert_xy = []


    # Init functions
    self.init_graph(nodes, edges)
    self.create_hover_data(max_layer, atlas)
    self.color_verts(max_layer)
    self.define_edge()
    self.init_scatter_json()

  # End __init__();

  '''
  Class used in deCasteljau for exception throwing
  '''
  class InvalidInputError(Exception):
    pass
  # End Class InvalidInputError()

  '''
  Used to create curve from node to node
  '''
  def BezierCv(self, b, nr=5):
    t=np.linspace(0, 1, nr)
    return np.array([self.deCasteljau(b, t[k]) for k in range(nr)]) 
  # End BezierCv();

  '''
  Colors Verticies. Maroon always inputs. Gold always outputs.

  Must be called after self.init_graph() as it references self._graph
  '''
  def color_verts(self, max_layer):
    for v in self._graph.vs:
      if v["Layer"] is max_layer:
        self._node_color.append('#660000')
      elif v["Layer"] is 1:
        self._node_color.append('#f0ab00')
      else:
        self._node_color.append(self._list_cofc_colors[v["Layer"] % (len(self._list_cofc_colors)-1)])
  # End color_verticies();

  '''
  Generates hover data for verticies. Defines self._labels

  Must be called after self.init_graph() as it references self._graph
  '''
  def create_hover_data(self, max_layer, atlas):
    V = list(self._graph.vs)
    # Creates hover labels for verticies
    for v in V:
      # Hovering over inputs shows two regions from Connectivity Atlas Matrix
      if v["Layer"] is max_layer:
        connect_pair = atlas._feature_to_matrix_hash[v["Node"]]
        reg_one = atlas._regions_list[connect_pair[0]][3].strip('\n')
        reg_two = atlas._regions_list[connect_pair[1]][3]
        title = reg_one + " <--> " + reg_two
        self._hover_labels.append(title)
      # Hovering shows node number and layer
      else:
        title = "Layer: " + str(v["Layer"]) + " Node: " + str(v["Node"])
        self._hover_labels.append(title)
  # End create_hover_data();


  '''
  Used to create aesthetic curve from node to node
  '''
  def deCasteljau(self, b, t): 
    N=len(b) 
    if(N<2):
      raise InvalidInputError("The  control polygon must have at least two points")
    a=np.copy(b) #shallow copy of the list of control points 
    for r in range(1,N): 
      a[:N-r,:]=(1-t)*a[:N-r,:]+t*a[1:N-r+1,:]                             
    return a[0,:]
  # End deCasteljau();

  '''
  Creates data the defines edges and lines. Defines self._lines and self._edge_info
  '''
  def define_edge(self):
    Weights = map(int, self._graph.es["Weight"]) #local
    Dist=[0, self.dist([1,0], 2*[np.sqrt(2)/2]), np.sqrt(2),
          self.dist([1,0],  [-np.sqrt(2)/2, np.sqrt(2)/2]), 2.0] #local
    params = [1.2, 1.5, 1.8, 2.1] #local


    # Potential method (set up edge and line scatter)
    V = list(self._graph.vs)
    E = [e.tuple for e in self._graph.es]
    for j, e in enumerate(E):
      A=np.array(self._vert_xy[e[0]])
      B=np.array(self._vert_xy[e[1]])
      d=self.dist(A, B)
      K=self.get_idx_interv(d, Dist)
      b=[A, A/params[K], B/params[K], B]
      color='#000000'
      pts=self.BezierCv(b, nr=5)
      text=str(V[e[0]]['Layer'])+' to '+str(V[e[1]]['Node'])+' '+str(Weights[j])+' pts'
      mark=self.deCasteljau(b,0.9)

      # Edge info to scatter
      # Used in final draw
      self._edge_info.append(go.Scatter(x=[mark[0]], 
                                  y=[mark[1]], 
                                  mode='markers', 
                                  marker=dict( size=0.5,  color='#000000'), 
                                  text=text, hoverinfo='text'))
      # line info to scatter
      # used in final draw
      self._lines.append(go.Scatter(x=pts[:,0],
                  y=pts[:,1],
                  mode='lines',
                  line=dict(color=color, shape='spline', width=Weights[j]),
                  hoverinfo='none'))
  #End define_edge();

  '''
  @Returns the distance between 2 points A and B
  '''
  def dist (self,A,B):
    return np.linalg.norm(np.array(A)-np.array(B))
  # End dist();

  '''
  Displays graph in .html
  @arg jupyter True if using jupyter notebook for visual display
  '''
  def draw(self, jupyter=False):
    data = self._lines + self._edge_info + [self._trace2]
    fig = go.Figure(data=data, layout=self._layout)

    if (not jupyter):
      plotly.offline.plot(fig, filename="Connectome Graph")
    else:
      plotly.offline.init_notebook_mode()
  # End draw();

  '''
  Returns index of the interval the distance d belongs to
  '''
  def get_idx_interv(self, d, D):
    k=0
    while(d>D[k]): 
      k+=1
    return  k-1
  # End get_idx_interv();


  '''
  Initializes graph with verticies and edges
  '''
  def init_graph(self, nodes, edges):
    g = Graph()
    g.add_vertices(len(nodes))
    g.add_edges(edges)
    g.vs["Layer"] = [l._layer for l in nodes]
    g.vs["Node"] = [n._node_number for n in nodes]
    g.es["Weight"] = 1
    g.vs.select(_degree=0).delete() # Removes blank nodes
    self._vert_xy = g.layout('circular')
    self._graph = g
  # End init_graph();

  '''
  Defines JSON that determines graph output. Init _trace2 and _layout
  Responsible for most of the visual layout of the chord graph
  '''
  def init_scatter_json(self):
    n_verts = len(self._vert_xy)

    Xn = [self._vert_xy[k][0] for k in  range(n_verts)]
    Yn = [self._vert_xy[k][1] for k in  range(n_verts)]

    self._trace2=go.Scatter(x=Xn,
                      y=Yn,
                      mode='markers',
                      name='',
                      marker=dict(symbol='circle', 
                                  size=40, 
                                  color=self._node_color, #call color method here
                                  line=dict(color='#000000', width=0.5)),
                      text=self._hover_labels,
                      hoverinfo='text',
                      )

    axis=dict(showline=False,
        zeroline=False,
        showgrid=False,
        showticklabels=False,
        title='')

    self._layout=go.Layout(title=self._title,
                    font = dict(size=12),
                    showlegend = False,
                    autosize = False,
                    width = self._width,
                    height = self._height,
                    xaxis = dict(axis),
                    yaxis = dict(axis),
                    margin = dict(l = 40,
                                  r = 40,
                                  b = 85,
                                  t = 100),
                    hovermode = 'closest')
  # End init_scatter_json();
# End ChordGraph

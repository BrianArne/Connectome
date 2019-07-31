import numpy as np
import plotly
import plotly.graph_objs as go
from copy import deepcopy

from igraph import *

class ChordGraph:

  '''
  Constructs graph and necessary html tags
  '''
  def __init__(self, nodes, edges, max_layer, atlas):

    # Visual Concerns
    self._height = 850
    self._width = 800
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
    self._orig_copy = None


    # Init functions
    self.init_graph(nodes, edges)
    self.create_hover_data(max_layer, atlas)
    self.color_verts(max_layer)
    self.define_edge()
    self.init_scatter_json()
    self._orig_copy = deepcopy(self._graph)

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
  Removes edges from ipython Graph object self._graph.
  
  Uses lists of indexes from _graph.vs pertaining to output vertices and input vertices NOT currently selected (vertices that are not to be shown).
  '''
  
  def remove_edges(self, rm_outputs, rm_inputs):
    #assumes last vertex will always be at the max layer
    max_layer = self._graph.vs[-1:]['Layer'][0]
    
    translated_out_verts = self._graph.vs.select(Layer = 1, Node_in = rm_outputs)
    translated_in_verts = self._graph.vs.select(rm_inputs)
    
    self.change_edges_from_outs(translated_out_verts)
    self.change_edges_from_ins(translated_in_verts)
    
    self._graph.delete_edges(Weight = -1)
    self._graph.vs.select(_degree = 0).delete()
  # End remove_edges();
  
  
  '''
  Iterates through list of unselected output vertices, recursively traversing and marking edges to be deleted.
  
  Marks edges by changing their weight to -1, which may cause an issue if data being presented could possibly yield negative weights. Would defining as None work?
  '''
  def change_edges_from_outs(self, vertex_seq):
    for v in vertex_seq:
        inputs = self._graph.es.select(_target = v.index)
        prev_trav_ins = inputs.select(Weight = -1)
        if len(inputs) == len(prev_trav_ins): #if layer 1 or 'higher' exclusive input after previous traversals
            edges = self._graph.es.select(_source = v.index)
            if len(edges) == 0: #'highest' layer
                continue
            else: #needed?
                edges['Weight'] = -1
                next_vertex_seq = self._graph.vs.select(e.target for e in edges)
                self.change_edges_from_outs(next_vertex_seq)
        else:
            continue
    
  # End change_edges_from_outs();
  
  '''
  Iterates through list of unselected input vertices, recursively traversing and marking edges to be deleted.
  
  Marks edges by changing their weight to -1, which may cause an issue if data being presented could possibly yield negative weights.  Would defining as None work?
  '''
  def change_edges_from_ins(self, vertex_seq):
    for v in vertex_seq:
        outputs = self._graph.es.select(_source = v.index, Weight = 1)
        prev_trav_outs = outputs.select(Weight = -1)
        if len(outputs) == len(prev_trav_outs): #max layer or 'lower' exclusive output after previous traversals
            edges = self._graph.es.select(_target = v.index)
            if len(edges) == 0: #'lowest' layer (layer 1)
                continue
            else: #needed?
                edges['Weight'] = -1
                next_vertex_seq = self._graph.vs.select(e.source for e in edges)
                self.change_edges_from_ins(next_vertex_seq)
        else:
            continue
    
  # End change_edges_from_ins();
  
  '''
  Draws current state of _graph object (to be called after manipulating vs and es), then resets to _graph state defined on ChordGraph initiation.
  '''
  
  def subdraw(self, max_layer, atlas, jupyter):
    self._node_color = []
    self._vert_xy = self._graph.layout('circular')
    self.create_hover_data(max_layer, atlas)
    self.color_verts(max_layer)
    self.define_edge()
    self.init_scatter_json()
    
    self.draw(jupyter)
    
    self._graph = deepcopy(self._orig_copy)
  # End subdraw();
  
  
  
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
    if len(self._hover_labels) != 0:
        self._hover_labels = []
    V = list(self._graph.vs)
    # Creates hover labels for verticies
    for v in V:
      # Hovering over inputs shows two regions from Connectivity Atlas Matrix
      if v["Layer"] is max_layer:
        connect_pair = atlas._feature_to_matrix_hash[v["Node"]]
        reg_one = atlas._regions_list[connect_pair[0]][3].strip('\n')
        reg_two = atlas._regions_list[connect_pair[1]][3].strip('\n')
        
        title = reg_one + " <--> " + reg_two
        
        selected_lines = [(atlas._l_nodes.index(connect_pair[0]),atlas._l_nodes.index(connect_pair[1]))]
        
        #TODO: change_node_file_values and change_edge_file_values would work
        #more efficiently here if they were both called once at the end of this
        #"for v in V:" loop
        if(self._orig_copy == None): #if initializing class/not selecting a sub-graph...
            atlas.change_node_file_values(selected_lines, "c+1.0,s=2.2")
            atlas.change_edge_file_values(selected_lines, 0.1)
        
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
      #if r == 1:
        #print(len(a[:N-r,:]))
    return a[0,:]
  # End deCasteljau();

  '''
  Creates data the defines edges and lines. Defines self._lines and self._edge_info

  Must be called after self.init_graph() as it references self._graph
  '''
  def define_edge(self):
    if len(self._edge_info) != 0:
        self._edge_info = []
    if len(self._lines) != 0:
        self._lines = []
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
                  line=dict(color=color, shape='spline', width=3),
                  hoverinfo='none'))
  #End define_edge();

  '''
  @Returns the distance between 2 points A and B
  '''
  def dist (self, vert_a_xy, vert_b_xy):
    return np.linalg.norm(np.array(vert_a_xy)-np.array(vert_b_xy))
  # End dist();

  '''
  Displays graph in .html
  @arg jupyter True if using jupyter notebook for visual display
  '''
  def draw(self, jupyter=False):
    data = self._lines + self._edge_info + [self._trace2]

    '''No on click '''
    #fig = go.Figure(data=data, layout=self._layout)

    '''Inables on click events'''
    fig = go.FigureWidget(data=data, layout=self._layout)

    if (jupyter):
      plotly.offline.init_notebook_mode(connected=True)
      plotly.offline.iplot(fig, filename="ConnectomeGraph.html")
    else:
      plotly.offline.plot(fig, filename="ConnectomeGraph.html")
  # End draw();

  '''
  Returns index of the interval the distance d belongs to
  '''
  def get_idx_interv(self, vert_dist, dist_list):
    k=0
    while(vert_dist>dist_list[k]): 
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
    g.vs.select(_degree=0, Layer_ne = 1).delete() #removes blank non-output nodes
    self._vert_xy = g.layout('circular')
    self._graph = g
  # End init_graph();

  '''
  Defines JSON that determines graph output. Init _trace2 and _layout
  Responsible for most of the visual layout of the chord graph
  
  Must be called after self.init_graph() as it references self._vert_xy
  '''
  def init_scatter_json(self):
    if self._trace2 != None:
        self._trace2 = None
    n_verts = len(self._vert_xy)

    Xn = [self._vert_xy[k][0] for k in  range(n_verts)]
    Yn = [self._vert_xy[k][1] for k in  range(n_verts)]

    self._trace2=go.Scatter(x=Xn,
                      y=Yn,
                      mode='markers',
                      name='',
                      marker=dict(symbol='circle', 
                                  size=20, 
                                  color=self._node_color,
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

  '''
  Changes the title of the graph from "Connectome" to the provided string
  Calls init_scatter_json to reset go.Layout
  '''
  def set_title(self, string):
    self._title = string
    self.init_scatter_json()
  # End set_title();

# End ChordGraph

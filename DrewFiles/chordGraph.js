/* NOTED ON JAN 18, 2019, v5.7.0
  d3.chord(matrix) is the type of graph we want to make for interpretation
  of layer relationships.  

  "The return value of chord(matrix) is an array 
  of chords, where each chord represents the combined bidirectional flow 
  between two nodes i and j (where i may be equal to j) and is an object with
  the following properties:

    source - the source subgroup
    target - the target subgroup

  Each source and target subgroup is also an object with the following properties:

    startAngle - the start angle in radians
    endAngle - the end angle in radians
    value - the flow value matrix[i][j]
    index - the node index i
    subindex - the node index j

  The chords are typically passed to d3.ribbon to display the network relationships.
  The returned array includes only chord objects for which the value matrix[i][j] or
  matrix[j][i] is non-zero. Furthermore, the returned array only contains unique 
  chords: a given chord ij represents the bidirectional flow from i to j and from j 
  to i, and does not contain a duplicate chord ji; i and j are chosen such that the 
  chord’s source always represents the larger of matrix[i][j] and matrix[j][i]. In 
  other words, chord.source.index equals chord.target.subindex, chord.source.subindex 
  equals chord.target.index, chord.source.value is greater than or equal to 
  chord.target.value, and chord.source.value is always greater than zero.

  The chords array also defines a secondary array of length n, chords.groups, where 
  each group represents the combined outflow for node i, corresponding to the elements 
  matrix[i][0 … n - 1], and is an object with the following properties:

    startAngle - the start angle in radians
    endAngle - the end angle in radians
    value - the total outgoing flow value for node i
    index - the node index i
    
  The groups are typically passed to d3.arc to produce a donut chart around the 
  circumference of the chord layout."


  subfunctions of d3.chord(matrix): padAngle([angle]),
  sortGroups([compare]), sortSubGroups([compare]), sortChords([compare]).
  d3.ribbon(args...) is what is used to visually graph the connections in the
  example being used as target (https://github.com/d3/d3-chord).
  subfunctions of d3.ribbon(args...): source([source]), target([target]),
  radius([radius]), startAngle([angle]), endAngle([angle]), context([context]).


  ISSUES: 1.  chord source is defined between indexes (i, j), (j, i) by which contains the 
  higher value (this is meant to indicate flow), so defining color based upon chord.source or 
  chord.target may lead to error unless lower layer value is always greater than or equal to
  higher layer value, or vice versa.  since the flow in our data is not bidirectional, this 
  should not occur, as you could easily just set both sides to equal value, or target to less.

  2.  this chord graph is coded to interpret an n x n matrix such that the matrix represents n 
  unique nodes, each of which can connect with a given value to each other node and itself in ONE
  bidirectional ribbon.  trying to have a chord represent a layer of reduction, of which there
  is much less than indexes of source data, is not possible with chord's source code.  nor
  is it possible to illustrate two connections from a single layer, whether from a singular
  node or from several, to another single layer.

  FIX:  modify the source code to meet our needs.  
  object needs: to be able to graphically indicate nodes on a layer (object itself)  with no 
  connections, nodes with connections to n nodes within m layers.

  adding these capabilities won't be the only issue, as then we will need to change how to
  express this data as well as how the modified class will interpret it.
*/
const ZERO = 0;
var svg = d3.select("svg"),
    g = svg.append("g");

width = +svg.attr("width");
height = Math.min(640, width);

 // const svg = d3.select(DOM.svg(width, height))
svg.attr("viewBox", [-width / 2, -height / 2, width, height]) //sets origin for object creation
    .attr("font-size", 10)
    .attr("font-family", "sans-serif");

/*sample output
  data = [-9999, 0, 0, 1, 1, 2, 2] //walk backwards from last index.  
*/

/*data = [
  []
  []
  []
  []
  []
  []
];
*/
/*data = [ //data must be n x n matrix?
  [11975,  5871, 8916, 2868],
  [ 1951, 10048, 2060, 6171],
  [ 8010, 16145, 8090, 8045],
  [ 1013,   990,  940, 6907]
  ];*/

/*data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], //<----
    [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
];*/

data = [
    [1, 1, 0, 0], //each row makes up an arc (--> layer) of the graph
    [1, 1, 0, 0], //arc(i,j), 'i' being the array, j being index in array. 
    [0, 0, 1, 0], //the value contained at (0,1) = 1 is used as the
    [0, 0, 0, 1]  //width of the ribbon at its 0th layer connection,
];              //then will visually extend to the arc representing
                  //the jth array, arc 1, and scale its width to the value
                 //found at (1,0) = 0.



outerRadius = Math.min(width, height) * 0.5 - 30;
innerRadius = outerRadius - 20;

formatValue = d3.formatPrefix(",.0", 1e3);

chord = d3.chord() //connection objects
    .padAngle(0.05)
    .sortSubgroups(d3.descending); //sort descending by j index value

arc = d3.arc() //outer rings
    .innerRadius(innerRadius)
    .outerRadius(outerRadius);

ribbon = d3.ribbon() //connection visualization
    .radius(innerRadius); 

color = d3.scaleOrdinal() //color specifications; need to finish function below that could create an array of size updateData.length with distributed values
    .domain(d3.range(32))
    .range(["#000000", "#FFDD89", "#957244", "#F26223","#AAB011","#5ADDCC","#2B44AA","#E022C0","#FA8055", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000"]);

/*function makeColors(updateData) {
    num = updateData.length;
    color = d3.scaleOrdinal()
	.domain(d3.range(num))
	.range(
}*/

function groupTicks(d, step) {
    const k = (d.endAngle - d.startAngle) / d.value;
    return d3.range(0, d.value, step).map(value => {
	return {value: value, angle: value * k + d.startAngle};
    });
}

function updateGraph(updateData) {
    var chords = chord(updateData);
    g.remove();
    g = svg.append("g");

    group = g.selectAll("g")
	.data(chords.groups)
	.enter().append("g");
    
    group.append("path") //outside arcs of graph, runs for and inserts inside every 'g' within group
	.attr("fill", d => color(d.index))
	.attr("stroke", d => d3.rgb(color(d.index)).darker())
	.attr("d", arc);

    var groupTick = group.append("g") //unit values, runs for and inserts inside every 'g' within group
	.selectAll("g")
	.data(d => groupTicks(d, 1e3))
	.enter().append("g")
	.attr("transform", d => `rotate(${d.angle * 180 / Math.PI - 90}) translate(${outerRadius},0)`);

    groupTick.append("line") //tick marks for each unit value on arcs
      .attr("stroke", "#000")
      .attr("x2", 6);

    groupTick
	.filter(d => d.value % 5e3 === 0) //filters out tick marks that aren't multiples of 5k
	.append("text")
	.attr("x", 8) //sets beginning radius of value being written
	.attr("dy", ".35em") //centers values to tick marks
	.attr("transform", d => d.angle > Math.PI ? "rotate(180) translate(-16)" : null) //text rotation
	.attr("text-anchor", d => d.angle > Math.PI ? "end" : null) //text orientation
	.text(d => formatValue(d.value));

    g.append("g") //creating pathway ribbons 
	.attr("fill-opacity", 0.67)
	.selectAll("path")
	.data(chords)
	.enter().append("path")
	.attr("d", ribbon)
	.attr("fill", d => color(d.source.index)) //EDIT changed 'target' to 'source'
	.attr("stroke", d => d3.rgb(color(d.source.index)).darker()); //EDIT changed 'target' to 'source'
}

d3.selectAll("button")
    .on("click", function(){
	//chords = chord(data2);
	//updateGraph(data2);
    });

updateGraph(data);

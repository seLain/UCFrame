// set up SVG for D3
var width  = 400,
    height = 300,
    colors = d3.scale.category10();

var svg, nodes, lastNodeId, links, force, drag_line, path, circle;
var selected_node, selected_link, mousedown_link, mousedown_node, mouseup_node;

function ams_colors(ams){

  var ACTOR_COLOR = '#FF0099';
  var MESSAGE_COLOR = '#00FF33';
  var SYSTEM_COLOR = '#00FFFF';
  var DEFAULT_COLOR = '#505050 ';

  if (ams == 'Actor'){
    return ACTOR_COLOR;
  } else if (ams == 'Message'){
    return MESSAGE_COLOR;
  } else if (ams == 'System'){
    return SYSTEM_COLOR;
  } else {
    return DEFAULT_COLOR;
  }

}

function reset_all(){

    d3.select('svg').remove();
    
    svg = d3.select('#chart')
            .append('svg')
            .attr('width', width)
            .attr('height', height);
    
    nodes = [];
    lastNodeId = 0;
    links = [];
    
    force = d3.layout.force()
              .nodes(nodes)
              .links(links)
              .size([width, height])
              .linkDistance(150)
              .charge(-500)
              .on('tick', tick)
    
    svg.append('svg:defs').append('svg:marker')
                          .attr('id', 'end-arrow')
                          .attr('viewBox', '0 -5 10 10')
                          .attr('refX', 6)
                          .attr('markerWidth', 3)
                          .attr('markerHeight', 3)
                          .attr('orient', 'auto')
                          .append('svg:path')
                          .attr('d', 'M0,-5L10,0L0,5')
                          .attr('fill', '#000');

    svg.append('svg:defs').append('svg:marker')
                          .attr('id', 'start-arrow')
                          .attr('viewBox', '0 -5 10 10')
                          .attr('refX', 4)
                          .attr('markerWidth', 3)
                          .attr('markerHeight', 3)
                          .attr('orient', 'auto')
                          .append('svg:path')
                          .attr('d', 'M10,-5L0,0L10,5')
                          .attr('fill', '#000');
    
    drag_line = svg.append('svg:path')
                   .attr('class', 'link dragline hidden')
                   .attr('d', 'M0,0L0,0');
    
    path = svg.append('svg:g').selectAll('path');
    circle = svg.append('svg:g').selectAll('g');
    
    selected_node = null,
    selected_link = null,
    mousedown_link = null,
    mousedown_node = null,
    mouseup_node = null;
    
}

function resetMouseVars() {
  mousedown_node = null;
  mouseup_node = null;
  mousedown_link = null;
}

// update force layout (called automatically each iteration)
function tick() {
  // draw directed edges with proper padding from node centers
  path.attr('d', function(d) {
    var deltaX = d.target.x - d.source.x,
        deltaY = d.target.y - d.source.y,
        dist = Math.sqrt(deltaX * deltaX + deltaY * deltaY),
        normX = deltaX / dist,
        normY = deltaY / dist,
        sourcePadding = d.left ? 17 : 12,
        targetPadding = d.right ? 17 : 12,
        sourceX = d.source.x + (sourcePadding * normX),
        sourceY = d.source.y + (sourcePadding * normY),
        targetX = d.target.x - (targetPadding * normX),
        targetY = d.target.y - (targetPadding * normY);
    return 'M' + sourceX + ',' + sourceY + 'L' + targetX + ',' + targetY;
  });

  circle.attr('transform', function(d) {
    return 'translate(' + d.x + ',' + d.y + ')';
  });
}

// update graph (called when needed)
function restart() {
    
  //console.log('[restart] nodes:', nodes);
  // path (link) group
  path = path.data(links);

  // update existing links
  path.classed('selected', function(d) { return d === selected_link; })
    .style('marker-start', function(d) { return d.left ? 'url(#start-arrow)' : ''; })
    .style('marker-end', function(d) { return d.right ? 'url(#end-arrow)' : ''; });


  // add new links
  path.enter().append('svg:path')
    .attr('class', 'link')
    .classed('selected', function(d) { return d === selected_link; })
    .style('marker-start', function(d) { return d.left ? 'url(#start-arrow)' : ''; })
    .style('marker-end', function(d) { return d.right ? 'url(#end-arrow)' : ''; })
    .on('mousedown', function(d) {
      if(d3.event.ctrlKey) return;

      // select link
      mousedown_link = d;
      if(mousedown_link === selected_link) selected_link = null;
      else selected_link = mousedown_link;
      selected_node = null;
      restart();
    });

  // remove old links
  path.exit().remove();


  // circle (node) group
  // NB: the function arg is crucial here! nodes are known by id, not by index!
  circle = circle.data(nodes, function(d) { return d.id; });

  // update existing nodes (reflexive & selected visual states)
  circle.selectAll('circle')
    .style('fill', function(d) { return (d === selected_node) ? d3.rgb(ams_colors(d.type)).brighter().toString() : ams_colors(d.type); })
    .classed('reflexive', function(d) { return d.reflexive; });

  // add new nodes
  var g = circle.enter().append('svg:g');

  g.append('svg:circle')
    .attr('class', 'node')
    .attr('r', 12)
    .style('fill', function(d) { return (d === selected_node) ? d3.rgb(ams_colors(d.type)).brighter().toString() : ams_colors(d.type); })
    .style('stroke', function(d) { return d3.rgb(colors(d.id)).darker().toString(); })
    .classed('reflexive', function(d) { return d.reflexive; })
    .on('mouseover', function(d) {
      if(!mousedown_node || d === mousedown_node) return;
      // enlarge target node
      d3.select(this).attr('transform', 'scale(1.1)');
    })
    .on('mouseout', function(d) {
      if(!mousedown_node || d === mousedown_node) return;
      // unenlarge target node
      d3.select(this).attr('transform', '');
    })
    .on('mousedown', function(d) {
      if(d3.event.ctrlKey) return;

      // select node
      mousedown_node = d;
      if(mousedown_node === selected_node) selected_node = null;
      else selected_node = mousedown_node;
      selected_link = null;

      // reposition drag line
      drag_line
        .style('marker-end', 'url(#end-arrow)')
        .classed('hidden', false)
        .attr('d', 'M' + mousedown_node.x + ',' + mousedown_node.y + 'L' + mousedown_node.x + ',' + mousedown_node.y);

      restart();
    })
    .on('mouseup', function(d) {
      if(!mousedown_node) return;

      // needed by FF
      drag_line
        .classed('hidden', true)
        .style('marker-end', '');

      // check for drag-to-self
      mouseup_node = d;
      if(mouseup_node === mousedown_node) { resetMouseVars(); return; }

      // unenlarge target node
      d3.select(this).attr('transform', '');

      // add link to graph (update if exists)
      // NB: links are strictly source < target; arrows separately specified by booleans
      var source, target, direction;
      if(mousedown_node.id < mouseup_node.id) {
        source = mousedown_node;
        target = mouseup_node;
        direction = 'right';
      } else {
        source = mouseup_node;
        target = mousedown_node;
        direction = 'left';
      }

      var link;
      link = links.filter(function(l) {
        return (l.source === source && l.target === target);
      })[0];

      if(link) {
        link[direction] = true;
      } else {
        link = {source: source, target: target, left: false, right: false};
        link[direction] = true;
        links.push(link);
      }

      // select new link
      selected_link = link;
      selected_node = null;
      restart();
    });

  // show node IDs
  g.append('svg:text')
      .attr('x', 0)
      .attr('y', 4)
      .attr('class', 'id')
      .text(function(d) { return d.id; });

  // [seLain] show node text along the circle
  g.append('svg:text')
      .attr('x', 40)
      .attr('y', 4)
      .attr('class', 'id')
      .text(function(d) { return d.text; });

  // remove old nodes
  circle.exit().remove();

  // set the graph in motion
  force.start();
}

function mousedown() {
  // prevent I-bar on drag
  //d3.event.preventDefault();
  
  // because :active only works in WebKit?
  svg.classed('active', true);

  if(d3.event.ctrlKey || mousedown_node || mousedown_link) return;

  // insert new node at point
  var point = d3.mouse(this),
      node = {id: ++lastNodeId, reflexive: false};
  node.x = point[0];
  node.y = point[1];
  nodes.push(node);

  restart();
}

function mousemove() {
  if(!mousedown_node) return;

  // update drag line
  drag_line.attr('d', 'M' + mousedown_node.x + ',' + mousedown_node.y + 'L' + d3.mouse(this)[0] + ',' + d3.mouse(this)[1]);

  restart();
}

function mouseup() {
  if(mousedown_node) {
    // hide drag line
    drag_line
      .classed('hidden', true)
      .style('marker-end', '');
  }

  // because :active only works in WebKit?
  svg.classed('active', false);

  // clear mouse event vars
  resetMouseVars();
}

function spliceLinksForNode(node) {
  var toSplice = links.filter(function(l) {
    return (l.source === node || l.target === node);
  });
  toSplice.map(function(l) {
    links.splice(links.indexOf(l), 1);
  });
}

// only respond once per keydown
var lastKeyDown = -1;

function keydown() {
  d3.event.preventDefault();

  if(lastKeyDown !== -1) return;
  lastKeyDown = d3.event.keyCode;

  // ctrl
  if(d3.event.keyCode === 17) {
    circle.call(force.drag);
    svg.classed('ctrl', true);
  }

  if(!selected_node && !selected_link) return;
  switch(d3.event.keyCode) {
    case 8: // backspace
    case 46: // delete
      if(selected_node) {
        nodes.splice(nodes.indexOf(selected_node), 1);
        spliceLinksForNode(selected_node);
      } else if(selected_link) {
        links.splice(links.indexOf(selected_link), 1);
      }
      selected_link = null;
      selected_node = null;
      restart();
      break;
    case 66: // B
      if(selected_link) {
        // set link direction to both left and right
        selected_link.left = true;
        selected_link.right = true;
      }
      restart();
      break;
    case 76: // L
      if(selected_link) {
        // set link direction to left only
        selected_link.left = true;
        selected_link.right = false;
      }
      restart();
      break;
    case 82: // R
      if(selected_node) {
        // toggle node reflexivity
        selected_node.reflexive = !selected_node.reflexive;
      } else if(selected_link) {
        // set link direction to right only
        selected_link.left = false;
        selected_link.right = true;
      }
      restart();
      break;
  }
}

/*
function keyup() {
  lastKeyDown = -1;

  // ctrl
  if(d3.event.keyCode === 17) {
    circle
      .on('mousedown.drag', null)
      .on('touchstart.drag', null);
    svg.classed('ctrl', false);
  }
}*/

function event_keyup(){
  lastKeyDown = -1;  
    
  // reset nodes
  //nodes = [];
  //lastNodeId = 0;
  //links = [];
  reset_all();
    
  // ctrl
  var pre1 = document.getElementById('PreCondition-Condition-input-1').value;
  var pre2 = document.getElementById('PreCondition-Condition-input-2').value;
  var pre3 = document.getElementById('PreCondition-Condition-input-3').value;
  
  update_by_string(pre1);
  update_by_string(pre2);
  update_by_string(pre3);
    
  // reset force
  force = d3.layout.force()
    .nodes(nodes)
    .links(links)
    .size([width, height])
    .linkDistance(150)
    .charge(-500)
    .on('tick', tick)

  //console.log('nodes:'+nodes);
  
  restart();
}

function update_by_string(statement){
  //console.log('statement:'+statement) 
  if(statement.length < 3){
      return;
  }
  
  var pre1_array = statement.split(' ');
  var last_type = '';
  var last_content = '';
  for(var term_index in pre1_array){
      var term = pre1_array[term_index];
      if(term.length < 5){ // avoid processing too short term
          continue;
      }
      var node = {}
      tag = term.substring(0, 1);
      content = term.substring(1, term.length);
      if(tag == '@'){  // actor
          checked = no_duplicate_node(content, 'Actor')
          if(checked['no_duplicate']){
              node = {id: ++lastNodeId, reflexive: false, text: content, type: 'Actor'};
              nodes.push(node);
          }else{  // duplicated, make the node = exisiting node
              node = checked['node'];
          };
      }else if(tag == '$'){  // actor
          checked = no_duplicate_node(content, 'Message')
          if(checked['no_duplicate']){
              node = {id: ++lastNodeId, reflexive: false, text: content, type: 'Message'};
              nodes.push(node);
          }else{ // duplicated, make the node = exisiting node
              node = checked['node'];
          };
      }else if(tag == '*'){  // actor
          checked = no_duplicate_node(content, 'System')
          if(checked['no_duplicate']){
              node = {id: ++lastNodeId, reflexive: false, text: content, type: 'System'};
              nodes.push(node);
          }else{ // duplicated, make the node = exisiting node
              node = checked['node'];
          };;
      }else{  // ignore terms not starts with @, $, *
          continue;
      };
      
      // build the link
      if(last_type != '' || last_content != ''){
        // find the last node id
        var previous_node_id = -1;
        var previous_node = {};
        for(var i in nodes){
            if(nodes[i]['text'] == last_content && nodes[i]['type'] == last_type){
              previous_node_id = nodes[i]['id'];
              previous_node = nodes[i];
              break;
            };
        };
        if(previous_node_id != -1){
            var link = {source: previous_node, target: node, left: false, right: true};
            //console.log(link);
            links.push(link);
        };
      }
      
      // recorded for later usage
      last_type = node.type;
      last_content = node.text;
  };
  
}

function no_duplicate_node(node_content, node_type){

  for(var index in nodes){
      var node = nodes[index];
      //console.log('text:'+node['text']);
      if(node['text'] == node_content && node['type'] == node_type){
          //console.log('caught false');
          return {no_duplicate: false, node: node};
      };
  };
  return {no_duplicate: true};
}


// app starts here
reset_all();
//svg.on('mousedown', mousedown)
//  .on('mousemove', mousemove)
//  .on('mouseup', mouseup);
d3.select(window)
//  .on('keydown', keydown)
  .on('keyup', event_keyup);
restart();
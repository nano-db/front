var Cube = function(name, dim, count, gran, mapping) {
  this.name = name;
  this.dim = dim;
  this.count= count;
  this.gran = gran;
  this.mapping = mapping;
  this.world = null;
};




var Serializer = function(){};
Serializer.HEADER_SIZE = 5;


Serializer.prototype.load = function(filepath, callback) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open('GET', filepath, true);

  var current = this;

  xmlHttp.onreadystatechange = function () {
    if(xmlHttp.readyState == 4) {
      if(xmlHttp.status == 200) {

        var cube = current._loadCube(xmlHttp.responseText);
        cube == null?
          callback(new Error('Loading of NanoCube failed!')):
          callback(null, cube);

      } else {
        callback(new Error('Request failed!'));
      }
    }
  }
  xmlHttp.send();
};


Serializer.prototype._loadCube = function(serialized) {
  var cube;

  var lines = serialized.split('\n');

  var dimValues = lines[3].split(',');
  var dims = [];
  for (var i = 0; i < dimValues.length; i++) {
    dims.push(dimValues[i]);
  }

  var mapping = JSON.parse(lines[4]);

  cube = new Cube(lines[0], lines[1], lines[2], dims, mapping);

  var nodes = {};
  var lastNode = null;

  for (var i = Serializer.HEADER_SIZE; i < lines.length; i++) {
    var line = lines[i];
    if (line.indexOf('t') > -1) {
      var table = _loadTimeSerieTable(line);
      nodes[table.id] = table;
    } else {
      var node = _loadNodes(line, nodes);
      nodes[node.id] = node;
      lastNode = node;
    }
  }
  cube.world = lastNode;

  return cube;
};


var TimeSerieTable = function(id, start, table) {
  this.id = id;
  this.start = start;
  this.table = table;
};

var Node = function(id) {
  this.id = id;
  this.pch = null;
  this.sch = null;
  this.spo = null;
  this.sco = null;
};


var _loadTimeSerieTable = function(line) {
  var splits = line.split('|');
  var id = splits[1];
  // Getting the date out of the splitted string (remove space and last 't' char)
  var time = splits[2];

  // For each value (csv) add it to the array
  var table = [];
  var values = splits[3].split(',');
  var count = 0;
  for (var i = 0; i < values.length; i++) {
    var value = values[i];
    if(value.indexOf(':') > -1) {
      var splits = value.split(':');

      count += parseInt(splits[0]);
      for(var j = 0; j < splits[1] ; j++) {
        table.push(count);
      }
    } else {
      count += parseInt(value);
      table.push(count);
    }
  }

  return new TimeSerieTable(id, time, table);
};


var _loadNodes = function(line, nodes) {

  var splits = line.split('|');
  var id = splits[1];
  var node;
  if (id != '') {
    node = new Node(id);
    if(splits[2] != '') {
      node.pch = JSON.parse(splits[2]);
      for(var key in node.pch) {
        var value = node.pch[key];
        node.pch[key] = nodes[value];
      }
    }
    if(splits[3] != '') {
      node.sch = JSON.parse(splits[3]);
      for(var key in node.sch) {
        var value = node.sch[key];
        node.sch[key] = nodes[value];
      }
    }

    if (splits[4] != '') {
      node.pco = nodes[splits[4]];
    } else {
      node.sco = nodes[splits[5]];
    }

    return node;

  } else {
    return null;
  }
};

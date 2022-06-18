var canvas = document.getElementById('globe');
var globe = planetaryjs.planet();

// Load autorotate plugin
globe.loadPlugin(autorotate(10));
// The `earth` plugin draws the oceans and the land
globe.loadPlugin(planetaryjs.plugins.earth({
topojson: { file:   '/world-110m-withlakes.json' },
//oceans:   { fill:   '#00004d' },
oceans:   { fill:   '#000000' },
//land:     { fill:   '#339966' },
land:     { fill:   '#2c5e21' },
//borders:  { stroke: '#008000' }
borders:  { stroke: '#339966' }
}));
// Load lakes plugin
globe.loadPlugin(lakes({
  //fill: '#000033'
  fill: '#1b1c1a'
}));

// load the pings plugin
globe.loadPlugin(planetaryjs.plugins.pings());
// load the zoom plugin
globe.loadPlugin(planetaryjs.plugins.zoom({
scaleExtent: [100, 300]
}));
// load the drag plugin
globe.loadPlugin(planetaryjs.plugins.drag({
// Dragging the globe should pause the
// automatic rotation until releasing the mouse.
onDragStart: function() {
  this.plugins.autorotate.pause();
},
onDragEnd: function() {
  this.plugins.autorotate.resume();
}
}));
// Set up the globe's initial scale, offset, and rotation.
globe.projection.scale(canvas.width/2).translate([canvas.width/2, canvas.height/2]).rotate([0, -10, 0]);

// Draw the globe
globe.draw(canvas);

// This plugin will automatically rotate the globe around its vertical
// axis a configured number of degrees every second.
function autorotate(degPerSec) {
  // Planetary.js plugins are functions that take a `planet` instance
  // as an argument...
  return function(planet) {
    var lastTick = null;
    var paused = false;
    planet.plugins.autorotate = {
    pause:  function() { paused = true;  },
    resume: function() { paused = false; }
    };
    // ...and configure hooks into certain pieces of its lifecycle.
    planet.onDraw(function() {
    if (paused || !lastTick) {
      lastTick = new Date();
    } else {
      var now = new Date();
      var delta = now - lastTick;
      // This plugin uses the built-in projection (provided by D3)
      // to rotate the globe each time we draw it.
      var rotation = planet.projection.rotate();
      rotation[0] += degPerSec * delta / 1000;
      if (rotation[0] >= 180) rotation[0] -= 360;
      planet.projection.rotate(rotation);
      lastTick = now;
    }
    });
  };
};

// This plugin takes lake data from the special
// TopoJSON we're loading and draws them on the map.
function lakes(options) {
options = options || {};
var lakes = null;

return function(planet) {
  planet.onInit(function() {
  // We can access the data loaded from the TopoJSON plugin
  // on its namespace on `planet.plugins`. We're loading a custom
  // TopoJSON file with an object called "ne_110m_lakes".
  var world = planet.plugins.topojson.world;
  lakes = topojson.feature(world, world.objects.ne_110m_lakes);
  });

  planet.onDraw(function() {
  planet.withSavedContext(function(context) {
    context.beginPath();
    planet.path.context(context)(lakes);
    context.fillStyle = options.fill || 'black';
    context.fill();
  });
  });
};
};

// this function is called everytime new pings need to be added
// and old ones need to be removed
function updateGlobe(ping_locations){
    function pingInterval(){
      // Iterate through all latitude longitude entries and create pings for each
        for(var i = 0; i < ping_locations.length; i++){
            for(var j = 0; j < ping_locations[i].length; j++){
              if(j == 0){
                var latitude = ping_locations[i][j];
              }else{
                var longitude = ping_locations[i][j];
                globe.plugins.pings.add(longitude, latitude, {color: "orange", ttl: 2000, angle: 4});
              }}};

    }

    // If the pingInterval function is currently being called every 2 seconds
    // then stop that, before calling the function again every 2 seconds with
    // new ping locations
    try{
      clearInterval(myInterval)
    }catch(error){
      //console.error(error);
    }

    // call the pingInterval function every 2 seconds
    myInterval = setInterval(pingInterval, 2000)

}

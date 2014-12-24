function initialize() {
    var myLatlng = new google.maps.LatLng(45.7597, 4.8422);
    var mapOptions = {
        zoom: 12,
        minZoom: 10,
        //draggable: false,
        center: myLatlng
    }
    var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

    //loadPictures(map, 'data.csv');
}

google.maps.event.addDomListener(window, 'load', initialize);



var serial = new Serializer();
serial.load('api/cubes/Crime/serialize', function(err, cube) {
  if(err) {
    console.error(err.message);
  } else {
    console.log("Cube was loaded correctly: let work on the viz :)");
    console.log(cube);
  }
});

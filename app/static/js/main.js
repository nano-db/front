var serial = new Serializer();
serial.load('api/cubes/Crime/serialize', function(err, cube) {
  if(err) {
    alert(err.message);
  } else {
    alert(cube);
  }

});

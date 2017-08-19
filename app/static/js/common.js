var map = (function() {
  var init = function(latLon, zoom) {
    var map = L.map('map').setView(latLon, zoom);

    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
  };
  return {
    init: init
  };
})();

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

var form = (function() {

  var setLatLon = function(lat, lon) {
    document.getElementById('lat').value = lat;
    document.getElementById('lon').value = lon;
  };

  var submit = function() {
    var data = {};

    $('#button-form').serializeArray().forEach(function(ele){
      data[ele.name] = ele.value;
    });

    $.ajax({
      type: 'POST',
      url: '/api/v1/sensors',
      data: JSON.stringify(data),
      contentType: "application/json; charset=utf-8",
      dataType: "json"
    });
  }

  var init = function() {
    $('#button-form').submit(function(e) {
      e.preventDefault()
      submit()
    })
  }

  return {
    setLatLon: setLatLon,
    init: init
  };
})();


$(document).ready(function() {
  map.init([51.954952, 7.619977], 13);
  form.init();
});

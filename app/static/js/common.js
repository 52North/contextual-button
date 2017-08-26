var map = (function () {
  var _map

  var _markers = L.layerGroup()

  var init = function (latLon, zoom) {
    _map = L.map('map').setView(latLon, zoom)

    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(_map)

    _markers.addTo(_map)
  }

  var onClick = function (callback) {
    _map.on('click', callback)
  }

  var showPopUp = function (popup) {
    popup.openOn(_map)
  }

  var addMarker = function (latlon, clearLayers = false) {
    if (clearLayers) {
      _markers.clearLayers()
    }
    L.marker(latlon).addTo(_markers)
  }

  var add = function (layer) {
    layer.addTo(_map)
  }

  return {
    init: init,
    onClick: onClick,
    showPopUp: showPopUp,
    addMarker: addMarker,
    add: add
  }
})()

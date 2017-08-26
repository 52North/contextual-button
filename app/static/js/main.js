var api = (function () {
  var getFOIs = function (callback) {
    return $.get('/api/v1/foi', callback)
  }

  return {
    getFOIs: getFOIs
  }
})()

$(document).ready(function () {
  map.init([51.954952, 7.619977], 13)

  map.onClick(function (e) {
    var popup = L.popup()
      .setLatLng(e.latlng)
      .setContent('<a href="/add_button?lat=' + e.latlng.lat + '&lon=' + e.latlng.lng + '">Add a new Button here</a>')
    map.showPopUp(popup)
  })

  api.getFOIs(function (data) {
    map.add(L.geoJSON(data, {
      onEachFeature: function (feature, layer) {
        layer.bindPopup(function () {
          var popup = document.createElement('div')
          $.get('/foi_popup',
          {'foi': feature.id},
          function (data) {
            popup.innerHTML = data
          })
          return popup
        })
      }
    }))
  })
})

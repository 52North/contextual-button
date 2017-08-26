var form = (function () {
  var setLatLon = function (lat, lon) {
    $('#lat').val(lat)
    $('#lon').val(lon)
  }

  var getLatLon = function () {
    return [$('#lat').val(), $('#lon').val()]
  }

  var submit = function () {
    var data = {}

    $('#button-form').serializeArray().forEach(function (ele) {
      data[ele.name] = ele.value
    })

    $.ajax({
      type: 'POST',
      url: '/api/v1/sensors',
      data: JSON.stringify(data),
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      success: displaySuccess,
      failure: displayError
    })
  }

  var displaySuccess = function(data) {
    $('#success-message').show()
    $('#success-message').text(JSON.stringify(data))
  }

  var displayError = function(data) {
    console.log(data)
    $('#error-message').show()
    $('#error-message').text(data)
  }

  var init = function () {
    $('#button-form').submit(function (e) {
      e.preventDefault()
      submit()
    })
  }

  return {
    setLatLon: setLatLon,
    getLatLon: getLatLon,
    init: init
  }
})()

$(document).ready(function () {
  form.init()

  map.init(form.getLatLon(), 16)
  map.addMarker(form.getLatLon())

  map.onClick(function (e) {
    map.addMarker(e.latlng, true)
    form.setLatLon(e.latlng.lat, e.latlng.lng)
  })
})

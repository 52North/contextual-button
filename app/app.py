from flask import Flask, render_template, request, jsonify, make_response
from uuid import uuid4
from datetime import datetime as dt, timezone
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_button')
def add_button():
    # extract lat lon values with fallback to Münster
    latlon = {}
    latlon['lat'] = request.args.get('lat', 52)
    latlon['lon'] = request.args.get('lon', 7)
    return render_template('add_button.html', latlon=latlon)


@app.route("/api/v1/sensors", methods=['POST'])
def create_sensor():
    sensor = request.get_json()
    sensor['id'] = uuid4()
    sensor_xml = render_template('sensor.xml', sensor=sensor)
    request_body = {"request": "InsertSensor",
                    "service": "SOS",
                    "version": "2.0.0",
                    "procedureDescriptionFormat": "http://www.opengis.net/sensorml/2.0",
                    "procedureDescription": sensor_xml,
                    "observableProperty": ["http://example.de/button_press"],
                    "observationType": ["http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_CountObservation"],
                    "featureOfInterestType": "http://www.opengis.net/def/samplingFeatureType/OGC-OM/2.0/SF_SamplingPoint"
                    }
    sos_res = requests.post(
        'http://sos:8080/52n-sos-webapp/service', json=request_body)
    response = make_response(sos_res.text, sos_res.status_code)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


@app.route('/api/v1/sensors/<string:id>/observation', methods=['POST'])
def create_observation(id):
    uuid = str(uuid4())
    time = dt.now(timezone.utc).isoformat(timespec='seconds')
    app.logger.debug(dt.now(timezone.utc).tzinfo)
    request_body = {"request": "InsertObservation",
                    "service": "SOS",
                    "version": "2.0.0",
                    "offering": "http://www.example.org/offering/{}/observations".format(id),
                    "observation": {
                        "identifier": {
                            "value": uuid,
                            "codespace": "http://www.opengis.net/def/nil/OGC/0/unknown"
                        },
                        "type": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_CountObservation",
                        "procedure": id,
                        "observedProperty": "http://example.org/button_press",
                        "featureOfInterest": {
                            "identifier": {
                                "value": "http://www.52north.org/test/featureOfInterest/9",
                                "codespace": "http://www.opengis.net/def/nil/OGC/0/unknown"
                            },
                            "name": [
                                {
                                    "value": "blub",
                                    "codespace": "http://www.opengis.net/def/nil/OGC/0/unknown"
                                }
                            ],
                            "sampledFeature": [
                                "http://www.52north.org/test/featureOfInterest/world"
                            ],
                            "geometry": {
                                "type": "Point",
                                "coordinates": [
                                    51.935101100104916,
                                    7.651968812254194
                                ],
                                "crs": {
                                    "type": "name",
                                    "properties": {
                                        "name": "EPSG:4326"
                                    }
                                }
                            }
                        },
                        "phenomenonTime": time,
                        "resultTime": time,
                        "result": 1
                    }}
    sos_res = requests.post(
        'http://sos:8080/52n-sos-webapp/service', json=request_body)
    response = make_response(sos_res.text, sos_res.status_code)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


@app.route('/api/v1/', methods=['GET'], defaults={'path': ''})
@app.route('/api/v1/<path:path>', methods=['GET'])
def redirect_api_calls(path):
    sos_res = requests.get(
        'http://sos:8080/52n-sos-webapp/api/v1/{}'.format(path), params=request.args.to_dict())
    response = make_response(sos_res.text, sos_res.status_code)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)

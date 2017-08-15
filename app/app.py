from flask import Flask, render_template, request, jsonify, make_response
from uuid import uuid4
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/api/v1/sensors", methods=['POST'])
def create_sensor():
    sensor = request.get_json()
    sensor['id'] = uuid4()
    sensor_xml = render_template('sensor.xml', sensor = sensor)
    request_body = {"request": "InsertSensor",
        "service": "SOS",
        "version": "2.0.0",
        "procedureDescriptionFormat": "http://www.opengis.net/sensorml/2.0",
        "procedureDescription":sensor_xml,
        "observableProperty": ["http://example.de/button_press"],
        "observationType": ["http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_CountObservation"],
        "featureOfInterestType": "http://www.opengis.net/def/samplingFeatureType/OGC-OM/2.0/SF_SamplingPoint"
    }
    sos_res = requests.post('http://sos:8080/52n-sos-webapp/service', json=request_body)
    response = make_response(sos_res.text, 201)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route('/api/v1/sensors/<int:id>/observation', methods=['POST'])
def create_observation():
    return 'create observation'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)

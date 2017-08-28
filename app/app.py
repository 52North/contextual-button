from flask import Flask, render_template, request, jsonify, make_response
from models import Sensor, Observation, FeatureOfInterest
import requests
import random

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


@app.route('/foi_popup')
def foi_popup():
    args = request.args.to_dict()
    if 'foi' in args:
        foi = args["foi"]
        filter_by = args.get("filter_by")
        popup_id = random.randrange(1, 100)
        data = Observation().get_filtered_for_foi(foi, filter_by)
        return render_template("popup.html", data=data, foi=foi, popup_id=popup_id)
    else:
        return ""


@app.route('/foi_popup/data')
def foi_popup_data():
    data = []
    args = request.args.to_dict()
    if 'foi' in args:
        foi = args["foi"]
        filter_by = args.get("filter_by")
        data = Observation().get_filtered_for_foi(foi, filter_by)
    return jsonify(data)


@app.route("/api/v1/sensors", methods=['POST'])
def create_sensor():
    sensor = request.get_json()
    sos_res = Sensor().create(sensor)
    response = make_response(sos_res.text, sos_res.status_code)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


@app.route('/api/v1/sensors/<string:id>/observation', methods=['POST'])
def create_observation(id):
    sos_res = Observation().create(id)
    response = make_response(sos_res.text, sos_res.status_code)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


@app.route('/api/v1/foi', methods=['GET'])
def getFOIs():
    sos_res = FeatureOfInterest().get_all()
    return jsonify(sos_res)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)

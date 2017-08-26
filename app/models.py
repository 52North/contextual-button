from flask import render_template
from datetime import datetime as dt, timezone
from uuid import uuid4
import json
import xmltodict
import requests


class Sensor:
    def create(self, sensor):
        sensor['id'] = uuid4()
        sensor['featureOfInterest'] = "http://example.org/featureOfInterest/" + \
            str(uuid4())
        sensor_xml = render_template('sensor.xml', sensor=sensor)
        request_body = {"request": "InsertSensor",
                        "service": "SOS",
                        "version": "2.0.0",
                        "procedureDescriptionFormat": "http://www.opengis.net/sensorml/2.0",
                        "procedureDescription": sensor_xml,
                        "observableProperty": ["http://example.org/button_press"],
                        "observationType": ["http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_CountObservation"],
                        "featureOfInterestType": "http://www.opengis.net/def/samplingFeatureType/OGC-OM/2.0/SF_SamplingPoint"
                        }
        return requests.post(
            'http://sos:8080/52n-sos-webapp/service', json=request_body)

    def get(self, id):
        request_body = {
            "request": "DescribeSensor",
            "service": "SOS",
            "version": "2.0.0",
            "procedureDescriptionFormat": "http://www.opengis.net/sensorml/2.0",
            "procedure": id
        }
        sos_res = requests.post(
            'http://sos:8080/52n-sos-webapp/service', json=request_body)
        sensor_xml = sos_res.json()["procedureDescription"]["description"]
        return xmltodict.parse(sensor_xml)


class Observation:
    def create(self, sensor_id):
        uuid = str(uuid4())
        time = dt.now(timezone.utc).isoformat(timespec='seconds')
        # get the feature of interest that is connected to the sensor
        feature_of_interest = self._get_feature_of_interest(sensor_id)
        request_body = {"request": "InsertObservation",
                        "service": "SOS",
                        "version": "2.0.0",
                        "offering": "http://www.example.org/offering/{}/observations".format(sensor_id),
                        "observation": {
                            "identifier": {
                                "value": uuid,
                                "codespace": "http://www.opengis.net/def/nil/OGC/0/unknown"
                            },
                            "type": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_CountObservation",
                            "procedure": sensor_id,
                            "observedProperty": "http://example.org/button_press",
                            "featureOfInterest": feature_of_interest,
                            "phenomenonTime": time,
                            "resultTime": time,
                            "result": 1
                        }}
        return requests.post(
            'http://sos:8080/52n-sos-webapp/service', json=request_body)

    def _get_feature_of_interest(self, id):
        # TODO try catch
        foi_res = FeatureOfInterest().get(id).json()
        if 'featureOfInterest' in foi_res and len(foi_res['featureOfInterest']) > 0:
            return foi_res['featureOfInterest'][0]
        else:
            return self._create_feature_of_interest_from_sensor(id)

    def _create_feature_of_interest_from_sensor(self, id):
        sensor = Sensor().get(id)["sml:PhysicalComponent"]
        feature_of_interest = {
            "identifier": {
                "value": sensor["sml:featuresOfInterest"]["sml:FeatureList"]["sml:feature"]["@xlink:href"],
                "codespace": "http://www.opengis.net/def/nil/OGC/0/unknown"
            },
            "name": [
                {"value": sensor["sml:identification"]["sml:IdentifierList"]["sml:identifier"][1]["sml:Term"]["sml:value"],
                 "codespace": "http://www.opengis.net/def/nil/OGC/0/unknown"}
            ],
            "geometry": {
                "type": "Point",
                "coordinates": self._get_coordinates_from_sensor_position(sensor["sml:position"]),
                "crs": {
                    "type": "name",
                    "properties": {
                        "name": "EPSG:4326"
                    }
                }
            }
        }
        return feature_of_interest

    def _get_coordinates_from_sensor_position(self, position):
        coordinates = [0] * 2 # init array length 2
        for coor in position["swe:Vector"]["swe:coordinate"]:
            value = float(coor["swe:Quantity"]["swe:value"])
            if coor["@name"] == "easting":
                coordinates[1] = value
            elif coor["@name"] == "northing":
                coordinates[0] = value
        return coordinates


class FeatureOfInterest:
    def get(self, sensor_id):
        request_body = {
            "request": "GetFeatureOfInterest",
            "service": "SOS",
            "version": "2.0.0",
            "procedure": sensor_id
        }
        return requests.post(
            'http://sos:8080/52n-sos-webapp/service', json=request_body)

    def get_all(self):
        request_body = {
            "request": "GetFeatureOfInterest",
            "service": "SOS",
            "version": "2.0.0"
        }
        sos_res = requests.post(
            'http://sos:8080/52n-sos-webapp/service', json=request_body)
        fois = sos_res.json()["featureOfInterest"]
        results = []
        for foi in fois:
            feature = {"type": "Feature",
            "properties": {}}

            feature["id"] = foi["identifier"]["value"]
            feature["geometry"] = foi["geometry"]
            feature["properties"]["name"] = foi["name"]["value"]
            results.append(feature)
        return results

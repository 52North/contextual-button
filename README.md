# Contextual Button

This project was created as part of the [52°North Student Innovation Challenge 2017](http://52north.org/about/other-activities/student-innovation-prize/current-call). This years Challenge focused on connecting the Internet of Things with Sensor Web technologies.

My entry into the challenge was inspired by the Amazon Dash button a small internet enabled device that allows Amazone customers to order refills for their consumable goods (e.g. razor blades, washing powder, etc.). Basically it is a small button that when pressed connects to Amazon and places an order for the respective item. The customer does not have to go to the website to do it themselves.
The interesting part is that the action of doing that is replaced by a physical action that is directly integrated in the context the user currently is in. For example when the user just used the last of the washing powder they can directly press the button attached to the washing machine to order a refill. The whole interaction takes place in the same pythoscal context.
With the Contextual Button I took the concept of adding physical interactions into different contexts and made it applicable to other situations. Similarly to the Dash Button the Contextual Button is a small button that connects to the internet when pressed, with the difference that the call that is made can be directed to any website.

While the physical device is one part of the project the second part is an infrastructure that integrates the registered button presses with a Sensor Observation Service(SOS) that allows then to manage the registered button presses from multiple buttons.

I will briefly explain how to install the system, and the provided functions followed by a small explanation of how to make your own button.

## Installation
As 52°North provides a docker image for the [SOS](https://hub.docker.com/r/52north/sos/) I decided to implement my own functionality in an additional Docker container that sits between the button and the SOS providing extra functions an small web frontend.
All together can be started from the project directory with:
```
docker-compose build
docker-compose up
```
Afterwards the SOS has to be configured to work with the database and a to allow transactional operations from external IPs for this do the following:
1. Go to [http://localhost:8080/52n-sos-webapp/](http://localhost:8080/52n-sos-webapp/)
2. Click in the notification box on top of the screen to complete the Installation
3. Click "Start"
4. Choose "PostgreSQL/PostGIS" as datasource
5. Set host to "postgres" and click "Next".
6. Choose the "Transactional Security" tab and remove the checkmark at "Transactional security active" (Note: On a productive system you probably should not do this but rather define a rule for allowed IPs)
7. Click "Next" and finish the installation by setting an admin user with password.
8. Go to [http://localhost:8080/52n-sos-webapp/admin/operations](http://localhost:8080/52n-sos-webapp/admin/operations) and activate the "InsertSensor", and the "InsertObservation" operations.

The installation is now completed and you can access the frontend under [http://localhost](http://localhost)
## Frontend

The frontend provides map view that shows all buttons (or rather the features of interest they are attached to) as markers. Clicking one of the markers opens a popup with a diagram showing the number of button presses aggregated in different ways. With a drop down selector three ways of aggregation can be selected: by date, by hour of the day and by weekday. This shows at which times the button was pressed how often.

Clicking the map at a different position opens a popup asking whether a new button should be registered at this location. Upon clicking the link the user is presented with a form to enter a name and a description for the button.

## API
The API provides two endpoints, that wrap the SOS JSON-Bindings and allow the creation of Sensors and observations. The responses are directly returned from the SOS.

### POST /api/v1/sensors

#### Parameters
+ **long_name(string):** A long and detailed name
+ **short_name(string):** A short name
+ **description(string):** Description of the Sensor
+ **lat(number):** Latitude of the Sensor
+ **lon(number):** Longitude of the Sensor

#### Example Request
POST http://example.org/api/v1/sensors
```
{
  "long_name":"long very detailed name",
  "short_name":"shrt nm",
	"description":"A description of the sensor",
	"lat": 7.2,
	"lon": 52
}
```

#### Example Response
200 OK
```
{
  "request": "InsertSensor",
  "version": "2.0.0",
  "service": "SOS",
  "assignedProcedure": "8df6efc0-5513-4d56-8ef9-a6cceccd8499",
  "assignedOffering": "http://www.example.org/offering/8df6efc0-5513-4d56-8ef9-a6cceccd8499/observations"
}
```


### POST/api/v1/sensor/<sensor_id>/observations

#### Parameters
+ **sensor_id(string):** ID of the sensor the observation belongs to

#### Example Request
POST http://example.org/api/v1/sensors/8df6efc0-5513-4d56-8ef9-a6cceccd8499/observations

```
{}
```

#### Example Response
200 OK
```
{
  "request": "InsertObservation",
  "version": "2.0.0",
  "service": "SOS"
}
```

## The Button

The button uses an ESP8266 Arduino module to connect to a specified WIFI and,
when it is pressed, it makes a POST request to the Observation route specified above.

For the prototype I used an [NodeMCU v1.0](https://en.wikipedia.org/wiki/NodeMCU) as it has a USB port which makes it easier to deploy code to it.
For the final version the smaller ESP8266 ESP-01 might be a better option.

(Image)
TODO add Image

I setup my board with a button and three LEDs, that indicate the state of the request (yellow = connecting, green = success, red = failure). While they are not really necessary they help with debugging.

The code needed to run the button can be found in the contextual_button folder. To get it running you simply have to fill in the correct parameters for your environment on top of the script and upload it to the device.
```C
const char* ssid = "SSID";
const char* password = "password";
const char* baseUrl = "http://example.org";
const char* sensorID = "sensor-example-id";
```

To get the code running you might have to install the Arduino libraries for the ESP8266. You will find an explanation of how that works [here](https://github.com/esp8266/Arduino)

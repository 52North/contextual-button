# Contextual Button

This project was created as part of the [52°North Student Innovation Challenge 2017](http://52north.org/about/other-activities/student-innovation-prize/current-call). This years challenge focused on connecting the Internet of Things with Sensor Web technologies.

My entry into the challenge was inspired by the Amazon Dash button, a small internet enabled device that allows Amazon customers to order refills for their consumable goods (e.g. razor blades, washing powder, etc.). Basically, it is a small button that when pressed, connects to Amazon and places an order for the respective item. This way, the customer does not have to go to the website to do it themselves.  
The interesting part is that the action of going online is replaced by a physical action that is directly integrated in the user's current context. For example, when the user has just used the last of the washing powder, they can directly press the button attached to the washing machine to order a refill. The whole interaction takes place in the same context.  
With the Contextual Button, I took the idea of adding physical interactions into different contexts and made it applicable to other situations. Similarly to the Dash Button, the Contextual Button is a small button that connects to the internet when pressed. The difference is that it can be modified to make requests to any website.

While the physical device is one part of the project, the second part is an infrastructure that integrates the registered button presses into a Sensor Observation Service (SOS). The SOS then allows to manage the registered button presses from multiple buttons.

I will briefly explain how to install the system and the provided functions, followed by a small explanation of how to make your own button.

## Installation
As 52°North provides a docker image for the [SOS](https://hub.docker.com/r/52north/sos/), I decided to implement my own functionality in an additional Docker container that sits between the button and the SOS, providing extra functions and a small web frontend.  
All together can be started from the project directory with:
```
docker-compose build
docker-compose up
```
Afterwards, the SOS has to be configured to work with the database and a to allow transactional operations from external IPs. To do this follow the following steps:
1. Go to [http://localhost:8080/52n-sos-webapp/](http://localhost:8080/52n-sos-webapp/)
2. Click in the notification box on top of the screen to complete the installation
3. Click "Start"
4. Choose "PostgreSQL/PostGIS" as datasource
5. Set the host to "postgres" and click "Next"
6. Choose the "Transactional Security" tab and remove the checkmark "Transactional security active" (Note: On a productive system you probably should not do this, but rather define a rule for allowed IPs)
7. Click "Next" and finish the installation by setting an admin user with password
8. Go to [http://localhost:8080/52n-sos-webapp/admin/operations](http://localhost:8080/52n-sos-webapp/admin/operations) and activate the "InsertSensor" and the "InsertObservation" operations.

The installation is now completed and you can access the frontend under [http://localhost](http://localhost)
## Frontend

The frontend provides a map view that shows all buttons (or rather the features of interest they are attached to) as markers. When clicking one of the markers, a popup appears showing a diagram with the number of button presses aggregated in different ways. With a drop down selector, one of three ways of aggregation can be selected: by date, by hour of the day and by weekday. This shows how often the button was pressed and at which times.

Clicking the map at a different position opens a popup asking whether a new button should be registered at this location. After clicking the link, the user is presented with a form to enter a name and a description for the button.

## API
The API provides two endpoints that wrap the SOS JSON-Bindings and allow the creation of sensors and observations. The responses are directly returned from the SOS.

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
	"lat": 51.963545851239274,
	"lon": 7.623589038848878
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
when it is pressed, it makes a POST request to the observation route specified above.

For the prototype, I used an [NodeMCU v1.0](https://en.wikipedia.org/wiki/NodeMCU), because it has a USB port, which makes it easier to deploy code to it. For the final version the smaller ESP8266 ESP-01 might be a better option.

<img src="/JanVan01/contextual-button/raw/master/button_circuit.png" alt="Button Circuit" style="max-width: 50%;">
(Image created with [http://fritzing.org](http://fritzing.org))

The image above shows how to wire the button. My setup not only contains the button but also three LEDs that indicate the state of the request (yellow = connecting, green = success, red = failure). While the LEDs are not really necessary, they help with debugging.

The code that is needed to run the button can be found in the contextual_button folder. To get it running you simply have to fill in the correct parameters for your environment on top of the script and upload it to the device.
```C
const char* ssid = "SSID";
const char* password = "password";
const char* baseUrl = "http://example.org";
const char* sensorID = "sensor-example-id";
```

To get the code running you might have to install the Arduino libraries for the ESP8266 first. You will find an explanation of how that works [here](https://github.com/esp8266/Arduino)

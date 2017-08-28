#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "SSID";
const char* password = "password";
const char* baseUrl = "http://example.org";
const char* sensorID = "sensor-example-id";

const int button = 4;     
const int red =  0;
const int yellow =  16;
const int green =  5;

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ;
  }
  pinMode(red, OUTPUT);
  pinMode(yellow, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(button, INPUT);
}

void loop() {

  if (digitalRead(button) == HIGH) {
    Serial.println("Button pressed");
    digitalWrite(yellow, HIGH);
    WiFi.begin(ssid, password);
    Serial.println("Connecting");
    while (WiFi.status() != WL_CONNECTED) {
      delay(1000);
      Serial.print(".");
    }
    Serial.println("");
    Serial.println("Connected");
    
    HTTPClient http;
    http.begin(baseUrl + "/api/v1/sensors/" + sensorID + "/observations");
    int httpCode = http.POST("");
    Serial.println(httpCode);
    digitalWrite(yellow, LOW);
    if (httpCode > 0) {
      String payload = http.getString();
      Serial.println(payload);
      digitalWrite(green, HIGH);
      delay(1000);
      digitalWrite(green, LOW);
    } else {
      digitalWrite(red, HIGH);
      delay(1000);
      digitalWrite(red, LOW);
    }
    http.end();
    WiFi.disconnect();
  }
}

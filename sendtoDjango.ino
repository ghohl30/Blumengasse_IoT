#include <ESP8266WiFi.h>

/* 
https://techtutorialsx.com/2016/07/21/esp8266-post-requests/ 
https://github.com/espressif/arduino-esp32/issues/3483
*/

#include "FS.h" // SPIFFS is declared
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>


#include "DHT.h"                
#define DHTPIN 2          // Hier die Pin Nummer eintragen wo der Sensor angeschlossen ist
#define DHTTYPE DHT22     // Hier wird definiert was für ein Sensor ausgelesen wird. In 
                          // unserem Beispiel möchten wir einen DHT11 auslesen, falls du 
                          // ein DHT22 hast einfach DHT22 eintragen

DHT dht(DHTPIN, DHTTYPE);

/* Define configurations for the sensor. Will be loaded from config.json */

int sensorPin = A0;    // select the input pin for the potentiometer
int sensorValue = 0; 
String ssid;  
String password; 
String servername;
String port;
String sensor_type;
int sensor_number;
int AirValue;
int WaterValue;
int interval;

int pinout = 12;

void setup()
{
  pinMode(pinout, OUTPUT);
  Serial.begin(115200);
  Serial.println();
  if (SPIFFS.begin()) {
    Serial.println("Mounting successfull!");
  }
  delay(100);
  digitalWrite(pinout, HIGH);

  // load config.json
  load_configs();

  // connect with the wifi
  connect_wifi();

  // register with server
  register_server();

  delay(2000);
  // for the humidity and temperature sensor
  dht.begin();
}


void loop() {

  // Step 1: Get sensor data
  float h = dht.readHumidity();    // Lesen der Luftfeuchtigkeit und speichern in die Variable h
  float t = dht.readTemperature(); // Lesen der Temperatur in °C und speichern in die Variable t
  // sensorValue = analogRead(sensorPin);
  // int p;
  // p = map(sensorValue, AirValue, WaterValue, 0, 100);
  //  Serial.println(p);
  //  float h = random(20,40);
  //  float t = random(100,200);


  // Step 2: Get ready to post to server

  WiFiClient wifiClient;
  HTTPClient http;

  String url = "http://";
  url += servername + ":" + port + "/data/" + sensor_number;
  Serial.println(url);
  http.begin(wifiClient, url);

  const int capacity = JSON_OBJECT_SIZE(100);
  StaticJsonDocument<capacity> doc;
  //  doc["sensor"] = sensor_number;
  doc["Temperatur"] = t;
  doc["Luftfeuchtigkeit"] = h;
  // doc["Bodenfeuchtigkeit"] = p;
  String postMessage;
  serializeJsonPretty(doc, postMessage);

  http.addHeader("Content-Type", "application/json");
  http.addHeader("token",  "1234");
  
  Serial.println(postMessage);
  int httpCode = http.POST(postMessage);
  String payload = http.getString();

  // Deserialize Json
  const int cap = JSON_OBJECT_SIZE(4);
  StaticJsonDocument<cap> settings;
  deserializeJson(settings, payload);
  if (settings["interval"]) {
    int i = settings["interval"];
    interval = 1000*int(i);
  }
  
  Serial.println(httpCode);
  Serial.println(payload);
  http.end();

  digitalWrite(pinout, LOW);
  ESP.deepSleep(interval*10e2);
  // delay(interval);  
}

void connect_wifi() {
  Serial.printf("Verbinde mit %s ", ssid);
  WiFi.begin(ssid, password); // Versucht mit WLAN Name und Schlüssel zu verbinden
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" verbunden");
}

void load_configs() {
  File f = SPIFFS.open("/config.json", "r");

  // getting content and printing it
  size_t size = f.size();
  Serial.println(size);

  char buf[size];
  int puff = f.readBytes(buf, size);
  Serial.println(puff);
  Serial.println(buf);
  f.close(); 

  StaticJsonDocument<200> doc;
  deserializeJson(doc, buf);

  ssid = doc["ssid"].as<String>();;
  password = doc["password"].as<String>();;
  servername = doc["servername"].as<String>();;
  port = doc["port"].as<String>();
  sensor_number = doc["sensor_number"];
  sensor_type = doc["sensor_type"].as<String>();
  AirValue = doc["min_humid_val"];
  WaterValue = doc["max_humid_val"];
  interval = doc["interval"];
}

void register_server() {
  WiFiClient wifiClient;
  HTTPClient http;
  
  String url = "http://";
  url += servername + ":" + port + "/register";
  Serial.println(url);
  http.begin(wifiClient, url);
  
  const int capacity = JSON_OBJECT_SIZE(100);
  StaticJsonDocument<capacity> doc;
  doc["sensor_id"] = sensor_number;
  doc["sensor_type"] = sensor_type;
  doc["interval"] = interval/1000;
  String postMessage;
  serializeJsonPretty(doc, postMessage);
  Serial.println(postMessage);
  
  http.addHeader("Content-Type", "application/json");
  http.addHeader("token",  "1234");
  
  int httpCode = http.POST(postMessage);
  String payload = http.getString();

  Serial.println(httpCode);
  Serial.println(payload);
  http.end();
}

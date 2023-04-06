Blumengasse_IoT
Welcome to Blumengasse IoT, a project that brings the 21<sup>st</sup> century to my parent's house by setting up a local Django webserver capable of communicating with sensors and IoT devices through the local Wi-Fi. As of now, the system consists of two humidity and temperature sensors, with plans to expand in the near future.

<p align="center">
<img width="400" alt="Screenshot" src="https://user-images.githubusercontent.com/74073756/148589246-f7a9ea83-25eb-4b6f-9030-950c05cdf8b3.png">
</p>
The repository contains the Django webserver code and the Arduino code for the D1 Mini microcontroller, which is responsible for sending sensor measurements to the Django server. The microcontroller sends data and then goes to sleep for a specified interval, as configured in the config.json file. To set up the microcontroller, simply upload the provided Arduino code (found in this repository) to the D1 Mini.

Important: Make sure to upload the config.json file in the correct format to the microcontroller's SPIFFS file system. This file is essential for proper communication between the server and the microcontroller. Use the following format for the `config.json` file:

```json
{
  "ssid": "your_wifi_ssid",
  "password": "your_wifi_password",
  "servername": "your_server_address",
  "port": "your_server_port",
  "sensor_number": sensor_id_number,
  "sensor_type": "sensor_type_string",
  "min_humid_val": minimum_humidity_value,
  "max_humid_val": maximum_humidity_value,
  "interval": data_sending_interval_in_seconds
}
```

<p align="center">
<img width="400" alt="Screenshot" src="https://user-images.githubusercontent.com/74073756/148590121-cedf8cf1-6a32-4c89-ab50-c1fc8a2658d4.jpeg">
</p>

The project is currently running seamlessly at my family's home. The server is hosted on a Raspberry Pi Zero, which has proven to be a reliable and energy-efficient solution for this application.

Please note that the data in the first image may appear suspicious because the screenshot was taken during testing while I was constantly touching the device, and it was being charged (which leads to heating). A more current and representative image will replace the existing one the next time I visit home.

Stay tuned for updates, as I will be uploading additional information such as the component list, CAD files for the sensor cases, and more.
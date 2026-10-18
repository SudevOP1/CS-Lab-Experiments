
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const int soilPin = A0;

// calibrate these by reading the sensor in dry air and in water
const int dryValue = 1023;
const int wetValue = 300;

const char *ssid = "YOUR_WIFI";
const char *password = "YOUR_PASSWORD";
const char *mqttBroker = "192.168.1.10"; // ip of pc running mosquitto + node-red
const int mqttPort = 1883;
const char *topic = "ioe/exp4/soil/raw";

WiFiClient espClient;
PubSubClient client(espClient);

void connectMqtt()
{
    while (!client.connected())
    {
        Serial.print("Connecting to MQTT...");
        if (client.connect("soil-node-01"))
            Serial.println("connected");
        else
        {
            Serial.print("failed, state=");
            Serial.println(client.state());
            delay(2000);
        }
    }
}

void setup()
{
    Serial.begin(115200);

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println();
    Serial.println("WiFi Connected");

    client.setServer(mqttBroker, mqttPort);
}

void loop()
{
    connectMqtt();
    client.loop();

    int soilValue = analogRead(soilPin);
    int moisturePercent = map(soilValue, dryValue, wetValue, 0, 100);
    moisturePercent = constrain(moisturePercent, 0, 100);

    char payload[80];
    sprintf(payload, "{\"device\":\"soil-node-01\",\"raw\":%d,\"moisture\":%d}", soilValue, moisturePercent);

    client.publish(topic, payload);
    Serial.print("Published: ");
    Serial.println(payload);

    delay(5000);
}

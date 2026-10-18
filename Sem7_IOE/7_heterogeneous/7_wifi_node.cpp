
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

const char *ssid = "YOUR_WIFI";
const char *password = "YOUR_PASSWORD";
const char *mqttBroker = "192.168.1.10"; // ip of pc running mosquitto
const int mqttPort = 1883;
const char *topic = "ioe/wifi/sensor";

WiFiClient espClient;
PubSubClient client(espClient);

void connectMqtt()
{
    while (!client.connected())
    {
        Serial.print("Connecting to MQTT...");
        if (client.connect("ESP32-WiFi-Node"))
            Serial.println("connected");
        else
        {
            Serial.println("failed, retrying");
            delay(2000);
        }
    }
}

void setup()
{
    Serial.begin(115200);
    dht.begin();

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

    float temperature = dht.readTemperature();

    char payload[100];
    sprintf(payload, "{\"device\":\"ESP32\",\"protocol\":\"WiFi\",\"temperature\":%.1f}", temperature);

    client.publish(topic, payload);
    Serial.print("Published: ");
    Serial.println(payload);

    delay(5000);
}

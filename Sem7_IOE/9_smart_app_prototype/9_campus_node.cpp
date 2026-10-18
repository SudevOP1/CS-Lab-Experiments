
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

const int ldrPin = 34;     // light sensor (analog)
const int irEntryPin = 18; // ir sensor at entry door (LOW when someone passes)
const int irExitPin = 19;  // ir sensor at exit door

const char *ssid = "YOUR_WIFI";
const char *password = "YOUR_PASSWORD";
const char *mqttBroker = "192.168.1.10"; // ip of pc running mosquitto
const int mqttPort = 1883;
const char *mqttUser = "campus-node";
const char *mqttPass = "YOUR_MQTT_PASSWORD";
const char *topic = "ioe/exp9/campus/sensor";

WiFiClient espClient;
PubSubClient client(espClient);

int occupancy = 0;
int lastEntry = HIGH;
int lastExit = HIGH;
unsigned long lastPublish = 0;

void connectMqtt()
{
    while (!client.connected())
    {
        Serial.print("Connecting to MQTT...");
        if (client.connect("campus-node-01", mqttUser, mqttPass))
            Serial.println("connected");
        else
        {
            Serial.print("failed, state=");
            Serial.println(client.state());
            delay(2000);
        }
    }
}

void countPeople()
{
    int entry = digitalRead(irEntryPin);
    int exit = digitalRead(irExitPin);

    // count only on falling edge so one person is counted once
    if (lastEntry == HIGH && entry == LOW)
        occupancy++;
    if (lastExit == HIGH && exit == LOW && occupancy > 0)
        occupancy--;

    lastEntry = entry;
    lastExit = exit;
}

void setup()
{
    Serial.begin(115200);
    dht.begin();
    pinMode(irEntryPin, INPUT);
    pinMode(irExitPin, INPUT);

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
    countPeople();

    if (millis() - lastPublish < 5000)
        return;
    lastPublish = millis();

    float temperature = dht.readTemperature();
    int lightLux = map(analogRead(ldrPin), 0, 4095, 0, 1000); // approximate lux

    if (isnan(temperature))
    {
        Serial.println("DHT read failed, skipping");
        return;
    }

    char payload[160];
    sprintf(payload,
            "{\"device\":\"campus-node-01\",\"application\":\"SmartCampus\","
            "\"temperature_c\":%.1f,\"occupancy\":%d,\"light_lux\":%d}",
            temperature, occupancy, lightLux);

    client.publish(topic, payload);
    Serial.print("Published: ");
    Serial.println(payload);
}

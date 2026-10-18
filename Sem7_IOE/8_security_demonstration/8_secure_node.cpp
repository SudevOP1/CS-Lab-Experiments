
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>

const char *ssid = "YOUR_WIFI";
const char *password = "YOUR_PASSWORD";

const char *mqttBroker = "192.168.1.10"; // must match CN of server.crt
const int mqttPort = 8883;
const char *mqttUser = "esp32";
const char *mqttPass = "esp32pass";
const char *topic = "ioe/security/sensor";

const int mq2Pin = 34;

// paste contents of ca.crt here
const char *caCert =
    "-----BEGIN CERTIFICATE-----\n"
    "...\n"
    "-----END CERTIFICATE-----\n";

WiFiClientSecure secureClient;
PubSubClient client(secureClient);

void connectMqtt()
{
    while (!client.connected())
    {
        Serial.print("Connecting to MQTT over TLS...");
        unsigned long start = millis();

        if (client.connect("ESP32-Secure-Node", mqttUser, mqttPass))
        {
            Serial.print("connected in ");
            Serial.print(millis() - start);
            Serial.println(" ms");
        }
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

    secureClient.setCACert(caCert);
    client.setServer(mqttBroker, mqttPort);
}

void loop()
{
    connectMqtt();
    client.loop();

    int value = analogRead(mq2Pin);

    char payload[100];
    sprintf(payload, "{\"device\":\"ESP32\",\"protocol\":\"MQTTS\",\"sensor\":\"MQ-2\",\"value\":%d}", value);

    client.publish(topic, payload);
    Serial.print("Published: ");
    Serial.println(payload);

    delay(5000);
}

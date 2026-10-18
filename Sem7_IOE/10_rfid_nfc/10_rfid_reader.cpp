
#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
#include <PubSubClient.h>

// mfrc522 (3.3V only) -> esp32: SDA=5, SCK=18, MOSI=23, MISO=19, RST=22
#define SS_PIN 5
#define RST_PIN 22

const int greenLed = 25;
const int redLed = 26;

const char *ssid = "YOUR_WIFI";
const char *password = "YOUR_PASSWORD";
const char *mqttBroker = "192.168.1.10"; // ip of pc running mosquitto
const int mqttPort = 1883;

const char *readerId = "LAB-A-READER-01";
const char *eventType = "ACCESS_ATTEMPT"; // use "ASSET_SCAN" for an inventory reader
const char *scanTopic = "ioe/rfid/scan";
const char *eventTopic = "ioe/rfid/access-events";

MFRC522 rfid(SS_PIN, RST_PIN);
WiFiClient espClient;
PubSubClient client(espClient);

// decision is made by the application, reader only shows the result
void onMessage(char *topic, byte *payload, unsigned int length)
{
    String msg;
    for (unsigned int i = 0; i < length; i++)
        msg += (char)payload[i];

    if (msg.indexOf(readerId) < 0)
        return;

    bool granted = msg.indexOf("ACCESS_GRANTED") >= 0 || msg.indexOf("ASSET_RECORDED") >= 0;
    Serial.println(granted ? "ACCESS GRANTED" : "ACCESS DENIED");

    digitalWrite(granted ? greenLed : redLed, HIGH);
    delay(1000);
    digitalWrite(greenLed, LOW);
    digitalWrite(redLed, LOW);
}

void connectMqtt()
{
    while (!client.connected())
    {
        Serial.print("Connecting to MQTT...");
        if (client.connect(readerId))
        {
            Serial.println("connected");
            client.subscribe(eventTopic);
        }
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
    pinMode(greenLed, OUTPUT);
    pinMode(redLed, OUTPUT);

    SPI.begin();
    rfid.PCD_Init();

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println();
    Serial.println("WiFi Connected");

    client.setServer(mqttBroker, mqttPort);
    client.setCallback(onMessage);
    Serial.println("Scan a tag...");
}

void loop()
{
    connectMqtt();
    client.loop();

    if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial())
        return;

    char uid[32] = "";
    for (byte i = 0; i < rfid.uid.size; i++)
    {
        char part[4];
        sprintf(part, i == 0 ? "%02X" : " %02X", rfid.uid.uidByte[i]);
        strcat(uid, part);
    }
    Serial.print("Tag UID: ");
    Serial.println(uid);

    // no timestamp here, the server assigns it on receipt
    char payload[150];
    sprintf(payload, "{\"reader_id\":\"%s\",\"tag_uid\":\"%s\",\"event_type\":\"%s\"}", readerId, uid, eventType);
    client.publish(scanTopic, payload);

    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();
    delay(1500);
}

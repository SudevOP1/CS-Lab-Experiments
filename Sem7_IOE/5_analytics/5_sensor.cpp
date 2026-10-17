
#include <ESP8266WiFi.h>
#include <DHT.h>

#define DHTPIN D4
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

const char *ssid = "YOUR_WIFI";
const char *password = "YOUR_PASSWORD";

unsigned long startTime;

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

    Serial.println("Timestamp,Temperature,Humidity");
    startTime = millis();
}

void loop()
{
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    // prints one csv row, copy serial monitor output into sensor_data.csv
    unsigned long t = (millis() - startTime) / 1000;
    char timestamp[9];
    sprintf(timestamp, "%02lu:%02lu:%02lu", t / 3600, (t / 60) % 60, t % 60);

    Serial.print(timestamp);
    Serial.print(",");
    if (!isnan(temperature))
        Serial.print(temperature);
    Serial.print(",");
    if (!isnan(humidity))
        Serial.print(humidity);
    Serial.println();

    delay(5000);
}

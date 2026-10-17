
const int soilPin = A0;

// calibrate these by reading the sensor in dry air and in water
const int dryValue = 1023;
const int wetValue = 300;

int soilValue;
int moisturePercent;

void setup()
{
    Serial.begin(115200);
}

void loop()
{
    soilValue = analogRead(soilPin);
    moisturePercent = map(soilValue, dryValue, wetValue, 0, 100);
    moisturePercent = constrain(moisturePercent, 0, 100);

    Serial.print("Soil Moisture: ");
    Serial.println(moisturePercent);

    delay(5000);
}

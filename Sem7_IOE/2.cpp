
const int gasPin = A0;
const int buzzerPin = 8;
const int redLedPin = 7;
const int greenLedPin = 6;

const int threshold = 400;

int gasValue;

void setup()
{
    Serial.begin(9600);
    pinMode(buzzerPin, OUTPUT);
    pinMode(redLedPin, OUTPUT);
    pinMode(greenLedPin, OUTPUT);
}

void loop()
{
    gasValue = analogRead(gasPin);

    Serial.print("Gas Value: ");
    Serial.print(gasValue);

    if (gasValue > threshold)
    {
        digitalWrite(redLedPin, HIGH);
        digitalWrite(greenLedPin, LOW);
        tone(buzzerPin, 1000);
        Serial.println(" -> SMOKE DETECTED!");
    }
    else
    {
        digitalWrite(redLedPin, LOW);
        digitalWrite(greenLedPin, HIGH);
        noTone(buzzerPin);
        Serial.println(" -> Safe");
    }

    delay(500);
}


const int redPin = 11;
const int yellowPin = 12;
const int greenPin = 13;

// 7 segment (common cathode) pins for segments a, b, c, d, e, f, g
const int segPins[7] = {2, 3, 4, 5, 6, 7, 8};

const byte digits[10][7] = {
    {1, 1, 1, 1, 1, 1, 0}, // 0
    {0, 1, 1, 0, 0, 0, 0}, // 1
    {1, 1, 0, 1, 1, 0, 1}, // 2
    {1, 1, 1, 1, 0, 0, 1}, // 3
    {0, 1, 1, 0, 0, 1, 1}, // 4
    {1, 0, 1, 1, 0, 1, 1}, // 5
    {1, 0, 1, 1, 1, 1, 1}, // 6
    {1, 1, 1, 0, 0, 0, 0}, // 7
    {1, 1, 1, 1, 1, 1, 1}, // 8
    {1, 1, 1, 1, 0, 1, 1}  // 9
};

void showDigit(int n)
{
    for (int i = 0; i < 7; i++)
        digitalWrite(segPins[i], digits[n][i]);
}

void runLight(int pin, int seconds, const char *name)
{
    digitalWrite(pin, HIGH);
    Serial.println(name);

    for (int t = seconds; t >= 0; t--)
    {
        showDigit(t);
        delay(1000);
    }

    digitalWrite(pin, LOW);
}

void setup()
{
    Serial.begin(9600);
    pinMode(redPin, OUTPUT);
    pinMode(yellowPin, OUTPUT);
    pinMode(greenPin, OUTPUT);

    for (int i = 0; i < 7; i++)
        pinMode(segPins[i], OUTPUT);
}

void loop()
{
    runLight(redPin, 9, "RED - Stop");
    runLight(greenPin, 9, "GREEN - Go");
    runLight(yellowPin, 3, "YELLOW - Wait");
}

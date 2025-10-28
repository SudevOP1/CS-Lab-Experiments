
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <ESP32Servo.h>

const int SERVO_PIN = 12;
Servo myServo;

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define SCREEN_ADDRESS 0x3C

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup()
{
    Serial.begin(115200);

    // 1. initialize the OLED display
    if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS))
    {
        Serial.println(F("SSD1306 allocation failed"));
        for (;;)
            ;
    }
    Serial.println("OLED display initialized.");

    // clear the display buffer and show initial message
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);
    display.println("System Ready!");
    display.display();
    delay(1000);

    // 2. initialize the servo motor
    myServo.attach(SERVO_PIN);
    myServo.write(0);
    Serial.println("Servo initialized.");
}

void loop()
{

    // sweep the servo from 0 to 180 degrees
    for (int pos = 0; pos <= 180; pos += 1)
    {
        myServo.write(pos);
        updateDisplay(pos);
        delay(15);
    }

    // sweep the servo from 180 back to 0 degrees
    for (int pos = 180; pos >= 0; pos -= 1)
    {
        myServo.write(pos);
        updateDisplay(pos);
        delay(15);
    }
}

// update the OLED display text
void updateDisplay(int angle)
{
    display.clearDisplay();
    display.setCursor(0, 0);
    display.print("Angle:");
    display.setCursor(0, 20);
    display.print(angle);
    display.print(" deg");
    display.display();
}

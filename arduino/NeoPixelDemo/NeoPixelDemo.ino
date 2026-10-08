/* Blink NeoPixel*/
#include <Adafruit_NeoPixel.h>

#define PIN 8

Adafruit_NeoPixel neo(1, PIN, NEO_GRB + NEO_KHZ800);

#define DELAYVAL 500 // Time (in milliseconds) to pause between pixels

void setup() {
  neo.begin();
  neo.show();
  Serial.begin(115200);
  delay(1000);
  Serial.println("\nLet's start!");
  Serial.println("Pin used: 8");
}

void loop() {
  neo.setPixelColor(1, 255, 0, 255);
  neo.show();
  delay(2000);
  neo.setPixelColor(1, 0, 255, 255);
  delay(2000);
  neo.show();
  Serial.println("Es geht was.");
}

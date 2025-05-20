#include <Wire.h>
#include "Adafruit_HTU21DF.h"

Adafruit_HTU21DF htu = Adafruit_HTU21DF();

void setup() {
  Serial.begin(9600);
  Serial.println("Testing HTU21D...");
  

  if (!htu.begin()) {
    Serial.println("HTU21D sensor not found!");
    while (1);
  }
}

void loop() {
  float temp = htu.readTemperature();
  float hum = htu.readHumidity();

  Serial.print("Temperature: ");
  Serial.print(temp);
  Serial.println(" °C");

  Serial.print("Humidity: ");
  Serial.print(hum);
  Serial.println(" %");

  delay(2000); // Waits 2 seconds
}

#include <Wire.h>
#include "Adafruit_HTU21DF.h"

Adafruit_HTU21DF htu = Adafruit_HTU21DF();

void setup() {
  Serial.begin(9600);
  Serial.println("Testando HTU21D...");
  

  if (!htu.begin()) {
    Serial.println("Sensor HTU21D não encontrado!");
    while (1);
  }
}

void loop() {
  float temp = htu.readTemperature();
  float hum = htu.readHumidity();

  Serial.print("Temperatura: ");
  Serial.print(temp);
  Serial.println(" °C");

  Serial.print("Umidade: ");
  Serial.print(hum);
  Serial.println(" %");

  delay(2000); // Aguarda 2 segundos
}

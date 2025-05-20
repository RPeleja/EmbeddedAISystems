#include <Wire.h>
#include <iostream>
#include "Adafruit_HTU21DF.h"
#include "LinearRegression.h"
Eloquent::ML::Port::LinearRegression model;

// Criar instância do sensor
Adafruit_HTU21DF htu = Adafruit_HTU21DF();

int calcularTempoRega(float temperatura, float humidade) {
    // Set base values and limits
    float tempoBaseRega = 1.0;  // watering minutes in normal conditions
    
    // The higher the temperature, the longer the watering time
    float fatorTemperatura = 0.0;
    if (temperatura < 15.0) {
        fatorTemperatura = -2.0;  // Reduce time on cold days
    } else if (temperatura >= 15.0 && temperatura < 25.0) {
        fatorTemperatura = 0.0;   // Normal conditions
    } else if (temperatura >= 25.0 && temperatura < 30.0) {
        fatorTemperatura = 3.0;   // Increase a bit on hot days
    } else if (temperatura >= 30.0 && temperatura < 35.0) {
        fatorTemperatura = 5.0;   // Increase more on very hot days
    } else if (temperatura >= 35.0 && temperatura < 40.0) {
        fatorTemperatura = 15.0;   // Increase more on very hot days
    } else {
        fatorTemperatura = 48.0;   // Significantly increase on extremely hot days
    }
    
    // Adjustment based on humidity
    // The lower the humidity, the longer the watering time
    float fatorHumidade = 0.0;
    if (humidade > 80.0) {
        fatorHumidade = -8.0;     // Reduce time on very humid days
    } else if (humidade >= 60.0 && humidade <= 80.0) {
        fatorHumidade = -6.0;     // Slightly reduce on humid days
    } else if (humidade >= 40.0 && humidade < 60.0) {
        fatorHumidade = 0.0;      // Normal conditions
    } else if (humidade >= 20.0 && humidade < 40.0) {
        fatorHumidade = 3.0;      // Increase on dry days
    } else {
        fatorHumidade = 5.0;      // Significantly increase on very dry days
    }
    
    // Calculation of the final watering time
    float tempoRega = tempoBaseRega + fatorTemperatura + fatorHumidade;
    
    // Ensure the minimum time is at least 5 minutes
    if (tempoRega < 0.0) {
        tempoRega = 0.0;
    }
    
    return (int)tempoRega;
}

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // Start HTU21D sensor
  if (!htu.begin()) {
    Serial.println("Sensor HTU21D não encontrado. Verifica a ligação!");
    while (1);  // stop if sensor is not found
  }

  Serial.println("Sensor HTU21D pronto.");
}

void loop() {
  float temperatura = htu.readTemperature();
  float humidade = htu.readHumidity();
  float minutos = calcularTempoRega(temperatura,humidade);

  float X_test[] = {temperatura, humidade, minutos };
  float prediction = model.predict(X_test);
  Serial.println(prediction);
  delay(1000);

  // Show results on Serial Monitor
  Serial.print("Temperatura: "); Serial.print(temperatura); Serial.println(" °C");
  Serial.print("Humidade: "); Serial.print(humidade); Serial.println(" %");
  Serial.print("Tempo de rega previsto: "); Serial.print(minutos); Serial.println(" minutos");
  Serial.println("------------------------------");

  delay(5000);  // Wait 5 seconds between readings





}

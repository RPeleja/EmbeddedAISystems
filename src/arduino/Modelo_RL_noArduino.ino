#include <Wire.h>
#include "Adafruit_HTU21DF.h"
#include "LinearRegressor.h"
Eloquent::ML::Port::LinearRegression model;

// Criar instância do sensor
Adafruit_HTU21DF htu = Adafruit_HTU21DF();

int calcularTempoRega(float temperatura, float umidade) {
    int tempo_rega = 10;  // Base de 10 minutos

    if (temperatura > 25) {
        tempo_rega += (int)(temperatura - 25);
    }

    if (umidade < 60) {
        tempo_rega += (int)(60 - umidade);
    }

    // Garante que o tempo está entre 5 e 30 minutos
    if (tempo_rega < 5) {
        tempo_rega = 5;
    } else if (tempo_rega > 30) {
        tempo_rega = 30;
    }

    return tempo_rega;
}

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // Iniciar sensor HTU21D
  if (!htu.begin()) {
    Serial.println("Sensor HTU21D não encontrado. Verifica a ligação!");
    while (1);  // parar se não encontrar o sensor
  }

  Serial.println("Sensor HTU21D pronto.");
}

void loop() {
  float temperatura = htu.readTemperature();
  float humidade = htu.readHumidity();

  float X_test[] = {temperatura, humidade, calcularTempoRega(temperatura,humidade) };  // insira os valores reais
  float prediction = model.predict(X_test);
  Serial.println(prediction);
  delay(1000);

  // Mostrar resultados no Serial Monitor
  Serial.print("Temperatura: "); Serial.print(temperatura); Serial.println(" °C");
  Serial.print("Humidade: "); Serial.print(humidade); Serial.println(" %");
  Serial.print("Tempo de rega previsto: "); Serial.print(minutos); Serial.println(" minutos");
  Serial.println("------------------------------");

  delay(5000);  // Espera 5 segundos entre leituras





}

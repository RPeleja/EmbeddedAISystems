#include <Wire.h>
#include "Adafruit_HTU21DF.h"

// Criar instância do sensor
Adafruit_HTU21DF htu = Adafruit_HTU21DF();

// Função do modelo de regressão linear
float preverRega(float temperatura, float humidade, float mes, float hora, float dias_desde_chuva, float ultima_rega_min) {
  return
    (temperatura * 0.0000000000001145) +
    (humidade * 40.3846154) +
    (mes * 19.3432072) +
    (hora * 18.6133422) +
    (dias_desde_chuva * 19.9818390) +
    (ultima_rega_min * -1.338681) +
    -39.4921614;
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

  // Simula valores fixos para as restantes variáveis
  float mes = 5;                  // Maio
  float hora = 14;                // 14h
  float dias_desde_chuva = 3;     // Exemplo: 3 dias
  float ultima_rega_min = 0;      // Exemplo: ainda não regou hoje

  float minutos = preverRega(temperatura, humidade, mes, hora, dias_desde_chuva, ultima_rega_min);

  // Mostrar resultados no Serial Monitor
  Serial.print("Temperatura: "); Serial.print(temperatura); Serial.println(" °C");
  Serial.print("Humidade: "); Serial.print(humidade); Serial.println(" %");
  Serial.print("Tempo de rega previsto: "); Serial.print(minutos); Serial.println(" minutos");
  Serial.println("------------------------------");

  delay(5000);  // Espera 5 segundos entre leituras
}

#include <Wire.h>
#include "Adafruit_HTU21DF.h"
#include "RandomForestRegressor.h"


// Criar instância do sensor
Adafruit_HTU21DF htu = Adafruit_HTU21DF();

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // Start HTU21D sensor
  if (!htu.begin()) {
    Serial.println("Sensor HTU21D não encontrado. Verifica a ligação!");
    while (1);
  }

  Serial.println("Sistema pronto.");
}

void loop() {
  double temperatura = htu.readTemperature();
  double humidade = htu.readHumidity();

  int ano = 2025;
  int mes = 5;
  int dia = 20;

  // Hora baseada no tempo desde o arranque
  int hora = 18;

  // Codificações cíclicas
  double dia_sin = sin(2 * PI * dia / 31.0);
  double dia_cos = cos(2 * PI * dia / 31.0);
  double mes_sin = sin(2 * PI * mes / 12.0);
  double mes_cos = cos(2 * PI * mes / 12.0);
  double hora_sin = sin(2 * PI * hora / 24.0);
  double hora_cos = cos(2 * PI * hora / 24.0);

  double X_test[] = {
    temperatura, humidade, ano,
    dia_sin, dia_cos, mes_sin, mes_cos, hora_sin, hora_cos
  };

  double prediction = score(X_test);
  if (prediction < 0) prediction = 0;  // Opcional: evita valores negativos

  Serial.print("Temperatura: "); Serial.print(temperatura); Serial.println(" °C");
  Serial.print("Humidade: "); Serial.print(humidade); Serial.println(" %");
  Serial.print("Tempo de rega previsto: "); Serial.print(prediction); Serial.println(" minutos");
  Serial.println("------------------------------");

  delay(5000);
}

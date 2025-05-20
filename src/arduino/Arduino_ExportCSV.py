import serial
import csv
import time
import os
from datetime import datetime

# CONFIGURATIONS
porta = 'COM5'
baud_rate = 9600
nome_arquivo = 'C:/temp/dados_arduino.csv'

# CONFIGURABLE VARIABLES
dias_desde_chuva = 3
rega_padrao_min = 10
humidade_limite = 40

# ENSURE THE FOLDER EXISTS
pasta = os.path.dirname(nome_arquivo)
if not os.path.exists(pasta):
    os.makedirs(pasta)

# Function for dynamic irrigation time calculation
def calcular_tempo_rega(temperatura, humidade):
    tempo = 10 
    if temperatura > 25:
        tempo += int(temperatura - 25)
    if humidade < 60:
        tempo += int(60 - humidade)
    tempo = max(5, min(tempo, 30))
    return tempo

# CONNECT TO SERIAL PORT
try:
    ser = serial.Serial(porta, baud_rate, timeout=2)
    time.sleep(2)
    ser.flushInput()
except serial.SerialException as e:
    print(f"Error opening port {porta}: {e}")
    exit()

# OPEN THE FILE AND WRITE HEADER
with open(nome_arquivo, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(['temperatura', 'humidade', 'data', 'rega_necessaria_min'])
    csvfile.flush()

    print("Reading data... Press Ctrl+C to stop.\n")

    temperatura = None
    ultima_rega = 0

    try:
        while True:
            linha = ser.readline().decode('utf-8', errors='replace').strip()
            print("Received:", repr(linha))

            if linha.startswith("Temperatura:"):
                try:
                    temperatura = float(linha.split(":")[1].replace("°C", "").strip())
                except ValueError:
                    temperatura = None

            elif linha.startswith("Humidade:") and temperatura is not None:
                try:
                    humidade = float(linha.split(":")[1].replace("%", "").strip())
                    data = datetime.now()

                    # Irrigation time calculation based on the function
                    tempo_rega = calcular_tempo_rega(temperatura, humidade)

                    if humidade < humidade_limite:
                        ultima_rega = tempo_rega
                        print(f"Irrigation calculation: {tempo_rega} minutes\n")
                    else:
                        tempo_rega = 0 
                        print(f"Irrigation calculation: {tempo_rega} minutes\n")

                    # Write data to CSV, including irrigation time
                    writer.writerow([
                        round(temperatura, 1),
                        round(humidade, 1),
                        data,
                        tempo_rega
                    ])
                    csvfile.flush()

                    print(f"Saved: {temperatura},{humidade},{data},{tempo_rega} minutes\n")
                except ValueError:
                    print("Error converting humidity.")
    except KeyboardInterrupt:
        print("\nInterrupted. CSV file saved and serial port closed.")

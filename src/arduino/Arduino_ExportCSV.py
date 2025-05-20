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
    """
    Calculates the required irrigation time in minutes based on temperature and humidity.
    
    Parameters:
    temperatura (float): Ambient temperature in degrees Celsius (°C)
    humidade (float): Air humidity percentage (0-100)
    
    Returns:
    float: Recommended irrigation time in minutes
    """
    # Set base values and limits
    tempo_base_rega = 1  # watering minutes in normal conditions
    
    # Adjustment based on temperature
    # The higher the temperature, the longer the watering time
    fator_temperatura = 0
    if temperatura < 15:
        fator_temperatura = -2  # Reduce time on cold days
    elif 15 <= temperatura < 25:
        fator_temperatura = 0   # Normal conditions
    elif 25 <= temperatura < 30:
        fator_temperatura = 3   # Increase a bit on hot days
    elif 30 <= temperatura < 35:
        fator_temperatura = 5   # Increase more on very hot days
    elif 35 <= temperatura < 40:
        fator_temperatura = 15   # Increase more on very hot days
    else:
        fator_temperatura = 48   # Significantly increase on extremely hot days
    
    # Adjustment based on humidity
    # The lower the humidity, the longer the watering time
    fator_humidade = 0
    if humidade > 80:
        fator_humidade = -8     # Reduce time on very humid days
    elif 60 <= humidade <= 80:
        fator_humidade = -6     # Slightly reduce on humid days
    elif 40 <= humidade < 60:
        fator_humidade = 0      # Normal conditions
    elif 20 <= humidade < 40:
        fator_humidade = 3      # Increase on dry days
    else:
        fator_humidade = 5      # Significantly increase on very dry days
    
    # Calculation of the final irrigation time
    tempo_rega = tempo_base_rega + fator_temperatura + fator_humidade
    
    # Ensure the minimum time is at least 0 minutes
    if tempo_rega < 0:
        tempo_rega = 0
    
    return tempo_rega

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

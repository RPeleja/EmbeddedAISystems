import serial
import csv
import time
import os
from datetime import datetime

# CONFIGURAÇÕES
porta = 'COM5'  # Altere conforme necessário
baud_rate = 9600
nome_arquivo = 'C:/temp/dados_arduino.csv'

# VARIÁVEIS CONFIGURÁVEIS
dias_desde_chuva = 3
rega_padrao_min = 10
umidade_limite = 40

# GARANTIR QUE A PASTA EXISTE
pasta = os.path.dirname(nome_arquivo)
if not os.path.exists(pasta):
    os.makedirs(pasta)

# Função para cálculo dinâmico de tempo de rega
def calcular_tempo_rega(temperatura, umidade):
    tempo = 10  # Base de 10 minutos
    if temperatura > 25:
        tempo += int(temperatura - 25)
    if umidade < 60:
        tempo += int(60 - umidade)
    tempo = max(5, min(tempo, 30))
    return tempo

# CONECTAR À PORTA SERIAL
try:
    ser = serial.Serial(porta, baud_rate, timeout=2)
    time.sleep(2)
    ser.flushInput()
except serial.SerialException as e:
    print(f"Erro ao abrir a porta {porta}: {e}")
    exit()

# ABRIR O FICHEIRO E ESCREVER CABEÇALHO
with open(nome_arquivo, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(['temperatura', 'humidade', 'data', 'rega_necessaria_min'])
    csvfile.flush()

    print("A ler dados... Pressione Ctrl+C para parar.\n")

    temperatura = None
    ultima_rega = 0

    try:
        while True:
            linha = ser.readline().decode('utf-8', errors='replace').strip()
            print("Recebido:", repr(linha))

            if linha.startswith("Temperatura:"):
                try:
                    temperatura = float(linha.split(":")[1].replace("°C", "").strip())
                except ValueError:
                    temperatura = None

            elif linha.startswith("Umidade:") and temperatura is not None:
                try:
                    umidade = float(linha.split(":")[1].replace("%", "").strip())
                    data = datetime.now()

                    # Cálculo do tempo de rega com base na função
                    tempo_rega = calcular_tempo_rega(temperatura, umidade)

                    if umidade < umidade_limite:
                        ultima_rega = tempo_rega
                        print(f"Rega necessária: {tempo_rega} minutos\n")
                    else:
                        tempo_rega = 0  # Sem rega se a umidade está OK
                        print("Sem necessidade de rega\n")

                    # Grava dados no CSV, incluindo o tempo de rega
                    writer.writerow([
                        round(temperatura, 1),
                        round(umidade, 1),
                        data,
                        tempo_rega
                    ])
                    csvfile.flush()

                    print(f"Gravado: {temperatura},{umidade},{data},{tempo_rega} minutos\n")
                except ValueError:
                    print("Erro ao converter umidade.")
    except KeyboardInterrupt:
        print("\nInterrupção. Ficheiro CSV salvo e porta serial fechada.")

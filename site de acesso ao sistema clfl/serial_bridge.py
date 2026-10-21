import json
import time
import requests
import serial

# IMPORTANTE: Coloque aqui a porta COM em que o seu ESP32 está plugado (ex: COM3, COM4...)
# No Windows você confere no Gerenciador de Dispositivos. No Linux/Mac costuma ser '/dev/ttyUSB0'
PORTA_SERIAL = 'COM6'
VELOCIDADE = 115200
URL_FLASK = 'http://127.0.0.1:5000/dados'

print(f'Conectando à porta serial {PORTA_SERIAL}...')
try:
  conexao = serial.Serial(PORTA_SERIAL, VELOCIDADE, timeout=1)
  time.sleep(2)
  print('Conectado com sucesso! Ouvindo o ESP32 via cabo USB...')
except Exception as e:
  print(f'Erro ao abrir porta serial: {e}')
  print('Verifique se a porta COM está correta ou se o Monitor Serial está fechado.')
  exit()

while True:
  try:
    if conexao.in_waiting > 0:
      linha = conexao.readline().decode('utf-8').strip()

      # Se a linha recebida for um JSON enviado pelo ESP32
      if linha.startswith('{') and linha.endswith('}'):
        dados = json.loads(linha)
        print(f'Recebido do ESP32 e enviado ao Flask -> {dados}')

        # Dispara um POST local para o seu Flask (que processa e salva no banco)
        resposta = requests.post(URL_FLASK, json=dados)
        print(f'Status do Servidor: {resposta.status_code}\n')

  except KeyboardInterrupt:
    print('Encerrando bridge serial...')
    break
  except Exception as e:
    print(f'Erro no processamento: {e}')
  time.sleep(0.1)
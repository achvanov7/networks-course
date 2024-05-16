import PySimpleGUI as gui
from utils import *
import socket
from datetime import datetime

window = gui.Window('Отправитель TCP', [
  [gui.Text('Введите IP адрес получателя', size=GUI_TEXT_SIZE), gui.InputText(DEFAULT_HOST, key='host')],
  [gui.Text('Введите порт отправки', size=GUI_TEXT_SIZE), gui.InputText(DEFAULT_PORT, key='port')],
  [gui.Text('Введите количество пакетов для отправки', size=GUI_TEXT_SIZE), gui.InputText(DEFAULT_PACKETS_NUMBER, key='npackets')],
  [gui.Button('Отправить')]
])

while True:
  event, values = window.read()
  if event is None or event == 'Exit':
    break

  if event != 'Отправить':
    continue

  host = values['host']
  port = int(values['port'])
  npackets = int(values['npackets'])

  try:
    cur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cur_socket.connect((host, port))
    cur_socket.sendall(str(npackets).encode())

    for i in range(npackets):
      msg = str(datetime.now().timestamp()) + ' '
      msg += random_string(PACKET_SIZE - len(msg))
      cur_socket.sendto(msg.encode(), (host, port))
  except Exception as e:
    print(e)
  finally:
    cur_socket.close()
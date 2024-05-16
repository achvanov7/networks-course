import PySimpleGUI as gui
from utils import *
import socket
from datetime import datetime

window = gui.Window('Отправитель UDP', [
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
    cur_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cur_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    cur_socket.settimeout(1)
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((host, port))
    tcp_socket.sendall(str(npackets).encode())

    for i in range(npackets):
      msg = str(datetime.now().timestamp()) + ' '
      msg += random_string(PACKET_SIZE - len(msg))
      cur_socket.sendto(msg.encode(), (host, port))
  except Exception as e:
    print(e)
  finally:
    cur_socket.close()
    tcp_socket.close()
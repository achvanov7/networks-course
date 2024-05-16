import PySimpleGUI as gui
from utils import *
import socket
from datetime import datetime

window = gui.Window('Получатель UDP', [
  [gui.Text('Введите IP', size=GUI_TEXT_SIZE), gui.InputText(DEFAULT_HOST, key='host')],
  [gui.Text('Введите порт для получения', size=GUI_TEXT_SIZE), gui.InputText(DEFAULT_PORT, key='port')],
  [gui.Text('Скорость передачи', size=GUI_TEXT_SIZE), gui.Text(key='speed')],
  [gui.Text('Число полученных пакетов', size=GUI_TEXT_SIZE), gui.Text(key='packets_rcv')],
  [gui.Button('Получить')]
])

while True:
  event, values = window.read(1000)
  if event is None or event == 'Exit':
    break

  if event != 'Получить':
    continue

  host = values['host']
  port = int(values['port'])

  tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  tcp_socket.bind((host, port))
  tcp_socket.listen(1)

  packets_rcv = 0
  time_diff = 0
  npackets = 0

  try:
    rcv_socket, _ = tcp_socket.accept()
    npackets = int(rcv_socket.recv(PACKET_SIZE).decode())
  except Exception as e:
    print(e)
  finally:
    rcv_socket.close()
    tcp_socket.close()

  print("kek")

  try:
    cur_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cur_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    cur_socket.settimeout(1)
    cur_socket.bind((host, port))

    for i in range(npackets):
      try:
        msg, _ = cur_socket.recvfrom(PACKET_SIZE)
        msg = msg.decode()
        time, rand_string = msg.split(' ')
        time = float(time)
        packets_rcv += 1
        cur_time = datetime.now().timestamp()
        time_diff += cur_time - time
      except socket.timeout:
        pass
  except Exception as e:
    print(e)
  finally:
    speed = 0
    if time_diff != 0:
      speed = (PACKET_SIZE * packets_rcv) / time_diff / 1000
    window['speed'].Update(f'{round(speed, 2)} KB/S')
    window['packets_rcv'].Update(f'{packets_rcv} of {npackets}')

    cur_socket.close()


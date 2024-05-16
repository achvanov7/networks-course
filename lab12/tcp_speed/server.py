import PySimpleGUI as gui
from utils import *
import socket
from datetime import datetime

window = gui.Window('Получатель TCP', [
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

  cur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  cur_socket.bind((host, port))
  cur_socket.listen(1)

  packets_rcv = 0
  time_diff = 0
  npackets = 0

  try:
    rcv_socket, _ = cur_socket.accept()
    npackets = int(rcv_socket.recv(PACKET_SIZE).decode())
    for i in range(npackets):
      try:
        msg = rcv_socket.recv(PACKET_SIZE).decode()
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
    rcv_socket.close()
  
  speed = 0
  if time_diff != 0:
    speed = (PACKET_SIZE * packets_rcv) / time_diff / 1000
  window['speed'].Update(f'{round(speed, 2)} KB/S')
  window['packets_rcv'].Update(f'{packets_rcv} of {npackets}')

  cur_socket.close()


import socket
from datetime import datetime
from time import sleep

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
port = 8080

while True:
  message = datetime.now().strftime("%H:%M:%S").encode()
  server_socket.sendto(message, ('<broadcast>', port))
  sleep(1)
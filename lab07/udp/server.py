from socket import *
import random

server_socket = socket(AF_INET, SOCK_DGRAM)
port = 8080
server_socket.bind(('', port))

while True:
  msg, addr = server_socket.recvfrom(1024)
  msg = msg.upper()
  if random.randint(0, 9) < 8:
    server_socket.sendto(msg, addr)
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
port = 8080
client_socket.bind(('', port))

while True:
  time, _ = client_socket.recvfrom(1024)
  print("Current time:", time.decode())
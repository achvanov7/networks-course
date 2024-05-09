import socket

host = 'localhost'
port = 8080

client_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
client_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)

client_socket.connect((host, port))

while True:
  msg = input('Enter your message: ')
  client_socket.sendall(msg.encode())

  response = client_socket.recv(1024)
  print('Response from the server: ', response.decode())
from stop_and_wait import smart_socket

addr = "127.0.0.1"
server_port = 8000
client_port = 8080

server_socket = smart_socket(addr, server_port)
server_socket.connect(addr, client_port)
server_socket.settimeout(1000)

with open('big_text_received.txt', '+wb') as file:
  file.write(server_socket.recvall())
  file.close()

server_socket.settimeout(1)
with open('big_text_received.txt', 'rb') as file:
  server_socket.sendall(file.read())
  file.close()
from stop_and_wait import smart_socket

addr = "127.0.0.1"
server_port = 8000
client_port = 8080

client_socket = smart_socket(addr, client_port)
client_socket.connect(addr, server_port)
client_socket.settimeout(1)

with open('big_text.txt', 'rb') as file:
  client_socket.sendall(file.read())
  file.close()

client_socket.settimeout(1000)
with open('big_text.txt', 'wb') as file:
  file.write(client_socket.recvall())
  file.close()
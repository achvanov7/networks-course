import socket 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 8080
client_socket.connect(('', port))

comm = input()
client_socket.send(comm.encode())

while True:
  response = client_socket.recv(1024).decode()
  print(response)
  if response == 'Done!':
    break

client_socket.close()

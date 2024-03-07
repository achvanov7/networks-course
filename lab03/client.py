import socket
import sys

server_host = sys.argv[1]
server_port = int(sys.argv[2])
filename = sys.argv[3]

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))
client_socket.send(f'GET /{filename} HTTP/1.1'.encode())

data = client_socket.recv(1024)
print(data.decode())

client_socket.close()

import socket
import sys
import os
from concurrent.futures import ThreadPoolExecutor

def find_file(conn, addr):
  data = conn.recv(1024)
  if data is None:
    conn.send('HTTP/1.1 500 Bad Request\r\n'.encode())
    conn.close()
  file_path = data.decode().split()[1][1:]
  if os.path.isfile(file_path):
    print("200 OK")
    file = open(file_path, "rb")
    file_content = file.read()
    conn.sendall(f'HTTP/1.1 200 OK\r\nContent-length: {os.path.getsize(file_path)}\r\nContent-Type: text/html\r\n\r\n'.encode())
    conn.sendall(file_content)
    file.close()
  else:
    print("404 Not Found")
    conn.send('HTTP/1.1 404 Not Found\r\n'.encode())
  conn.close()

def main():
  port = int(sys.argv[1])
  
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.bind(('', port))
  server_socket.listen()

  pool = ThreadPoolExecutor(max_workers=int(sys.argv[2]))
  
  while True:
    conn, addr = server_socket.accept()
    pool.submit(find_file, conn, addr)

if __name__ == '__main__':
  main()
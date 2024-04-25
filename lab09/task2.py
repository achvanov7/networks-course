import sys
from socket import *

host = sys.argv[1]
lport = int(sys.argv[2])
rport = int(sys.argv[3])

for port in range(lport, rport + 1):
  tmp_socket = socket(AF_INET, SOCK_STREAM)
  tmp_socket.settimeout(1)
  if tmp_socket.connect_ex((host, port)) == 0:
    print(port)
  tmp_socket.close()
from socket import *
from datetime import datetime
import time
import numpy as np

client_socket = socket(AF_INET, SOCK_DGRAM)
host = "127.0.0.1"
port = 8080
client_socket.settimeout(1.0)

lost = 0
rtts = []
n = 10

for i in range(1, n + 1):
  msg = 'Ping ' + str(i) + ' ' + datetime.now().strftime("%H:%M:%S")
  try:
    sent = datetime.now()
    client_socket.sendto(msg.encode(), (host, port))
    ans = client_socket.recv(1024)
    recieved = datetime.now()
    rtt = (recieved - sent).total_seconds() * 1000
    rtt = round(rtt, 3)
    rtts.append(rtt)
    print(ans.decode())
    print(f"RTT: {rtt} ms")
  except:
    print("Request timed out")
    lost += 1
  time.sleep(0.2)

print('--- Statistics ---')
print(f'{n} packets transmitted, {n - lost} packets received, {lost / n * 100}% packet loss')
print(f'round-trip min/avg/max/stddev = {min(rtts)}/{round(np.average(rtts), 3)}/{max(rtts)}/{round(np.std(rtts), 3)} ms')
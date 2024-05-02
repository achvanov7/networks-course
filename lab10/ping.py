from socket import *
import time
from datetime import datetime
import sys
import struct
import numpy as np

ICMP_CODE = getprotobyname('icmp')
ICMP_ECHO_REQUEST = 8

def checksum(data):
  sum = 0
  for i in range(0, len(data), 2):
    if i + 1 < len(data):
      sum += (data[i + 1] << 8) + data[i]
    else:
      sum += data[i]
  sum &= 0xffffffff
  sum = (sum >> 16) + (sum & 0xffff)
  sum += (sum >> 16)
  answer = ~sum
  answer &= 0xffff
  answer = answer >> 8 | (answer << 8 & 0xff00)
  return answer

def create_packet(id):
  header = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, 0, 0, id, 1)
  data = b'42'
  header = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, 0, checksum(header + data), id, 1)
  return header + data

def ping(addr, id):
  try:
    cur_socket = socket(AF_INET, SOCK_RAW, ICMP_CODE)
    packet = create_packet(id)
    start = datetime.now()
    cur_socket.settimeout(1)
    cur_socket.sendto(packet, (addr, 0))
    rec, _ = cur_socket.recvfrom(1024)
    rtt = (datetime.now() - start).total_seconds() * 1000
    rtt = round(rtt, 3)
    cur_socket.close()
    print(f'Ping to {addr} number {id}. {len(rec)} bytes, RTT: {rtt} ms')
    return rtt
  except timeout:
    print(f'Ping to {addr} number {id} timed out')
    return None

n = int(sys.argv[1])
addr = sys.argv[2]

lost = 0
rtts = []

for i in range(1, n + 1):
  rtt = ping(addr, i)
  if rtt == None:
    lost += 1
  else:
    rtts.append(rtt)
  time.sleep(1)

print('--- Statistics ---')
print(f'{n} packets transmitted, {n - lost} packets received, {lost / n * 100}% packet loss')
if lost < n:
  print(f'round-trip min/avg/max/stddev = {min(rtts)}/{round(np.average(rtts), 3)}/{max(rtts)}/{round(np.std(rtts), 3)} ms')

from checksum import calc, check
from socket import *
from random import randint

class smart_socket:
  def __init__(self, addr, port) -> None:
    self._socket = socket(AF_INET, SOCK_DGRAM)
    self._socket.bind((addr, port))
    self._packet_size = 256
    self._checksum_bytes = 2
    self._num_bytes = 1
    self._num = 0
    self._last_num = -1

  def connect(self, addr, port) -> None:
    self._addr = (addr, port)
    self._socket.connect(self._addr)

  def settimeout(self, time) -> None:
    self._socket.settimeout(time)

  def _make_pkt(self, data, num):
    msg = int.to_bytes(num, self._num_bytes) + data
    return int.to_bytes(calc(msg), self._checksum_bytes) + msg

  def recv(self) -> bytes:
    print(f'Receiving packet {self._num}')
    while True:
      try:
        msg, addr = self._socket.recvfrom(1024)
        if randint(1, 10) <= 3:
          raise timeout
      except timeout:
        print('Timeout')
        continue
      
      if not check(msg, 0):
        print('Wrong checksum')
        continue

      if len(msg) < self._checksum_bytes + self._num_bytes:
        print('Wrong data length')
        continue
      
      num = int.from_bytes(msg[self._checksum_bytes : self._checksum_bytes + self._num_bytes])

      if num == self._last_num:
        self._socket.send(self._make_pkt(bytes(), num))
        print('Confirmation packet was lost')
        continue

      if num != self._num:
        print('Wrong ACK number')
        continue
      
      self._socket.send(self._make_pkt(bytes(), num))
      self._last_num = num
      self._num ^= 1

      print('Packet received successfully')
      return msg[self._checksum_bytes + self._num_bytes : ]
    
  def recvall(self) -> bytes:
    msg = bytes()

    while True:
      packet = self.recv()
      msg += packet
      if len(packet) < self._packet_size:
        break
    
    self._num = 0
    print('Whole message received successfully')

    return msg
  
  def send(self, msg) -> None:
    print(f'Sending packet {self._num}')
    while True:
      self._socket.send(self._make_pkt(msg, self._num))

      try:
        msg, addr = self._socket.recvfrom(1024)
        if randint(1, 10) <= 3:
          raise timeout
      except timeout:
        print('Timeout')
        continue

      if len(msg) != self._checksum_bytes + self._num_bytes:
        print('Wrong data length')
        continue

      if not check(msg, 0):
        print('Wrong checksum')
        continue

      num = int.from_bytes(msg[self._checksum_bytes : self._checksum_bytes + self._num_bytes])

      if num != self._num:
        print('Wrong ACK number')
        continue
      
      break

    self._num ^= 1
    print('Packet sent successfully')

  def sendall(self, msg) -> None:
    size = len(msg)
    pkt_cnt = (size + self._packet_size - 1) // self._packet_size

    for i in range(pkt_cnt):
      packet = msg[i * self._packet_size : min(size, (i + 1) * self._packet_size)]
      self.send(packet)
    
    self._num = 0
    print('Whole message sent successfully')










      

      

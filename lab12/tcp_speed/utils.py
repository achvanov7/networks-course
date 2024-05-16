from random import choice
from string import ascii_lowercase

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8080
DEFAULT_PACKETS_NUMBER = 5
PACKET_SIZE = 1024
GUI_TEXT_SIZE = (50, 2)

def random_string(n):
  str = ''
  for i in range(n):
    str += choice(ascii_lowercase)
  return str
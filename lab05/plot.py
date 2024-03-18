import matplotlib.pyplot as plt
import numpy as np

F = 15 * (1000 ** 2)
us = 30 * 1000
d = 2 * 1000
N = 1000

def client_server(u):
  return max(N * F / us, F / d)

def peer_to_peer(u):
  return max(F / us, F / d, N * F / (us + N * u))

u = np.linspace(100, 2500, 24)
y1 = np.array([client_server(x) for x in u])
y2 = np.array([peer_to_peer(x) for x in u])

plt.plot(u, y1, label = 'client-server')
plt.plot(u, y2, label = 'peer to peer')
plt.title("N = 1000")
plt.xlabel("u, Kbit/s")
plt.ylabel("time, seconds")
plt.legend()
plt.show()
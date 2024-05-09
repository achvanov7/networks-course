import socket

port = 8080

server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM) 
server.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)

server.bind(('', port))    
server.listen()

while True:
    conn, addr = server.accept()
    msg = conn.recv(1024).decode()
    conn.sendall(msg.upper().encode())
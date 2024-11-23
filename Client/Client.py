# Runs on Pc, directly from Thonny
# The client

import socket
s = socket. socket()
host = '192.168.2.33'# ip of raspberry pi, running the server
port = 5000
s.connect((host, port))
message = s.recv(1024).decode()
print(message)
s.close()


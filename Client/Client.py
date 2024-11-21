# Runs on Pc, directly from Thonny
# The client

import socket
s = socket. socket()
host = '10.102.13.62'# ip of raspberry pi, running the server
port = 5000
s.connect((host, port))
message = s.recv(1024).decode()
print(message)
s.close()


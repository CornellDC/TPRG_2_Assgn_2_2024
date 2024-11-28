# Runs on Pc, directly from Thonny
# The client

import socket
s = socket.socket()
host = '10.102.13.55'# ip of raspberry pi, running the server
port = 5000
s.connect((host, port))
message = s.recv(1024).decode()
# print(message)

f_dict = eval(message)  # The eval() function evaluates JavaScript code represented as a string and returns its completion value.

# Print each key and value pair to the shell.
for key, value in f_dict.items(): # https://stackoverflow.com/a/5905166
    print(f'{key} = {value}')

s.close()
'''
TPRG 2131 Fall 2024 Assignment 2 - Client.py
November 28th, 2024
Cornell Falconer-Lawson <Cornell.FalconerLawson@dcmail.ca>

This program is strictly my own work. Any material
beyond course learning materials that is taken from
the Web or other sources is properly cited, giving
credit to the original author(s).

Runs on Pc, directly from Thonny
The client: This will receive information from the server, process and output it to console.
'''
import json
import socket
s = socket.socket()
host = '10.102.13.55'# ip of raspberry pi, running the server
port = 5000
s.connect((host, port))
message = s.recv(1024).decode()
# print(message)

f_dict = json.loads(message)  # Converts the received Json into a python dict.
# print(json.dumps(f_dict))
# Print each key and value pair to the shell.
for key, value in f_dict.items(): # https://stackoverflow.com/a/5905166
    print(f'{key} = {value}')

s.close()
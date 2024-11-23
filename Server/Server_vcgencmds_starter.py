# This server runs on Pi, sends Pi's your 4 arguments from the vcgencmds, sent as Json object.

# details of the Pi's vcgencmds - https://www.tomshardware.com/how-to/raspberry-pi-benchmark-vcgencmd
# more vcgens on Pi 4, https://forums.raspberrypi.com/viewtopic.php?t=245733
# more of these at https://www.nicm.dev/vcgencmd/

import socket
import os, time
import json

s = socket.socket()
host = '' # Localhost
port = 5000
s.bind((host, port))
s.listen(5)

def get_temp():
  """gets from the os, using vcgencmd - the core-temperature."""
  t = os.popen('/usr/bin/vcgencmd measure_temp').readline()
  formatted_temp = t.split('=')[1]
  return formatted_temp

def get_arm_clock():
  """gets from the os, using vcgencmd - the cpu clock speed."""
  clock_speed = os.popen('/usr/bin/vcgencmd measure_clock arm').readline()
  formatted_clock_speed = clock_speed.split('=')[1]
  return formatted_clock_speed

while True:
  temp = get_temp()
  clock_speed = get_arm_clock()

  # initialising json object string
  ini_string = """{"Temperature": temp,
                   "arm_clock_speed": clock_speed}"""

  # converting string to json
  f_dict = eval(
    ini_string)  # The eval() function evaluates JavaScript code represented as a string and returns its completion value.
  print(f_dict)

  c, addr = s.accept()
  print ('Got connection from',addr)
  res = bytes(str(f_dict), 'utf-8') # needs to be a byte
  c.send(res) # sends data as a byte type
  c.close()
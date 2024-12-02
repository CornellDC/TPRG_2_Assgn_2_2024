'''
TPRG 2131 Fall 2024 Assignment 2 - Server
November 28th, 2024
Cornell Falconer-Lawson <Cornell.FalconerLawson@dcmail.ca>

This program is strictly my own work. Any material
beyond course learning materials that is taken from
the Web or other sources is properly cited, giving
credit to the original author(s).

This server runs on Pi, sends Pi's your 4 arguments from the vcgencmds, sent as Json object.
'''

# details of the Pi's vcgencmds - https://www.tomshardware.com/how-to/raspberry-pi-benchmark-vcgencmd
# more vcgens on Pi 4, https://forums.raspberrypi.com/viewtopic.php?t=245733
# more of these at https://www.nicm.dev/vcgencmd/

import socket
import os, time
import json

s = socket.socket()
host = ''  # Localhost
port = 5000
s.bind((host, port))
s.listen(5)


def get_temp():
    """
  Gets from the os, using vcgencmd - the core-temperature.
  :return: Temperature in Celsius.
  """
    t = os.popen('/usr/bin/vcgencmd measure_temp').readline() #vcgencmd commands
    formatted_temp = t.split('=')[1]
    formatted_temp = formatted_temp.strip('\n') # remove new line.
    return formatted_temp

def get_mem():
    """
  Gets from the os, using vcgencmd - the installed memory on the RPi.
  :return: Total arm memory in MB.
  """
    # https://raspberrypi.stackexchange.com/questions/108993/what-exactly-does-vcgencmd-get-mem-arm-display
    mem = os.popen('/usr/bin/vcgencmd get_config total_mem').readline()
    formatted_mem = mem.split('=')[1]
    formatted_mem = formatted_mem.strip('\n') + 'MB' # remove new line.
    return formatted_mem



def get_clock(name):
    """
  Gets from the os, using vcgencmd - the specified clock speed.
  :param name: Name of the clock you want to retrieve, https://www.elinux.org/RPI_vcgencmd_usage
  :return: clock speed in Hz
  """
    clock_speed = os.popen(f'/usr/bin/vcgencmd measure_clock {name}').readline()
    formatted_clock_speed = clock_speed.split('=')[1]
    formatted_clock_speed = formatted_clock_speed.split('\n')[0] + "Hz" # remove new line.
    return formatted_clock_speed


def get_voltage():
    """
  Gets from the os, using vcgencmd - the cpu voltage.
  :return: CPU voltage in Volts.
  """
    v = os.popen('/usr/bin/vcgencmd measure_volts').readline() #vcgencmd commands
    formatted_voltage = v.split('=')[1]
    formatted_voltage = formatted_voltage.strip('\n')    # remove new line.
    formatted_voltage = formatted_voltage.split('V')[0] # remove 'V' so that it can be rounded.
    formatted_voltage = round(float(formatted_voltage), 1) # convert to float and round to 1 decimal.
    formatted_voltage = str(formatted_voltage) + 'V' # Convert back to string and add the 'V'.
    return formatted_voltage

try:
    while True:
        # Retrieve sensor values
        temp = get_temp()
        arm_clock_speed = get_clock('arm')
        core_clock_speed = get_clock('core')
        voltage = get_voltage()
        total_mem = get_mem()

        # initialising dict.
        ini_dict = {"temperature": temp, "arm_clock_speed": arm_clock_speed, "core_clock_speed": core_clock_speed,
                      "cpu_voltage": voltage, "total_memory" : total_mem}



        # converting dict to json
        f_dict = json.dumps(ini_dict)

        c, addr = s.accept()
        print('Got connection from', addr)
        res = bytes(str(f_dict), 'utf-8')  # needs to be a byte
        c.send(res)  # sends data as a byte type
        print(ini_dict)
        c.close()

except KeyboardInterrupt:
    c.close()
    print("Thank you for using my program.")
# This server runs on Pi, sends Pi's your 4 arguments from the vcgencmds, sent as Json object.

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
  gets from the os, using vcgencmd - the core-temperature.
  :return: Temperature in Celsius.
  """
    t = os.popen('/usr/bin/vcgencmd measure_temp').readline()
    formatted_temp = t.split('=')[1]
    return formatted_temp


def get_clock(name):
    """
  gets from the os, using vcgencmd - the specified clock speed.
  :param name: Name of the clock you want to retrieve, https://www.elinux.org/RPI_vcgencmd_usage
  :return: clock speed in Hz
  """
    clock_speed = os.popen(f'/usr/bin/vcgencmd measure_clock {name}').readline()
    formatted_clock_speed = clock_speed.split('=')[1]
    return formatted_clock_speed


def get_voltage():
    """
  gets from the os, using vcgencmd - the cpu voltage.
  :return: CPU voltage in Volts.
  """
    v = os.popen('/usr/bin/vcgencmd measure_volts').readline()
    formatted_voltage = v.split('=')[1]
    return formatted_voltage


while True:
    # Retrieve sensor values
    temp = get_temp()
    arm_clock_speed = get_clock('arm')
    core_clock_speed = get_clock('core')
    voltage = get_voltage()

    # initialising json object string
    ini_string = """{"temperature": temp, "arm_clock_speed": arm_clock_speed, "core_clock_speed" : core_clock_speed, "cpu_voltage" : voltage}"""

    print(ini_string)

    # converting string to json
    f_dict = eval(
        ini_string)  # The eval() function evaluates JavaScript code represented as a string and returns its completion value.
    print(f_dict)
    print(f_dict["temperature"])

    c, addr = s.accept()
    print('Got connection from', addr)
    res = bytes(str(f_dict), 'utf-8')  # needs to be a byte
    c.send(res)  # sends data as a byte type
    c.close()
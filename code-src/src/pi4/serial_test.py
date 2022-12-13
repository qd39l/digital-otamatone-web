# serial_test.py
#
# Author: Owen Deng 2022
# Description: simple script to test serial connection

import serial
import time
ser = serial.Serial(port='/dev/ttyS0', baudrate=9600, timeout=0.01)

while True:
    x=ser.readline()
    
    if x == b'':
        pass
    else:
        print(str(x, 'UTF-8'))


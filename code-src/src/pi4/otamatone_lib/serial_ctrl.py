# serial_ctrl.py
#
# Author: Owen Deng 2022

import serial

class serCtrl:
    # enforce singleton
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(serCtrl, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.ser = serial.Serial(port='/dev/ttyS0', baudrate=9600, timeout=0.500)
    
    def read_val(self, print_r=False):
        x = b''
        while x == b'':
            x = self.ser.readline()
        if print_r: print(x)

        return float(str(x, 'UTF-8').strip())

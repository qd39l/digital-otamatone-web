# digipot_controller.py
#
# Author: Owen Deng 2022
# Description: digital potentiometer controller class

import RPi.GPIO as GPIO
import board
import adafruit_ds3502
from math import floor

OCTAVE_PIN1 = 5
OCTAVE_PIN2 = 26
ON_OFF_PIN = 19

class potCtrl:

    pot_127_max = 4 * 127
    pot_01_max = pot_127_max + 1 + pot_127_max
    pot_max = pot_01_max + 1 + pot_127_max 


    # enforce singleton
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(potCtrl, cls).__new__(cls)
        return cls.instance


    def __init__(self):
        # GPIO init
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(OCTAVE_PIN1, GPIO.OUT)
        GPIO.setup(OCTAVE_PIN2, GPIO.OUT)
        GPIO.setup(ON_OFF_PIN, GPIO.OUT)
        GPIO.output(OCTAVE_PIN1, 0) # Connected between RW and RL so 0 is low resistance
                                   # need to be consistent here so 0 should be low resistance (bypassed)
        GPIO.output(OCTAVE_PIN2, 0)
        GPIO.output(ON_OFF_PIN, 0) # 0 is disconnected and 1 is connected

        # I2C init
        self.i2c = board.I2C()
        self.pots = []
        
        for i in range(4):
            self.pots.append(adafruit_ds3502.DS3502(self.i2c, 40+i))
            self.pots[i].wiper = 127 # maxout wiper val in init

        # class invariant
        self.state = [0, 127, 127, 127, 127, 0]


    def __str__(self):
        return ", ".join(str(x) for x in self.state)


    def __set_pots(self, config: list):
        if config[0] != self.state[0]:
            if config[0] == 1:
                GPIO.output(OCTAVE_PIN1, 1)
            else:
                GPIO.output(OCTAVE_PIN1, 0)
            self.state[0] = config[0]
        
        if config[5] != self.state[5]:
            if config[5] == 1:
                GPIO.output(OCTAVE_PIN2, 1)
            else:
                GPIO.output(OCTAVE_PIN2, 0)
            self.state[5] = config[5]

        for i in range(1, 5):
            if config[i] < 0 or config[i] > 127:
                self.sound_off()
                raise Exception(f"config illegal input at pos {i}. {config[i]} is not within [0, 127]. config = {config}")
            if config[i] != self.state[i]:
                self.pots[i-1].wiper = config[i]
                self.state[i] = config[i]


    # a lower pot_val corresponds to a lower pitch (higher resistance)
    def set_pots(self, pot_val: int):
        if pot_val < 0 or pot_val > (self.pot_max):
            self.sound_off()
            raise Exception(f"pot_val illegal input ({pot_val}). Have to be between 0 and {self.pot_max}")

        # generate config of form (x, x, x, x, x)
        res = []
        append_last = 0
        if pot_val >= self.pot_01_max + 1:
            res.append(1)
            append_last = 1
            pot_val -= self.pot_01_max + 1
        elif pot_val >= self.pot_127_max + 1:
            res.append(1)
            append_last = 0
            pot_val -= self.pot_127_max + 1
        else:
            res.append(0)
            append_last = 0

        for i in range(1, 5):
            res.append(floor(pot_val/4))
        
        pot_val -= floor(pot_val/4) * 4

        for i in range(1, 5):
            if (pot_val == 0):
                break
            if pot_val + res[i] > 127:
                tmp = res[i]
                res[i] = 127
                pot_val -= 127 - tmp
            else:
                res[i] += pot_val
                pot_val -= pot_val
        
        assert(pot_val == 0)

        res.append(append_last)

        self.__set_pots(res)


    def sound_on(self):
        GPIO.output(ON_OFF_PIN, 1)


    def sound_off(self):
        GPIO.output(ON_OFF_PIN, 0)


    def power_off(self):
        GPIO.output(ON_OFF_PIN, 0)
        GPIO.output(OCTAVE_PIN1, 0)
        GPIO.output(OCTAVE_PIN2, 0)
        self.state[5] = 0
        self.state[0] = 0

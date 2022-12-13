# multi_pot_test.py
#
# Author: Owen Deng 2022
# Description: test the connection with multiple digital potentiometers

from time import sleep
import board
import busio
import adafruit_ds3502

i2c = busio.I2C(board.SCL, board.SDA)

ds35021 = adafruit_ds3502.DS3502(i2c, 40)
ds35022 = adafruit_ds3502.DS3502(i2c, 41)
ds35023 = adafruit_ds3502.DS3502(i2c, 42)
ds35024 = adafruit_ds3502.DS3502(i2c, 43)

wiper_val=0

ds35021.wiper=wiper_val
ds35022.wiper=wiper_val
ds35023.wiper=wiper_val
ds35024.wiper=wiper_val

while True:
    pass

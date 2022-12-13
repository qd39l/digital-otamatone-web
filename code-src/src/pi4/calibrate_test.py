# calibrate_test.py
#
# Author: Owen Deng 2022
# Description: test the calibration function

from otamatone_lib.digital_otamatone import digitalOtamatone
from time import sleep

controller = digitalOtamatone()
controller.sound_on()
sleep(0.1)
controller.sound_off()

controller.calibrate(steps=20, skip_check=True)

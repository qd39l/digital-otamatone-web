# single_pot_test.py
#
# Author: Owen Deng 2022
# Description: test script for the potCtrl class

from otamatone_lib.digipot_controller import potCtrl

controller = potCtrl()
controller.set_pots(303)
controller.sound_on()

# power_off_test.py
#
# Author: Owen Deng 2022
# Description: Power off the relays. This is handy when there's an exception

from otamatone_lib.digipot_controller import potCtrl

controller = potCtrl()
controller.power_off()

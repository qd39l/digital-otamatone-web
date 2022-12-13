# relay_test.py
#
# Author: Owen Deng 2022
# Description: handy script used to match relay-controlled resistors

from otamatone_lib.digipot_controller import potCtrl
from time import sleep

if __name__ == "__main__":
    pot_controller = potCtrl()
    print(pot_controller.pot_max)

    for _ in range(1):
        for x in [
                #   pot_controller.pot_127_max,
                  pot_controller.pot_01_max,
                 ]:

            for i in range(0, 2):
                pot_controller.set_pots(x+i)
                print(f"{x+i}, {pot_controller}")
                pot_controller.sound_on()
                sleep(0.3)
                pot_controller.sound_off()
                sleep(1)

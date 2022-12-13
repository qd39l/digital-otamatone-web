# linear_approximator.py
#
# Author: Owen Deng 2022
# Description: helper class to do the linear interpolation for pot_val

from otamatone_lib.tone_mapping import tone_map
from otamatone_lib.digipot_controller import potCtrl

class LinApprox():
    def __init__(self, max, min, steps):
        self.slope = (max - min) / steps
        self.offset = max - self.slope * steps

    def find_step_setting(self, desired_freq):
        return (desired_freq - self.offset)/self.slope

    def find_tone_setting(self, tone, verbose = False):
        if tone not in tone_map.keys():
            return None
        out = self.find_step_setting(tone_map[tone])

        if out > potCtrl.pot_max:
            out = potCtrl.pot_max
        if out < 0:
            out = 0
        if (verbose == True):
            print(out)
        return int(out)

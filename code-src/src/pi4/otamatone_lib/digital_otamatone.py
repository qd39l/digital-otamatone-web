# digital_otamatone.py
#
# Author: Owen Deng 2022
# Description: this singleton class provides a simple API to interact with the hardware system

from otamatone_lib.digipot_controller import potCtrl
from otamatone_lib.serial_ctrl import serCtrl
from otamatone_lib.tone_mapping import tone_map
from otamatone_lib.linear_approximator import LinApprox
from time import sleep
from statistics import mean 
from os.path import exists
import json

pctrl = potCtrl()
sctrl = serCtrl()
CALIBRATION_SAMPLES = 3
CALIBRATION_TOLERANCE = 0.05
factor_lo = 1 - CALIBRATION_TOLERANCE/2
factor_hi = 1 + CALIBRATION_TOLERANCE/2
CONFIG_DIRECTORY = "./config/calibration.json"
CONFIG_BACKUP = "./config/calibration_backup.json"
LOG_HDR = "[Calibration]"

class digitalOtamatone:
    # enforce singleton
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(digitalOtamatone, cls).__new__(cls)
        return cls.instance


    def __init__(self):
        self.cal_data = None
        self.note2pot = {}
        self.max_note = None
        self.min_note = None
        self.max_freq = None
        self.min_freq = None

        try:        
            self.__get_min_max__()
            print(f"[INIT] (min, max) freq: ({self.min_freq}, {self.max_freq}) | (min, max) notes: ({self.min_note}, {self.max_note})")

            self.__note2pot__()
            print(f"[INIT] note to pot mapping complete")
        except:
            print(f"[INIT] Calibration broken. restore from backup")
            self.restore_calibration()
            self.__get_min_max__()
            self.__note2pot__()


    def __str__(self):
        return str(pctrl)

    # generate note to pot_val mapping and store in self.note2pot
    def __note2pot__(self):
        tone_map_keys = list(tone_map.keys())
        tone_map_vals = [tone_map[x] for x in tone_map_keys]
        avgs = self.cal_data["avgs"]
        steps = self.cal_data["steps"]
        lo = tone_map_keys.index(self.min_note)
        hi = tone_map_keys.index(self.max_note)

        for i in range(lo, hi+1):
            target_note = tone_map_keys[i]
            target_freq = tone_map_vals[i]

            for j in range(len(avgs)-1):
                if avgs[j] <= target_freq and avgs[j+1] >= target_freq:
                    low_mount_idx = j
                    low_mount_freq = self.cal_data["avgs"][j]
                    high_mount_idx = j+1
                    high_mount_freq = self.cal_data["avgs"][j+1]
            
            lin_approx = LinApprox(high_mount_freq, low_mount_freq, steps[high_mount_idx]-steps[low_mount_idx])
            self.note2pot[tone_map_keys[i]] = lin_approx.find_tone_setting(tone_map_keys[i]) + steps[low_mount_idx]


    def __get_min_max__(self):
        if not exists(CONFIG_DIRECTORY):
            print("[INIT] No calibration file found. Calibrate now.")
            self.calibrate()

        with open(CONFIG_DIRECTORY, "r") as in_f:
            self.cal_data = json.load(in_f)
        
        # find out max and min notes
        avgs = self.cal_data["avgs"]
        self.max_freq = max(avgs)
        self.min_freq = min(avgs)
        keys = list(tone_map.keys())
        for i in range(len(keys)):
            if (tone_map[keys[i]] < self.min_freq):
                continue
            self.min_note = keys[i]
            break
        
        for i in range(len(keys)):
            if (tone_map[keys[i]] > self.max_freq):
                break
            self.max_note = keys[i]
            

    def restore_calibration(self):
        with open(CONFIG_BACKUP, "r") as in_f:
            backup_data = json.load(in_f)
        with open(CONFIG_DIRECTORY, "w") as out_f:
            json.dump(backup_data, out_f)


    # calibrate the otamatone
    # There's probably a better way to do this but we were running out of time for the demo :)
    def calibrate(self, steps=20, skip_check=False):
        assert steps >= 3

        pot_config = {}
        avgs = []

        sweep_steps = [x for x in range(0, pctrl.pot_max, int(pctrl.pot_max / steps))]
        if not (pctrl.pot_max in sweep_steps): sweep_steps.append(pctrl.pot_max)

        for pot_val in sweep_steps:
            print(f"{LOG_HDR} ** start calibration pot_val = {pot_val} ")
            pot_config[pot_val] = {}
            
            # change resistance
            pctrl.set_pots(pot_val)

            pctrl.sound_on()
            sleep(1.0)

            sample_fail = True
            while (sample_fail):
                samples_values = []
                for _ in range(CALIBRATION_SAMPLES):
                    samples_values.append(sctrl.read_val())
                
                sample_fail = False

                # counter harmonics...
                min_sampled_val = min(samples_values)
                for i in range(len(samples_values)):
                    if (samples_values[i] > 1.5 * min_sampled_val):
                        samples_values[i] = samples_values[i] / 2
                avg = mean(samples_values)

                # all samples need to be within tolerance
                for x in samples_values:
                    if (x > avg * (1+CALIBRATION_TOLERANCE) or x < avg * (1-CALIBRATION_TOLERANCE)):
                        sample_fail = True
                        print(f"{LOG_HDR} sampling failed... samples_values = {samples_values}. avg = {avg}")
                        break
            
            avgs.append(avg)
            print(f"{LOG_HDR} samples_values = {samples_values}, avg = {avg}")
        
            pctrl.sound_off()

            # save data
            pot_config[pot_val]["data"] = samples_values
            pot_config[pot_val]["avg"] = avg

        # attempt to fix non-monotonic issue
        if avgs[0] >= avgs[1] and avgs[0]/2 <= avgs[1]:
            avgs[0] = avgs[0] / 2

        for i in range(1, len(avgs)-1):
            this_val = avgs[i]
            prev_val = avgs[i-1]
            next_val = avgs[i+1]
            if not (prev_val*factor_lo <= this_val*factor_hi) or not (this_val*factor_lo <= next_val * factor_hi):
                if (prev_val*factor_lo <= this_val/2*factor_hi) and (this_val/2*factor_lo <= next_val * factor_hi):
                    avgs[i] = this_val / 2

        if avgs[-1] * factor_hi > 2 * avgs[-2] * factor_lo:
            avgs[-1] = avgs[-1] / 2 

        # redo calibrate if trends are not monotonic
        next_cali = True
        for i in range(1, len(avgs)-1):
            this_val = avgs[i]
            prev_val = avgs[i-1]
            next_val = avgs[i+1]
            if not (prev_val * factor_lo <= this_val * factor_hi) or not (this_val * factor_lo <= next_val * factor_hi):
                next_cali = False

        if next_cali:
            with open(CONFIG_DIRECTORY, "w+") as out_f:
                pot_config["steps"] = sweep_steps
                pot_config["avgs"] = avgs
                json.dump(pot_config, out_f)
                print(f"{LOG_HDR} Calibration data saved")
        else:
            print(f"{LOG_HDR} Calibration failed. Data not saved.")

        if (not next_cali and not skip_check):
            print(f"{LOG_HDR} Oh no! Monotonic requirement failed... Redo calibration")
            self.calibrate(steps)


    # set the digitpots for the note. This does not play the sound. Need to use with self.sound_on()/off()
    def set_note(self, note):
        if not (note in self.note2pot.keys()):
            tone_map_keys = list(tone_map.keys())
            if tone_map_keys.index(note) < tone_map_keys.index(self.min_note):
                pctrl.set_pots(0)
            else:
                pctrl.set_pots(pctrl.pot_max)
            return
        
        pctrl.set_pots(self.note2pot[note])


    def sound_on(self):
        pctrl.sound_on()


    def sound_off(self):
        pctrl.sound_off()
    

    def power_off(self):
        pctrl.power_off()

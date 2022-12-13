# set_note_test.py
#
# Author: Michael Wu, Owen Deng 2022
# Description: play some music to make sure the analog circuit works

from otamatone_lib.digital_otamatone import digitalOtamatone
from otamatone_lib.tone_mapping import tone_map
from time import sleep

# tones = [("C4", 0.3), ("D4", 0.3), ("E4", 0.3), ("C4", 0.3), ("C4", 0.3), ("D4", 0.3), ("E4", 0.3), ("C4", 0.3), ("E4", 0.3), ("F4", 0.3), ("G4", 1), ("E4", 0.3), ("F4", 0.3), ("G4", 1), ("G4", 0.3), ("A4", 0.3), ("G4", 0.3), ("F4", 0.3), ("E4", 0.3), ("C4", 1), ("G4", 0.3), ("A4", 0.3), ("G4", 0.3), ("F4", 0.3), ("E4", 0.3), ("C4", 1), ("D4", 0.3), ("G3", 0.3), ("C4", 1),("D4", 0.3), ("G3", 0.3), ("C4", 1) ]
tones = [("C4", 0.3), ("D4", 0.3), ("E4", 0.3), ("F4", 0.3), ("G4", 0.3), ("A4", 0.3) ]

controller = digitalOtamatone()

for tu in tones:
    controller.set_note(tu[0])
    print(f"{tu[0]} {tone_map[tu[0]] if tu[0] in tone_map.keys() else 'not avail'} {controller.note2pot[tu[0]] if tu[0] in controller.note2pot.keys() else 'not avail'} {controller}")
    controller.sound_on()
    sleep(tu[1])
    controller.sound_off()

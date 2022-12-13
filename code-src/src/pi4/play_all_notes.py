# play_all_notes.py
#
# Author: Owen Deng 2022
# Description: Play all notes that are available

from otamatone_lib.digital_otamatone import digitalOtamatone
from otamatone_lib.tone_mapping import tone_map
from time import sleep

controller = digitalOtamatone()
tone_map_lst = list(tone_map.keys())

for x in tone_map_lst:
    if tone_map_lst.index(x) >= tone_map_lst.index(controller.min_note) and tone_map_lst.index(x) <= tone_map_lst.index(controller.max_note):
        controller.set_note(x)
        print(f"note is {x}, freq is {tone_map[x]}, pot_val is {controller.note2pot[x]}, controller setting is {controller}")
        controller.sound_on()
        sleep(0.5)
        controller.sound_off()
        sleep(0.1)

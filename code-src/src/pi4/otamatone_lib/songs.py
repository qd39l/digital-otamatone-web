# songs.py
#
# Author: Michael Wu, Owen Deng 2022
# Description: hardcoded demo songs

from otamatone_lib.digital_otamatone import digitalOtamatone
from otamatone_lib.tone_mapping import tone_map
from time import sleep
import random

songs = {
    "happy_birthday":[
        ('C4', 0.5),
        ('C4', 0.5),
        ('D4', 1),
        ("C4", 1),

        ("F4", 1),
        ("E4", 1),
        (None, 1),

        ('C4', 0.5),
        ('C4', 0.5),
        ('D4', 1),
        ("C4", 1),

        ("G4", 1),
        ("F4", 1),
        (None, 1),
    ],

    "jingle_bell":[
        ('E4', 0.5),
        ('E4', 0.5),
        ('E4', 1),
        ('E4', 0.5),
        ('E4', 0.5),
        ("E4", 1),

        ('E4', 0.5),
        ('G4', 0.5),
        ('C4', 1.25),
        ('D4', 0.25),
        ('E4', 1.25),
        (None, 0.25),

        ('F4', 0.5),
        ('F4', 0.5),
        ('F4', 0.75),
        ('F4', 0.25),
        ('F4', 0.5),
        ('E4', 0.5),
        ('E4', 0.5),
        ('E4', 0.25),
        ('E4', 0.25),
        
        
        ('E4', 0.5),
        ("D4", 0.5),
        ('D4', 0.5),
        ("C4", 0.5),
        ('D4', 1),
        ('G4', 1)
    ],

    "girigiri":[
        ("D4", 0.5),
        ("D4", 0.5),
        ("E4", 0.5),
        ("D4", 0.5),
        ("F4", 2),

        ("F4", 0.5),
        (None, 0.15),
        ("F4", 0.5),
        ("G4", 0.5),
        ("F4", 0.5),
        ("G4", 2),

        ("G4", 0.5),
        (None, 0,15),
        ("G4", 0.5),
        ("A4", 0.5),
        ("G4", 0.5),
        ("F4", 0.5),

        ("F4", 0.3),
        ("G4", 0.3),
        ("A4", 0.3),
        ("F4", 0.3),
        ("A4#", 0.5),
        ("A4", 0.3),
        ("G4", 0.3),
        ("F4", 0.3),
        ("A4", 0.3),
        ("G4", 2)
    ]
}

def play_song(song_name="happy_birthday", speed = 0.5, counter = None):
    songs_lst = list(songs.keys())
    if not (counter is None):
        tones = songs[songs_lst[counter % len(songs_lst)]]
    else:
        tones = songs[song_name]
    controller = digitalOtamatone()

    for tu in tones:
        if (tu[0] is None): # stop
            sleep(tu[1] * speed)
            continue

        controller.set_note(tu[0])
        print(f"{tu[0]} {tone_map[tu[0]] if tu[0] in tone_map.keys() else 'not avail'} {controller.note2pot[tu[0]] if tu[0] in controller.note2pot.keys() else 'not avail'} {controller}")
        controller.sound_on()
        sleep(tu[1] * speed)
        controller.sound_off()
        sleep(speed * 0.1)

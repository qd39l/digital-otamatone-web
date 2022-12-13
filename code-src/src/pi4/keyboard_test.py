# keyboard_test.py
#
# Author: Michael Wu 2022

from otamatone_lib.digital_otamatone import digitalOtamatone
from otamatone_lib.tone_mapping import tone_map
from time import sleep
import time
import pygame
from key_mapping import Keyboard

pygame.init()
window = pygame.display.set_mode((320, 240))
pygame.display.set_caption("Pygame Demonstration")

controller = digitalOtamatone()

start = time.time()
while time.time() - start < 30:
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN):
            print("key_down")
            key_str = pygame.key.name(event.key)
            print(key_str)
            print(type(key_str))

        if (event.type == pygame.KEYUP):
            print("key_up")
            # controller.sound_off()
            pass

                
                
pygame.quit()

# calibrate_test.py
#
# Author: Michael Wu, Owen Deng 2022
# Description: The "main" function for running the system

import pygame 
from pygame.locals import *   # for event MOUSE variables
import os
import RPi.GPIO as GPIO
import time
from time import sleep
from otamatone_lib.digital_otamatone import digitalOtamatone
from otamatone_lib.tone_mapping import tone_map
from otamatone_lib.songs import play_song
from otamatone_lib.keyboard2note import keyboard2note
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

os.putenv('SDL_VIDEODRIVER', 'fbcon')   # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb0')     
os.putenv('SDL_MOUSEDRV', 'TSLIB')     # Track mouse clicks on piTFT 
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

pygame.init()
pygame.mouse.set_visible(False)

WHITE = 255, 255, 255
BLACK = 0,0,0
RED = 255, 0, 0

screen = pygame.display.set_mode((320, 240))
face = pygame.image.load("face.png")
face_rect = face.get_rect()
my_font = pygame.font.Font(None, 30)
my_buttons = {
    "Calibrate":(50,10),
    "Keyboard":(260,10),
    "Demo":(50,220), 
    "Quit":(260,220)
}
DEMO_COUNTER = 0

def render_default_screen():
    screen.fill(BLACK)               # Erase the Work space
    for my_text, text_pos in my_buttons.items():    
        text_surface = my_font.render(my_text, True, WHITE)    
        rect = text_surface.get_rect(center=text_pos)
        screen.blit(text_surface, rect)
    screen.blit(face, (80,50))
    pygame.display.flip()


def render_button_screen(button_name, note=None):
    screen.fill(BLACK)               # Erase the Work space
    for my_text, text_pos in my_buttons.items():
        if my_text == button_name:   
            text_surface = my_font.render(my_text, True, RED)  
        else:
            text_surface = my_font.render(my_text, True, WHITE)  
        rect = text_surface.get_rect(center=text_pos)
        screen.blit(text_surface, rect)
    if not (note is None):
        text_surface = my_font.render(note, True, WHITE)
        rect = text_surface.get_rect(center=(280, 60))
        screen.blit(text_surface, rect)
    if (button_name == "Keyboard"):
        text_surface = my_font.render("press q to exit keyboard mode", True, WHITE)
        rect = text_surface.get_rect(center=(160, 30))
        screen.blit(text_surface, rect)
    screen.blit(face, (80,50))
    pygame.display.flip()

render_default_screen()

start = time.time()
controller = digitalOtamatone()

while True:
    if (not GPIO.input(17)):
        quit()

    for event in pygame.event.get():        
        if(event.type is MOUSEBUTTONDOWN):            
            pos = pygame.mouse.get_pos()           
        if(event.type is MOUSEBUTTONUP):            
            pos = pygame.mouse.get_pos() 
            x,y = pos
            print(pos)
            if (x <= 85 and y <= 40):
                render_button_screen("Calibrate")
                print("Calibrate")
                controller.calibrate(steps=10)
                render_default_screen()
                controller.power_off()
            if (x >= 210 and y <= 40):
                render_button_screen("Keyboard")
                quit_flag = False
                while (not quit_flag):
                    for event in pygame.event.get():
                        if (event.type == pygame.KEYDOWN):
                            key_str = pygame.key.name(event.key)
                            if key_str == 'q':
                                controller.sound_off()
                                quit_flag = True
                                break

                            if key_str in keyboard2note.keys(): 
                                render_button_screen("Keyboard", keyboard2note[key_str])
                                controller.set_note(keyboard2note[key_str])
                                controller.sound_on()
                            else:
                                render_button_screen("Keyboard")
                                controller.sound_off()
                    
                        if (event.type == pygame.KEYUP):
                            render_button_screen("Keyboard")
                            controller.sound_off()
                render_default_screen()
                controller.power_off()

            if (x <= 85 and y >= 185):
                render_button_screen("Demo")
                play_song(counter=DEMO_COUNTER)
                DEMO_COUNTER += 1
                render_default_screen()
                controller.power_off()
            if (x >= 225 and y >= 190):
                quit()

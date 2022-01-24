import glob
import json
import os
import sys
import time
from time import sleep

import pygame
import RPi.GPIO as GPIO
from gpiozero import Button

from sherlock import Sherlock

if __name__=='__main__':
    # Print instructions
    print('#'*10)
    print('WELCOME TO SHERLOCK')
    print('#'*10)
    print('\n')
    print('#'*5)
    print('INSTRUCTIONS')
    print('#'*5)
    print('1. Press the right button (NEXT) to skip to the next track.')
    print('2. Press the central button (PLAY/PAUSE) to play/pause the track.')
    print('3. Press the left button (BACK) to go back to the previous track.')
    print('4. Long press the right button (NEXT) to fast-forward the current track.')
    print('5. Long press the left button (BACK) to fast-backward the current track.')
    print('\n')
    print('Have fun!')
    
    # Initialize the device
    sherlock = Sherlock(
            TRACKS_DIR='./tracks',
            FW_PIN=3,
            BW_PIN=5, 
            PLAY_PIN=11, 
            OUT_PIN=13,
            BOUNCE=200, # [milliseconds]
            SKIP_TIME=10, # [seconds]
            LONG_PRESS_TIME=2, # [seconds]
            CURRENT_IDX=0, 
            PLAY_STATE=False,
            RESTART_TIME=2 # [seconds]
    )
    
    # Start continuous loop
    while True:
        pass
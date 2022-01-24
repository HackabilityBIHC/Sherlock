import glob
import json
import os
import sys
import time
import yaml
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
    
    # Load parameters file
    with open('./config/sherlock_parameters.yaml', 'r') as param_file:
        sherlock_params_dict = yaml.load(param_file, Loader=yaml.FullLoader)
    
    # Initialize the device
    sherlock = Sherlock(**sherlock_params_dict)
    
    # Start continuous loop
    while True:
        pass
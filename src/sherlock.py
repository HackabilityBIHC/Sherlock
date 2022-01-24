import glob
import json
import os
import sys
import time
from time import sleep

import pygame
import RPi.GPIO as GPIO
from gpiozero import Button

class Sherlock:
    '''
    A Sherlock object contains all methods and attributes to setup and control
    a Sherlock device. It builds upon the pygame.mixer object.
    '''
    def __init__(
                 self,
                 TRACKS_DIR='./tracks',
                 FW_PIN=3,
                 BW_PIN=5, 
                 PLAY_PIN=11, 
                 OUT_PIN=13,
                 BOUNCE=200, # [milliseconds]
                 SKIP=10, # [seconds]
                 LONG_PRESS_TIME=2, # [seconds]
                 START_IDX=0, 
                 PLAY_STATE=False
                 ):
        '''
        Args:
            FW_PIN (int)         : RaspberryPi board pin for NEXT button
            BW_PIN (int)         : RaspberryPi board pin for BACK button
            PLAY_PIN (int)       : RaspberryPi board pin for PLAY/PAUSE button
            OUT_PIN (int)        : RaspberryPi board pin for OUTPUT
            BOUNCE (int)         : time delay (in [ms]) to compensate bounce effect
            SKIP (int)           : time (in [s]) to skip when long-pressing the NEXT button
            LONG_PRESS_TIME (int): time (in [s]) to long-press the NEXT button before triggering the fast-forward
            START_IDX (int)      : index of track to start the playback (assuming tracks are ordered)
            PLAY_STATE (bool)    : flag for play/pause status
        
        '''
        # RaspberryPi board setup
        self.fw_pin = FW_PIN # NEXT
        self.bw_pin = BW_PIN # BACK
        self.play_pin = PLAY_PIN # PLAY/PAUSE
        self.out_pin = OUT_PIN # OUTPUT
        
        # Compensate bounce effect
        self.bounce = BOUNCE
        
        # Initialize GPIO   
        self.init_board()
        
        # Store tracks
        self.tracks = [os.path.join(TRACKS_DIR, track) for track in os.listdir(TRACKS_DIR)]
        # How many seconds to skip forward when long-pressing NEXT button
        self.fforward_skip = SKIP
        self.long_press_time = LONG_PRESS_TIME
        # From which track to start the playback (assuming the tracks in the folder are ordered)
        self.start_idx = START_IDX
        # Flag for play/pause status
        self.is_playing = PLAY_STATE
        
        # Initialize pygame.mixer object
        self.player = pygame.mixer.init().music
        
        
    
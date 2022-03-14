import os
import time
import subprocess

import pygame
import RPi.GPIO as GPIO
from gpiozero import Button
from gpiozero import MCP3008

from mutagen.mp3 import MP3

class Sherlock:
    '''
    A Sherlock object contains all methods and attributes to setup and control
    a Sherlock device. It builds upon the GPIO libray and the pygame.mixer object.
    
    Methods:
        init_board              : initializes RaspberryPi board
        init_player             : initializes pygame.mixer.music
        _play                   : stops current track, loads track indicated by self.current_idx, then plays it
        _forward                : skips to next track or fast-forwards the current track. Used as callback in GPIO.add_event_detect
        _fastforward            : fast-forwards the current track by incrementing track position
        _backward               : restart current track or goes back to previous track. Used as callback in GPIO.add_event_detect
        _fastbackward           : fast-backwards the current track by decrementing track position
        _play_pause             : pause/unpause the current track. Used as callback in GPIO.add_event_detect
        _long_press             : detects long-pressing of any button and trigger specific action
        
    Examples:
        >>> device1 = Sherlock(1, 2, 3, 4, 5) # dummy pins 
        >>>
        >>> device2 = Sherlock(6, 7, 8, 9, 10, CURRENT_IDX=1, SUPPORTED_FORMATS=['wav', 'oog'])
    '''
    def __init__(
                 self,
                 FW_PIN,
                 BW_PIN, 
                 PLAY_PIN, 
                 FW_LED_PIN,
                 BW_LED_PIN,
                 PLAY_LED_PIN,
                 R_LED_STRIPE,
                 G_LED_STRIPE,
                 B_LED_STRIPE,
                 TRACKS_DIR='./tracks',
                 BOUNCE=1000, # [milliseconds]
                 SKIP_TIME=10, # [seconds]
                 LONG_PRESS_TIME=2, # [seconds]
                 CURRENT_IDX=0, 
                 PLAY_STATE=False,
                 RESTART_TIME=2, # [seconds]
                 SUPPORTED_FORMATS=['mp3'],
                 STRIPE_FREQ = 100000
                 ):
        '''
        Store all parameters, then (1) initialize the board, (2) initialize
        te pygame.mixer.music object.
        
        Args:
            FW_PIN (int)            : RaspberryPi board pin for NEXT button.
            BW_PIN (int)            : RaspberryPi board pin for BACK button.
            PLAY_PIN (int)          : RaspberryPi board pin for PLAY/PAUSE button.
            OUT_PIN (int)           : RaspberryPi board pin for OUTPUT.
            TRACKS_DIR (str)        : path to the folder where the tracks are stored. Defaults to: '.tracks'
            BOUNCE (int)            : time delay (in [ms]) to compensate bounce effect. Defaults to: 200
            SKIP_TIME (int)         : time (in [s]) to skip when long-pressing the NEXT button. Defaults to: 10
            LONG_PRESS_TIME (int)   : time (in [s]) to long-press the NEXT button before triggering the fast-forward. Defaults to: 2
            CURRENT_IDX (int)       : index of track to start the playback (assuming tracks are ordered). Defaults to: 0
            PLAY_STATE (bool)       : flag for play/pause status. Defaults to: False
            RESTART_TIME (int)      : time (in [s]) AFTER which the BACK button restarts the current track instead of going back to the previous one. Defaults to: 2
            SUPPORTED_FORMATS (list): list of supported adio formats as strings. Defaults to: ['mp3']
        '''
        
        # RaspberryPi board setup
        self.fw_pin = FW_PIN # NEXT
        self.bw_pin = BW_PIN # BACK
        self.play_pin = PLAY_PIN # PLAY/PAUSE
        
        self.fw_led_pin = FW_LED_PIN # OUTPUT
        self.bw_led_pin = BW_LED_PIN # OUTPUT
        self.play_led_pin = PLAY_LED_PIN # OUTPUT
        self.bounce = BOUNCE # Compensate bounce effect
        self.r_led_stripe = R_LED_STRIPE #red value led stripe
        self.g_led_stripe = G_LED_STRIPE #green value led stripe
        self.b_led_stripe = B_LED_STRIPE #blue value led stripe
        
        # Other parameters
        self.tracks = [os.path.join(TRACKS_DIR, track) for track in os.listdir(TRACKS_DIR) for fmt in SUPPORTED_FORMATS if track.endswith(fmt)] # store tracks
        print('Initializing tracks...', self.tracks)
        self.skip_time = SKIP_TIME # How many seconds to skip forward when long-pressing NEXT button
        self.long_press_time = LONG_PRESS_TIME # How long to keep pressing the NEXT button to trigger the fast-forward
        self.current_idx = CURRENT_IDX # From which track to start the playback (assuming the tracks in the folder are ordered)
        print('Initializing index for tracks...', self.current_idx)
        self.is_playing = PLAY_STATE # Flag for play/pause status
        self.restart_track_time = RESTART_TIME # after how many seconds the BACK button pressing restarts the current track instead of going back to the previous track
        self.stripe_freq = STRIPE_FREQ #PWM frequency for led stripe

        #parameters considered private
        self._absolute_time = 0 # Absolute time of current position from start of audio track
        self._play_time_start = 0 # Time stamp from start of playing/unpausing/skipping (uses time.time())

        ### INITIALIZATIONS ### 
        # 1. Initialize GPIO 
        print('Initializing board...')
        self.init_board()
        # 2. Initialize audioplayer
        print('Initializing audioplayer...')
        self.init_player()
        
        print('Ready! Press the PLAY/PAUSE button to start!')
        
    def init_board(self):
        '''Initialize GPIO input/output pins and event detection.'''
        ### GPIO SETUP ###
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        # Set pins modes
        GPIO.setup(self.fw_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.bw_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.play_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.setup(self.fw_led_pin, GPIO.OUT)
        GPIO.setup(self.bw_led_pin, GPIO.OUT)
        GPIO.setup(self.play_led_pin, GPIO.OUT)

        GPIO.setup(self.r_led_stripe, GPIO.OUT)
        GPIO.setup(self.g_led_stripe, GPIO.OUT)
        GPIO.setup(self.b_led_stripe, GPIO.OUT)

        #GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.potentiometer = MCP3008(0)
        self.pot_old = 0
        
        self.r_pwm = GPIO.PWM(self.r_led_stripe, self.stripe_freq)
        self.g_pwm = GPIO.PWM(self.g_led_stripe, self.stripe_freq)
        self.b_pwm = GPIO.PWM(self.b_led_stripe, self.stripe_freq)
        self.r_pwm.start(0)
        self.g_pwm.start(0)
        self.b_pwm.start(100)

        
    def init_player(self):
        '''Initialize pygame.mixer object.'''
        ### PYGAME SETUP ###
        self.mixer = pygame.mixer
        self.mixer.init()
        self.player = self.mixer.music

        
    def _play(self):
        '''Play the current track (self.current_idx).'''
        # Stop the playback if it's playing
        self.player.stop()
        # Load the current track
        self.player.load(self.tracks[self.current_idx])
        # Start playing
        self.player.play()
        
        # Initialize absolute time of playing
        self._absolute_time = 0
        # Initialize starting time
        self._play_time_start = time.time()
        # Set is_playing flag
        self.is_playing = True
        # Initialize track duration
        self.track_duration = MP3(self.tracks[self.current_idx]).info.length

        
    def _forward(self):
        '''
        Pressing the NEXT button lets the user skip to the next track.
        Long-pressing the NEXT button for `N` seconds lets the user fast-forward the track by `skip` seconds.
        
        Args:
            channel: parameter passed by GPiO.add_event_detect callback. It is the pin number
        '''
        # Play track
        self._play()
        print(f"Avanti. Traccia corrente #{self.current_idx+1} - ({self.tracks[self.current_idx]})")

        # Skip to next track
        if(self.current_idx == len(self.tracks)-1):
            self.current_idx = 0
        else:
            self.current_idx += 1       

    
    def _fastforward(self):
        '''
        Long-pressing the NEXT button for `N` seconds lets the user 
        fast-forward the current track by `self.skip_time` seconds.
        
        Note: depending on the audio format, pygame.mixer.music.set_pos
        behaves differently. For .mp3 audio files, set_pos sets the new
        position relatively to the current position - i.e., if you do
        set_pos(5), it will skip to 5 seconds after the current position.
        
        More info on the official documentation: 
        https://www.pygame.org/docs/ref/music.html#pygame.mixer.music.set_pos
        '''
        # If playing, update absolute time to current position and update time of playing
        if (self.is_playing):
            self._absolute_time += (time.time() - self._play_time_start)
            self._play_time_start = time.time()

        # Increment absolute time by skip seconds
        self._absolute_time += self.skip_time

        # Initialize player pointer to start
        self.player.rewind()

        # Skip to absolute time until the end of the track is reached
        if self._absolute_time < self.track_duration:
            self.player.set_pos(self._absolute_time)
        else:
            # If the end of the track is reached then the track is stopped
            self.player.stop()

        print("Fast forward")
    
    def _backward(self):
        '''
        Pressing the BACK button lets te user either restart the current track
        or go back to the previous one if the time from the start of the current
        track is less than a pre-defined time interval.
        
        Note: get_pos() returns time from start of playback in [milliseconds].   
        
        Args:
            channel: parameter passed by GPiO.add_event_detect callback. It is the pin number
        '''
        # If self.restart_track_time has passed, then restart current track
        if(self.player.get_pos()//1000 > self.restart_track_time):
            self._play()
            print(f"Rinizio. Traccia corrente #{self.current_idx+1} - ({self.tracks[self.current_idx]})")
        else:
            # Go to previous track
            if(self.current_idx == 0):
                self.current_idx = len(self.tracks)-1
            else:
                self.current_idx -= 1
            self._play()
            print(f"Indietro. Traccia corrente #{self.current_idx+1} - ({self.tracks[self.current_idx]})")
                
    def _fastbackward(self):
        '''
        Long-pressing the BACK button for 'self.long_press_time' seconds
        lets the user go back of the current track by 'self.skip_time' seconds.
        
        Note: see self._fastforward() note.
        '''
        # Go back by 'self.skip_time' seconds
        raise NotImplementedError
        
    def _play_pause(self):
        '''
        Pressing the center PLAY/PAUSE button, plays or pauses the current track.
                
        Args:
            channel: parameter passed by GPiO.add_event_detect callback. It is the pin number
        '''
        if(self.is_playing):
            self.player.pause()		
            #update absolute position to current time
            self._absolute_time += (time.time() - self._play_time_start)
            print(f"Pausa. Traccia corrente #{self.current_idx+1} - ({self.tracks[self.current_idx]})")
            self.is_playing = False
        else:
            self.player.unpause()
            #restart counting time
            self._play_time_start = time.time()
            print(f"Play. Traccia corrente #{self.current_idx+1} - ({self.tracks[self.current_idx]})")
            self.is_playing = True

    def _setVolume(self, pot_new):
        self.player.set_volume(pot_new)
        self.pot_old = pot_new


    def __del__(self):
        self.r_pwm.stop()
        self.g_pwm.stop()
        self.b_pwm.stop()
        print("ADDIO")
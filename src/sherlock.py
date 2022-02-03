import os
import time

import pygame
import RPi.GPIO as GPIO
from gpiozero import Button

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
                 OUT_PIN,
                 TRACKS_DIR='./tracks',
                 BOUNCE=200, # [milliseconds]
                 SKIP_TIME=10, # [seconds]
                 LONG_PRESS_TIME=2, # [seconds]
                 CURRENT_IDX=0, 
                 PLAY_STATE=False,
                 RESTART_TIME=2 # [seconds]
                 SUPPORTED_FORMATS=['mp3']
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
        self.out_pin = OUT_PIN # OUTPUT
        self.bounce = BOUNCE # Compensate bounce effect
        
        # Other parameters
        self.tracks = [os.path.join(TRACKS_DIR, track) for track in os.listdir(TRACKS_DIR) for fmt in SUPPORTED_FORMATS if track.endswith(fmt)] # store tracks
        self.skip_time = SKIP_TIME # How many seconds to skip forward when long-pressing NEXT button
        self.long_press_time = LONG_PRESS_TIME # How long to keep pressing the NEXT button to trigger the fast-forward
        self.current_idx = CURRENT_IDX # From which track to start the playback (assuming the tracks in the folder are ordered)
        self.is_playing = PLAY_STATE # Flag for play/pause status
        self.restart_track_time = RESTART_TIME # after how many seconds the BACK button pressing restarts the current track instead of going back to the previous track
        
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
        
        # Set pins modes
        GPIO.setup(self.fw_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.bw_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.play_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.out_pin, GPIO.OUT)
        GPIO.output(self.out_pin, GPIO.HIGH)
        
        # Detect button pressing events
        GPIO.add_event_detect(self.fw_pin, GPIO.FALLING, callback=self._forward, bouncetime=self.bounce)
        GPIO.add_event_detect(self.bw_pin, GPIO.FALLING, callback=self._backward, bouncetime=self.bounce)
        GPIO.add_event_detect(self.play_pin, GPIO.FALLING, callback=self._play_pause, bouncetime=self.bounce)
        
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
        
        # Set is_playing flag
        self.is_playing = True
        
    def _forward(self, channel):
        '''
        Pressing the NEXT button lets the user skip to the next track.
        Long-pressing the NEXT button for `N` seconds lets the user fast-forward the track by `skip` seconds.
        
        Args:
            channel: parameter passed by GPiO.add_event_detect callback. It is the pin number
        '''
        # Detect long-press
        long_press_flag = self._long_press(self.fw_pin, self._fastforward)
            
        # If single, short press, skip to next track
        if (not long_press_flag):
            if(self.current_idx == len(self.tracks)-1):
                self.current_idx = 0
            else:
                self.current_idx += 1
            # Play next track
            self._play()

            print(f"Avanti. Traccia corrente #{self.current_idx}")
        elif long_press_flag:
            print(f'Fast-forward. Traccia corrente #{self.current_idx}')
    
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
        # Skip by 'fforward_skip' seconds
        self.player.set_pos(self.skip_time)
    
    def _backward(self, channel):
        '''
        Pressing the BACK button lets te user either restart the current track
        or go back to the previous one if the time from the start of the current
        track is less than a pre-defined time interval.
        
        Note: get_pos() returns time from start of playback in [milliseconds].   
        
        Args:
            channel: parameter passed by GPiO.add_event_detect callback. It is the pin number
        '''
        # Detect long-press
        long_press_flag = self._long_press(self.bw_pin, self._fastbackward)
        
        if (not long_press_flag):
            # If self.restart_track_time has passed, then restart current track
            if(self.player.get_pos()//1000 > self.restart_track_time):
                self._play()
            else:
                # Go to previous track
                if(self.current_idx == 0):
                    self.current_idx = len(self.tracks)-1
                else:
                    self.current_idx -= 1
                self._play()
                print(f"Indietro. Traccia corrente #{self.current_idx}")
        elif long_press_flag:
            print(f'Fast-backward. Traccia corrente #{self.current_idx}')
                
    def _fastbackward(self):
        '''
        Long-pressing the BACK button for 'self.long_press_time' seconds
        lets the user go back of the current track by 'self.skip_time' seconds.
        
        Note: see self._fastforward() note.
        '''
        # Go back by 'self.skip_time' seconds
        raise NotImplementedError
        
    def _play_pause(self, channel):
        '''
        Pressing the center PLAY/PAUSE button, plays or pauses the current track.
                
        Args:
            channel: parameter passed by GPiO.add_event_detect callback. It is the pin number
        '''
        if(self.is_playing):
            self.player.pause()		
            print(f"Pausa. Traccia corrente #{self.current_idx}")
            self.is_playing = False
        else:
            self.player.unpause()
            print(f"Play. Traccia corrente #{self.current_idx}")
            self.is_playing = True
            
    def _long_press(self, pin, action, **action_kwargs):
        '''
        Detect long-pressing of any button. 
        
        Note: The action triggered by the long-pressing is repeated every half-second.
        
        Args:
            pin (int)               : board pin to detect the long-pressing from
            action (function)       : which action to trigger when long-pressing
            action_kwargs (kwargs)  : any kwargs needed by the action function (do not specify any if the function does not need any)
            
        Returns:
            long_press_flag (bool)  : whether the long-press was detected or not
        '''
        # Compute time from when button press is detected
        start_press = time.time()
        
        # Detect if the NEXT button has been long-pressed
        long_press_flag = False
        
        while GPIO.input(pin) == GPIO.LOW: 
            time.sleep(.5)
            if(time.time()-start_press > self.long_press_time):
                # Long-pressing triggers a specific action
                action(**action_kwargs)
                
                # Do not go to the next track
                long_press_flag = True
                
        return long_press_flag

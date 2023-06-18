import logging
import time
from pathlib import Path
from typing import List, Optional, Union

import pygame
import RPi.GPIO as GPIO
from gpiozero import MCP3008
from mutagen.mp3 import MP3


class Sherlock:
    """Base class for Sherlock devices.

    A Sherlock class object contains all methods and attributes to setup and control
    a Sherlock device. It builds upon the GPIO libray and the pygame.mixer object.
    
    Methods:
        init_board:
            Initializes RaspberryPi board
        init_player:
            Initializes pygame.mixer.music
        _play:
            Stops current track, loads track indicated by self.current_idx,
            then plays it from the start.
        _forward:
            Skips to next track or fast-forwards the current track if long-press
            is detected. Used as callback in GPIO.add_event_detect().
        _fastforward:
            Fast-forwards the current track by incrementing track temporal position.
        _backward:
            Restarts current track or goes back to previous track. Used as callback in GPIO.add_event_detect().
        _play_pause:
            Pauses/unpauses the current track. Used as callback in GPIO.add_event_detect().
        _long_press:
            Detects long-pressing of any button and trigger specific action.
        
    Examples:
        >>> device1 = Sherlock(1, 2, 3, 4, 5) # dummy pins 
        >>>
        >>> device2 = Sherlock(6, 7, 8, 9, 10, CURRENT_IDX=1, SUPPORTED_FORMATS=["wav", "oog"])
    """
    def __init__(
                 self,
                 FW_PIN: int,
                 BW_PIN: int,
                 PLAY_PIN: int,
                 LAMP_PIN: int,
                 SWITCH_PIN: int,
                 BOUNCE: int = 500, # [milliseconds]
                 START_VOLUME: int = 0,
                 TRACKS_DIR: Union[str, Path] = "./tracks",
                 SKIP_TIME: int = 10, # [seconds]
                 LONG_PRESS_TIME: int = 2, # [seconds]
                 CURRENT_IDX: int = 0,
                 RESTART_TIME: int = 2, # [seconds]
                 SUPPORTED_FORMATS: List[str] = ["mp3"],
                 logger: Optional[logging.Logger] = None,
                 ):
        """Initialize Sherlock object.

        (1) Initializes the board,
        (2) initializes the pygame.mixer.music object.
        (3) Looks for tracks in the removable device folder. If None, it won't start.
        
        Args:
            FW_PIN (int):
                RaspberryPi board pin for NEXT button.
            BW_PIN (int):
                RaspberryPi board pin for BACK button.
            PLAY_PIN (int):
                RaspberryPi board pin for PLAY/PAUSE button.
            LAMP_PIN (int):
                RaspberryPi board pin for the external LIGHT/LAMP pin.
            SWITCH_PIN (int):
                RaspberryPi board pin for the external lamp SWITCH ON/OFF button.
            BOUNCE (int):
                Time delay (in [ms]) to compensate bounce effect. Defaults to: 500.
            START_VOLUME (int):
                Initial volume of the device. Defaults to: 0.
            TRACKS_DIR (Path, str):
                Path to the folder where the tracks are stored. Defaults to: "./tracks".
            SKIP_TIME (int):
                Time (in [s]) to fast-forward skip when long-pressing the NEXT button. Defaults to: 10.
            LONG_PRESS_TIME (int):
                Time (in [s]) to long-press the NEXT button before triggering the fast-forward. Defaults to: 2.
            CURRENT_IDX (int):
                Index of track to start the playback (assuming tracks are ordered). Defaults to: 0.
            RESTART_TIME (int):
                Time (in [s]) AFTER which the BACK button restarts the current
                track instead of going back to the previous one. Defaults to: 2.
            SUPPORTED_FORMATS (List[str]):
                List of supported adio formats as strings. Defaults to: ["mp3"].
            logger (logging.Logger, None):
                Logger object to log sessions.
        """
        # Log
        msg = "Initializing Sherlock circuit board..."
        logger.info(msg) if logger else print(msg)

        # RaspberryPi board setup
        self.init_board(
            FW_PIN,
            BW_PIN,
            PLAY_PIN,
            LAMP_PIN,
            SWITCH_PIN,
            BOUNCE,
            START_VOLUME,
        )
    
        # Log
        msg = "Initializing Sherlock audio player..."
        logger.info(msg) if logger else print(msg)
        
        # PyGame audio player setup
        self.init_player(
            SKIP_TIME,
            LONG_PRESS_TIME,
            CURRENT_IDX,
            RESTART_TIME,
        )

        # Log
        msg = f"Looking for tracks to load in: {TRACKS_DIR}..."
        logger.info(msg) if logger else print(msg)

        # Load tracks
        self.supported_formats = [str(ext).lstrip(".") for ext in SUPPORTED_FORMATS] # strip leading dots
        self.tracks_dir = TRACKS_DIR
        # Initialize empty
        self.tracks = []

        self.load_tracks()

        # Log
        msg = f"Found {len(self.tracks)} tracks to play: {[Path(t).name for t in self.tracks]}."
        logger.info(msg) if logger else print(msg)

        # Log
        msg = f"""
            ###########################
            SETUP DONE! READY TO START!
            ###########################
            
            Press the PLAY/PAUSE button to start Sherlock!"
        """
        logger.info(msg) if logger else print(msg)


    def init_board(
            self,
            FW_PIN: int,
            BW_PIN: int,
            PLAY_PIN: int,
            LAMP_PIN: int,
            SWITCH_PIN: int,
            BOUNCE: int,
            START_VOLUME: int,
        ):
        """Initialize GPIO input/output pins and event detection parameters.
        
        Args:
            FW_PIN (int):
                RaspberryPi board pin for NEXT button.
            BW_PIN (int):
                RaspberryPi board pin for BACK button.
            PLAY_PIN (int):
                RaspberryPi board pin for PLAY/PAUSE button.
            LAMP_PIN (int):
                RaspberryPi board pin for the external LIGHT/LAMP pin.
            SWITCH_PIN (int):
                RaspberryPi board pin for the external lamp SWITCH ON/OFF button.
            BOUNCE (int):
                Time delay (in [ms]) to compensate bounce effect.
            START_VOLUME (int):
                Initial volume of the device.
        """
        # Store pins
        self.fw_pin = FW_PIN
        self.bw_pin = BW_PIN
        self.play_pin = PLAY_PIN
        self.lamp_pin = LAMP_PIN
        self.switch_pin = SWITCH_PIN

        # Other parameters
        self.bounce = BOUNCE
        self.start_volume = START_VOLUME

        # Setup GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        # Set pins modes
        GPIO.setup(self.fw_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.bw_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.play_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.lamp_pin, GPIO.OUT)
    
        # Set volume to 0
        self.potentiometer = MCP3008(0)
        self.prev_volume = self.start_volume

        # Lamp on at start
        self.lamp_on = True
        GPIO.output(self.lamp_pin, GPIO.HIGH)


    def init_player(
            self,
            SKIP_TIME: int,
            LONG_PRESS_TIME: int,
            CURRENT_IDX: int,
            RESTART_TIME: int,
        ):
        """Initialize pygame.mixer object and mediaplayer related parameters.
        
        Args:
            SKIP_TIME (int):
                Time (in [s]) to fast-forward skip when long-pressing the NEXT button. Defaults to: 10.
            LONG_PRESS_TIME (int):
                Time (in [s]) to long-press the NEXT button before triggering the fast-forward. Defaults to: 2.
            CURRENT_IDX (int):
                Index of track to start the playback (assuming tracks are ordered). Defaults to: 0.
            RESTART_TIME (int):
                Time (in [s]) AFTER which the BACK button restarts the current
                track instead of going back to the previous one. Defaults to: 2.
        """
        ### PYGAME SETUP ###
        self.mixer = pygame.mixer
        self.mixer.init()
        self.player = self.mixer.music

        # Other mediaplayer-related parameters
        self.is_playing = False # Paused at start
        self._absolute_time = 0 # Absolute time of current position from start of audio track
        self._play_time_start = 0 # Time stamp from start of playing/unpausing/skipping (uses time.time())

        # Other parameters
        self.skip_time = SKIP_TIME # How many seconds to skip forward when long-pressing NEXT button
        self.long_press_time = LONG_PRESS_TIME # How long to keep pressing the NEXT button to trigger the fast-forward
        self.current_idx = CURRENT_IDX # From which track to start the playback (assuming the tracks in the folder are ordered)
        self.restart_track_time = RESTART_TIME # after how many seconds the BACK button pressing restarts the current track instead of going back to the previous track

    
    def _load_tracks(self):
        """Load tracks to play.
        
        Warning: it does not check if no tracks were found.
        """
        # Get all tracks with the supported extensions
        tracks = [str(track) for ext in self.supported_formats for track in Path(self.tracks_dir).rglob(f"*.{ext}")]
        # Sort tracks numerically (supposing they have an order, else order alphabetically)
        tracks.sort()

        # Note: can be empty
        self.tracks = tracks


    def load_tracks(self):
        """Repeatedly search for tracks to load until any are found in the specified folder.
        
        We check if any tracks are found. If none, then keeps searching until they
        have been uploaded to the specified folder. In the meantime, the light blinks.

        Example:
            The tracks are not stored locally, but on a removable device (e.g., USB pen).
            The specified folder to look for tracks in is "/media/<user>/<removable device>/".
            
            As long as the device is not inserted, no tracks can be loaded, the light
            blinks and the program is stuck. Once the device with the corresponding
            tracks is inserted, the tracks are loaded, the light stops blinking and
            the program can move on.

            If the removable device is already inserted, then there's no waiting.

        Args:
            logger (logging.Logger, None):
                Logger object to log sessions.
        """
        # Store lamp status
        initial_lamp_status = self.lamp_on

        # Continuously look for tracks until any are found
        while True:
            # Look for tracks once and save paths to `self.tracks`
            self._load_tracks()

            # If any are found, stop blinking and exit
            if self.tracks:
                self.lamp_on = initial_lamp_status
                self._lamp_switch()
                break
            
            # If none are found and track is playing, stop playback until tracks are found again
            if self.is_playing:
                self._play_pause()
            # Blink light while it searches for tracks
            self._lamp_switch()
            time.sleep(0.4)

        
    def _play(self):
        """Play the current track (`self.current_idx`)."""
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
        """
        Pressing the NEXT button lets the user skip to the next track.
        Long-pressing the NEXT button for `N` seconds lets the user fast-forward the track by `skip` seconds.
        
        Args:
            channel: parameter passed by GPiO.add_event_detect callback. It is the pin number
        """
        # Skip to next track
        if self.current_idx == len(self.tracks)-1:
            self.current_idx = 0
        else:
            self.current_idx += 1       
        
        # Play track
        self._play()


    def _fastforward(self):
        """
        Long-pressing the NEXT button for `N` seconds lets the user 
        fast-forward the current track by `self.skip_time` seconds.
        
        Note: depending on the audio format, pygame.mixer.music.set_pos
        behaves differently. For .mp3 audio files, set_pos sets the new
        position relatively to the current position - i.e., if you do
        set_pos(5), it will skip to 5 seconds after the current position.
        
        More info on the official documentation: 
        https://www.pygame.org/docs/ref/music.html#pygame.mixer.music.set_pos
        """
        # If playing, update absolute time to current position and update time of playing
        if self.is_playing:
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
    

    def _backward(self):
        """
        Pressing the BACK button lets te user either restart the current track
        or go back to the previous one if the time from the start of the current
        track is less than a pre-defined time interval.
        
        Note: get_pos() returns time from start of playback in [milliseconds].   
        
        Args:
            channel: parameter passed by GPiO.add_event_detect callback. It is the pin number
        """
        # If self.restart_track_time has passed, then restart current track
        if self.player.get_pos()//1000 > self.restart_track_time:
            self._play()
        else:
            # Go to previous track
            if(self.current_idx == 0):
                self.current_idx = len(self.tracks)-1
            else:
                self.current_idx -= 1
            self._play()


    def _fastbackward(self):
        """
        Long-pressing the BACK button for "self.long_press_time" seconds
        lets the user go back of the current track by "self.skip_time" seconds.
        
        Note: see self._fastforward() note.
        """
        # Go back by "self.skip_time" seconds
        raise NotImplementedError
    

    def _play_pause(self):
        """
        Pressing the center PLAY/PAUSE button, plays or pauses the current track.
                
        Args:
            channel: parameter passed by GPiO.add_event_detect callback. It is the pin number
        """
        if self.is_playing:
            self.player.pause()		
            #update absolute position to current time
            self._absolute_time += (time.time() - self._play_time_start)
            self.is_playing = False
        else:
            self.player.unpause()
            #restart counting time
            self._play_time_start = time.time()
            self.is_playing = True


    def _set_volume(self, new_volume):
        """Set volume of device."""
        self.player.set_volume(new_volume)
        self.prev_volume = new_volume


    def _lamp_switch(self):
        """Turn lamp on/off."""
        # Lamp is on, turn it off
        if self.lamp_on:
            GPIO.output(self.lamp_pin, GPIO.LOW)
            self.lamp_on = False
        # Lamp is off, turn it on
        else:
            GPIO.output(self.lamp_pin, GPIO.HIGH)
            self.lamp_on = True


    def run(self, logger: Optional[logging.Logger] = None):
        """Main running logic."""
        long_press_flag = False
        t_old = 0
        while True:
            try:
                # Check volume level
                new_volume = round(self.potentiometer.value, 1)
                if new_volume != self.prev_volume:
                    self._set_volume(new_volume)

                ##### FORWARD BUTTON LOGIC #####
                if GPIO.input(self.fw_pin) == GPIO.LOW:
                    if(time.time() - t_old > self.bounce):
                        start = time.time()
                        long_press_flag = False
                        # Forward long-press = fast-forward current track
                        while GPIO.input(self.fw_pin) == GPIO.LOW:
                            duration = time.time() - start
                            # Need to press for longer than `long_press_time`
                            if duration > self.long_press_time:
                                self._fastforward()
                                long_press_flag = True
                                duration = 0
                                start = time.time()
                        
                        # Forward (short) press = next track
                        if not long_press_flag:    
                            self._forward()
                            # Log
                            msg = f">>>> FORWARD >>>> New track: {Path(self.tracks[self.current_idx]).name}."
                            logger.info(msg) if logger else print(msg)
                        t_old = time.time()
                
                ##### BACKWARD BUTTON LOGIC #####
                if GPIO.input(self.bw_pin) == GPIO.LOW:
                    if time.time() - t_old > self.bounce:
                        while GPIO.input(self.bw_pin) == GPIO.LOW:
                            pass
                        # Backward press = restart track if after n seconds from start
                        # Backward press = previous track if before n seconds from start
                        self._backward()
                        # Log
                        msg = f"<<<< BACKWARD <<<< New track: {Path(self.tracks[self.current_idx]).name}"
                        logger.info(msg) if logger else print(msg)
                        t_old = time.time()
                        
                        # Backward long-press = fast-backward current track
                        # TODO: implement fast-backward
                
                ##### PLAY BUTTON LOGIC #####
                if GPIO.input(self.play_pin) == GPIO.LOW:
                    if time.time() - t_old > self.bounce:
                        while GPIO.input(self.play_pin) == GPIO.LOW:
                            pass
                        
                        # Play button press = play/pause if in pause/playing respectively
                        self._play_pause()
                        # Log
                        msg = f"==== {'PLAY' if self.is_playing else 'PAUSE'} ===="
                        logger.info(msg) if logger else print(msg)

                        t_old = time.time()   

                ##### LAMP BUTTON LOGIC #####
                if GPIO.input(self.switch_pin) == GPIO.LOW:
                    if time.time() - t_old > self.bounce:
                        # Lamp button press = turn lamp on/off if off/on respectively
                        self._lamp_switch()
                        while GPIO.input(self.switch_pin) == GPIO.LOW:
                            pass
                        
                        # Log
                        msg = f"**** LIGHT {'ON' if self.lamp_on else 'OFF'} ****"
                        logger.info(msg) if logger else print(msg)

                        t_old = time.time()

            # If tracks cannot be found anymore (e.g., because USB was removed or tracks deletec), pygame will throw a pygame.error
            except pygame.error:
                msg = f"""
                    Could not find the tracks to play anymore. 
                    Please, check and upload the tracks to play in: {self.tracks_dir}.
                """

                logger.info(msg) if logger else print(msg)
                # Look for tracks
                self.load_tracks()


    def __del__(self):
        GPIO.output(self.lamp_pin, GPIO.LOW)
        self.lamp_on = False


    def __repr__(self):
        return f"{type(self).__name__}({' '.join(f'{k}={v}' for k, v in self.__dict__.items())})"
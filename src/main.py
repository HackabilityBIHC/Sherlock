import os
import yaml

import RPi.GPIO as GPIO
import time

from sherlock import Sherlock

def welcome_sherlock():
    '''Prints welcome and instructions for usage.'''
    # Print instructions
    print('#'*10)
    print('WELCOME TO SHERLOCK! :)')
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

def goodbye_sherlock():
    '''Prints closing message for KeyboardInterrupt exception.'''
    # Print goodbye
    print('#'*10)
    print('GOODBYE! COME BACK SOON! :)')
    print('#'*10)
    
def read_yaml(config_path='/home/pi/Desktop/Sherlock-dev/config/sherlock_parameters.yaml'):
    '''
    Reads a .yaml file from the specified path. Returns a dict of parameters.
    
    Args:
        config_path (str)   : path to .yaml config file
        
    Returns:
        params_dict (dict)  : dict containing the parameters in config file
    '''
    # Load parameters file
    with open(config_path, 'r') as param_file:
        params_dict = yaml.load(param_file, Loader=yaml.FullLoader)
    
    return params_dict
    

def main():
    '''Starts main loop by initializing the Sherlock device.'''
    # Load configuration parameters
    sherlock_params_dict = read_yaml()
    
    # Initialize the device
    sherlock = Sherlock(**sherlock_params_dict)
    # Continue listening to events
    long_press_flag = False
    t_old = 0
    while True:

        pot_new = round(sherlock.potentiometer.value, 1)
        if(pot_new != sherlock.pot_old):
            sherlock._setVolume(pot_new)

        if(GPIO.input(sherlock.fw_pin) == GPIO.LOW):
            if(time.time() - t_old > sherlock.bounce):
                GPIO.output(sherlock.fw_led_pin, GPIO.HIGH)
                start = time.time()
                long_press_flag = False
                while(GPIO.input(sherlock.fw_pin) == GPIO.LOW):
                    duration = time.time() - start
                    if(duration > sherlock.long_press_time):
                        sherlock._fastforward()
                        long_press_flag = True
                        duration = 0
                        start = time.time()

                if(not long_press_flag):    
                    sherlock._forward()
                GPIO.output(sherlock.fw_led_pin, GPIO.LOW)
                t_old = time.time()
        
        if(GPIO.input(sherlock.bw_pin) == GPIO.LOW):
            if(time.time() - t_old > sherlock.bounce):
                GPIO.output(sherlock.bw_led_pin, GPIO.HIGH)
                while(GPIO.input(sherlock.bw_pin) == GPIO.LOW):
                    pass

                sherlock._backward()
                GPIO.output(sherlock.bw_led_pin, GPIO.LOW)
                t_old = time.time()   
        
        if(GPIO.input(sherlock.play_pin) == GPIO.LOW):
            if(time.time() - t_old > sherlock.bounce):
                GPIO.output(sherlock.play_led_pin, GPIO.HIGH)
                while(GPIO.input(sherlock.play_pin) == GPIO.LOW):
                    pass

                sherlock._play_pause()
                GPIO.output(sherlock.play_led_pin, GPIO.LOW)
                t_old = time.time()   

        if(GPIO.input(sherlock.switch_pin) == GPIO.LOW):
            if(time.time() - t_old > sherlock.bounce):
                sherlock._lamp_switch()
                while(GPIO.input(sherlock.switch_pin) == GPIO.LOW):
                    pass
                t_old = time.time()   

if __name__=='__main__':
    '''
    Wraps main loop in a try-except exception handling to catch 
    KeyboardInterrupt as quit event.
    '''
    try:    
        # Welcome message and instructions
        welcome_sherlock()
        # Start main loop
        main()
    # Catch CTRL+C command for quitting
    except KeyboardInterrupt:
        # Say goodbye
        goodbye_sherlock()
    # Deal elegantly with other errors and quit
    except Exception as ex:
        print('Encountered the following error: ', ex)
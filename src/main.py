import yaml

import RPi.GPIO as GPIO
import time

from sherlock import Sherlock
from utils import get_logger, welcome_sherlock


logger = get_logger()


def goodbye_sherlock():
    """Prints closing message for KeyboardInterrupt exception."""
    # Print goodbye
    print("#"*10)
    print("GOODBYE! COME BACK SOON! :)")
    print("#"*10)


def read_yaml(config_path="/home/pi/Desktop/Sherlock-dev/config/sherlock_parameters.yaml"):
    """
    Reads a .yaml file from the specified path. Returns a dict of parameters.
    
    Args:
        config_path (str)   : path to .yaml config file
        
    Returns:
        params_dict (dict)  : dict containing the parameters in config file
    """
    # Load parameters file
    with open(config_path, "r") as param_file:
        params_dict = yaml.load(param_file, Loader=yaml.FullLoader)
    
    return params_dict
    

def main():
    """Starts main loop by initializing the Sherlock device."""
    # Print welcome message
    welcome_sherlock(logger)

    # Load configuration parameters
    sherlock_params_dict = read_yaml()
    
    # Initialize the device
    sherlock = Sherlock(**sherlock_params_dict)
    # Continue listening to events
    long_press_flag = False
    t_old = 0
    while True:
        # Check volume level
        new_volume = round(sherlock.potentiometer.value, 1)
        if(new_volume != sherlock.prev_volume):
            sherlock._set_volume(new_volume)

        # Forward press = next track
        # Forward long-press = fast-forward current track
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
        
        # Backward press = restart track if after n seconds from start
        # Backward press = previous track if before n seconds from start
        if(GPIO.input(sherlock.bw_pin) == GPIO.LOW):
            if(time.time() - t_old > sherlock.bounce):
                GPIO.output(sherlock.bw_led_pin, GPIO.HIGH)
                while(GPIO.input(sherlock.bw_pin) == GPIO.LOW):
                    pass

                sherlock._backward()
                GPIO.output(sherlock.bw_led_pin, GPIO.LOW)
                t_old = time.time()   
        
        # Play button press = pause/play track
        if(GPIO.input(sherlock.play_pin) == GPIO.LOW):
            if(time.time() - t_old > sherlock.bounce):
                GPIO.output(sherlock.play_led_pin, GPIO.HIGH)
                while(GPIO.input(sherlock.play_pin) == GPIO.LOW):
                    pass

                sherlock._play_pause()
                GPIO.output(sherlock.play_led_pin, GPIO.LOW)
                t_old = time.time()   

        # Light switch press = turn on/off light/lamp
        if(GPIO.input(sherlock.switch_pin) == GPIO.LOW):
            if(time.time() - t_old > sherlock.bounce):
                sherlock._lamp_switch()
                while(GPIO.input(sherlock.switch_pin) == GPIO.LOW):
                    pass
                t_old = time.time()   


if __name__=="__main__":
    try:
        main()
    # Catch CTRL+C command for quitting
    except KeyboardInterrupt:
        # Say goodbye
        goodbye_sherlock()
    # Deal elegantly with other errors and quit
    except Exception as ex:
        print(f"Encountered the following error: {ex}. Exiting Sherlock session.")
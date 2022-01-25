import os
import yaml

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
    
def main():
    '''Starts main loop by initializing the Sherlock device.'''
    # Load parameters file
    with open('./config/sherlock_parameters.yaml', 'r') as param_file:
        sherlock_params_dict = yaml.load(param_file, Loader=yaml.FullLoader)
    
    # Initialize the device
    sherlock = Sherlock(**sherlock_params_dict)
    
    # Continue listening to events
    while True:
        pass    

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
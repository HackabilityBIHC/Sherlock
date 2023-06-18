"""Utilities for Sherlock's functioning."""
import logging
import sys
from pathlib import Path
from typing import Dict, Optional, Union

import yaml

def get_logger(name: str) -> logging.Logger:
    """Returns a python Logger object."""
    # Initialize logger and set options/formats
    logger = logging.getLogger(name)
    # Set level
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    # Format string
    formatter = logging.Formatter("[%(asctime)s - %(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def goodbye_sherlock(logger: Optional[logging.Logger] = None):
    """Prints exit message for KeyboardInterrupt exception."""
    message = """
        ###########################
        GOODBYE! COME BACK SOON! :)
        ###########################
    """

    logger.info(message) if logger else print(message)


def read_yaml(
        config_path: Union[str, Path] = Path("../config/sherlock_parameters.yaml")
    ) -> Dict:
    """Returns config parameters from a yaml file.
    
    Args:
        config_path (str, Path):
            Path to .yaml config file.
        
    Returns:
        A dict containing the parameters from the config file.
    """
    # Load parameters file
    with open(config_path, "r") as param_file:
        params_dict = yaml.load(param_file, Loader=yaml.FullLoader)
    
    return params_dict


def welcome_sherlock(logger: Optional[logging.Logger] = None):
    """Prints welcome and instructions for usage.
    
    Args:
        logger (logger.Logger, None):
            If specified, the logger to print to stdout.
    """
    message = """
        ####################
        WELCOME TO SHERLOCK!
        ####################

        I am your friendly concierge! My task is to help you navigate your surroundings
        and get familiar within this new space. 

        ############
        INSTRUCTIONS

        1. Press the right button (NEXT) to skip to the next track.
        2. Press the central button (PLAY/PAUSE) to play/pause the current track.
        3. Press the left button (LEFT) to go back to the previous track.
        4. Long-press the right button (NEXT) to fast-forward the current track.

        #############

        Have fun! :)
    """

    logger.info(message) if logger else print(message)
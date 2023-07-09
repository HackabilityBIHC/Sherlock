from sherlock import Sherlock
from utils import get_logger, goodbye_sherlock, read_yaml, welcome_sherlock


logger = get_logger(__name__)

def main():
    """Starts main loop by initializing the Sherlock device."""
    try:
        # Print welcome message
        welcome_sherlock(logger)

        # Load configuration parameters
        # TODO: Make path non-hardcoded
        sherlock_params_dict = read_yaml()
        # Add logger
        sherlock_params_dict.update({"logger": logger})
        
        # Initialize the device
        sherlock = Sherlock(**sherlock_params_dict)
        
        # Start playback
        sherlock.run(logger)

    # Catch CTRL+C command from CLI
    except KeyboardInterrupt:
        # Say goodbye and exit
        goodbye_sherlock(False, logger)
    # Catch any other exception gracefully
    except Exception as ex:
        logger.info(f"Encountered the following error: {ex}.")
        logger.info(f"Closing Sherlock session...")
        goodbye_sherlock(True, logger)


if __name__=="__main__":
    main()
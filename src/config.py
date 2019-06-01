# Chessboard Configuration

import logging
import os

# Project location, don't change this:
SRC_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.join(SRC_DIR, '../')

SHUTDOWN_AT_END = False # Shutdown pi at end of program
RESTART_ON_CRASH = True # Restart when program crashes
MAXIMUM_CRASHES = 2 # Maximum number of restarts

BUTTON_PRESS_DELAY = 0.4 # Delay after pressing a button. Should be greater than 0.3

PROCESS_NAME = 'open-magic-chess'

INTRO_DELAY = 1.5 # How long each part of the intro lasts
RESTART_DELAY = 10 # How long it takes to restart
SHUTDOWN_DELAY = 2 # How long the shutdown message shows for

LOGGING_LEVEL = logging.INFO # Minimum level for logging messages stored in logs
LOGGING_FORMAT = '%(asctime)-10s OPEN-MAGIC-CHESS |%(levelname)s: %(message)s' # Log message format
LOGGING_DATE_FORMAT = '%m-%d %H:%M:%S' # Log message date format
LOGGING_BACKUP_COUNT = 3 # Number of log files
LOG_FILE_MAX_BYTES = 6000 # Max bytes per log file

DISPLAY_UPDATE_DELAY = 0.5
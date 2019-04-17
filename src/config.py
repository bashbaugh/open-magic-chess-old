# Chessboard Configuration

import logging
import os

SRC_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.join(SRC_DIR, '../')

SHUTDOWN_AT_END = False

RESTART_ON_CRASH = True
MAXIMUM_CRASHES = 2

BUTTON_PRESS_DELAY = 0.4

LOADING_DELAY = 1
RESTART_DELAY = 11

LOGGING_LEVEL = logging.INFO
LOGGING_FORMAT = '%(asctime)-10s OPEN-MAGIC-CHESS |%(levelname)s: %(message)s'
LOGGING_DATE_FORMAT = '%m-%d %H:%M:%S'
LOGGING_BACKUP_COUNT = 3
LOG_FILE_MAX_BYTES = 6000
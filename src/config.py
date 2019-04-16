# Chessboard Configuration

import logging
import os

SRC_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.join(SRC_DIR, '../')

USE_KEYBOARD = True

SHUTDOWN_AT_END = False

RESTART_ON_CRASH = True
MAXIMUM_CRASHES = 2

LOADING_DELAY = 0.4

LOGGING_LEVEL = logging.DEBUG
LOGGING_FORMAT = '%(asctime)-10s OPEN-MAGIC-CHESS |%(levelname)s: %(message)s'
LOGGING_DATE_FORMAT = '%m-%d %H:%M'
LOGGING_BACKUP_COUNT = 5
LOG_FILE_MAX_BYTES = 6000
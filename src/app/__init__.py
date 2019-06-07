"""The app server
"""

from multiprocessing import Process
import logging
from logging.handlers import RotatingFileHandler

import app._app

import config as cfg

logging_handler = RotatingFileHandler(cfg.BASE_DIR + 'logs/chess_app.log', maxBytes=cfg.LOG_FILE_MAX_BYTES, backupCount=cfg.LOGGING_BACKUP_COUNT)
logging_formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
logging_handler.setLevel(cfg.LOGGING_LEVEL)
logging_handler.setFormatter(logging_formatter)

server = None

def run_app():
    global server
    server = Process(target=_app.start, args=(logging_handler,))
    server.start()
    
def stop_app():
    global server
    server.terminate()
    server.join()
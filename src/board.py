"""Open Magic Chess
High tech chessboard

https://github.com/scitronboy/open-magic-chess

Copyright 2019 Benjamin A. and contributors
Licensed under MIT license, located in /LICENSE
"""

from time import sleep, time

import config as cfg

def intro(loading=False, delay=cfg.INTRO_DELAY):
    lcd.clear()
    lcd.display_string("Open magic chess", 1)
    if loading:
        lcd.display_string("Loading...", 2)
        sleep(delay * 1.5)
    else:
        lcd.display_string("Please wait...  ", 2)
    sleep(delay)

from parts import lcd_driver
lcd = lcd_driver.Serial_lcd()
intro(loading=True)

from threading import Thread
import traceback
import logging
from logging.handlers import RotatingFileHandler
from setproctitle import *
import socket
import os
from math import floor

import chess
import chess.engine

from constants import *
from parts import controls, board_sensor, actuator, leds
import app
import menu

# Set process name so that it can be easily found and killed:
setproctitle(cfg.PROCESS_NAME)

# Create logs and saves directory:
if not os.path.isdir(cfg.BASE_DIR + 'logs'):
    os.mkdir(cfg.BASE_DIR + 'logs')
if not os.path.isdir(cfg.BASE_DIR + 'data'):
    os.mkdir(cfg.BASE_DIR + 'data')

# Logging
logging_formatter = logging.Formatter(cfg.LOGGING_FORMAT, cfg.LOGGING_DATE_FORMAT)

logging_sh = logging.StreamHandler()
logging_sh.setLevel(logging.DEBUG)
logging_sh.setFormatter(logging_formatter)

logging_rfh = RotatingFileHandler(cfg.BASE_DIR + 'logs/chessboard.log', maxBytes=cfg.LOG_FILE_MAX_BYTES, backupCount=cfg.LOGGING_BACKUP_COUNT)
logging_rfh.setLevel(cfg.LOGGING_LEVEL)
logging_rfh.setFormatter(logging_formatter)

logger = logging.getLogger("chess-logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging_sh)
logger.addHandler(logging_rfh)
logger.debug("--- Logger started ---")

crash_counter = 0
    

class Board:
    """ Magic chess board
    """
    
    def __init__(self, lcd):
        self.menu_stack = [menu.MAIN_MENU]
        self.co = 0 # current menu option
        self.game = None
        self.status = IN_MENU
        
        # Parts
        # If you want to use a customized part just replace any of these class names with your own.
        self.lcd = lcd
        self.led = leds.Neopixel_RGB_LEDs(self.log_warning)
        self.controls = controls.Keyboard_controls()
        self.grid = board_sensor.Reedswitch_grid_sensor()
        self.actuator = actuator.Stepper_actuator()
        
        # In-game variables
        self.white_clock_time = None
        self.black_clock_time = None
        self.last_update = 0
        self.ptype = None # Current player type
        self.last_BWcolors = ("off", "off")
        
        # Game options
        self.mode = None
        self.flip_board = None
        self.white_type = None
        self.black_type = None
        self.player_color = None
        self.engine_time_limit = None
        self.use_clock = None
        self.clock_time = None
        self.clock_time_increment = None
        
        # Engine
        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish")
        self.engine_process = None
        self.engine_results =  []
        
        # App
        app.run_app()
        
        self.led.rainbow(40)
        logger.info("Board initialized")
            
            
    def main(self):
        try:
            while self.status is not SHUTDOWN:
                
                if self.status == IN_MENU or self.status == GAME_PAUSED:
                    self.run_menu()
                elif self.status == IN_GAME:
                    self.run_game()
                    
                sleep(0.05)
        except KeyboardInterrupt:
            logger.debug("Keyboard Interrupt")
            self.shutdown()
        
    def run_menu(self):
        if self.status is not GAME_PAUSED:
            cm = self.menu_stack[-1] # Current Menu
        else:
            cm = menu.PAUSE_MENU
        
        # MENU.optionl1 is a constant first line message for that menu
        if cm.optionl1 is None:
            self.lcd.disp_two_lines(cm.options[self.co])
        else:
            self.lcd.clear()
            self.lcd.display_string(cm.optionl1, 1)
            self.lcd.display_string(cm.options[self.co], 2)
        
        back, yes, no = self.controls.buttons()
        while not (back or yes or no):
            back, yes, no = self.controls.buttons()
        sleep(cfg.BUTTON_PRESS_DELAY)
        if back:
            self.co = 0
            if len(self.menu_stack) > 1 and self.status is not GAME_PAUSED:
                del self.menu_stack[-1]
        
        if no:
            self.co += 1
            if len(cm.options) == 1:
                cm.no(self)
            if self.co >= len(cm.options):
                self.co = 0
        
        if yes:
            cm.yes(self)
            self.co = 0
            
    def run_game(self):
        # Check for pause command
        back, yes, no = self.controls.buttons()
        if (back or yes or no):
            self.status = GAME_PAUSED
            return
        
        # Update display if a second has passed
        if time() - self.last_update >= cfg.DISPLAY_UPDATE_DELAY:
            self.game_display()
            self.last_update = time()
        
        # Check for moves
        if self.ptype == PLAYER_MACHINE:
            if self.engine_process.isAlive() or self.engine_process is None:
                return
            self.process_move(engine_results[-1].move)
            if not self.actuator.move(engine_results[-1].move):
                self.confirm("Unable to move", "Check Logs")
        elif ptype == PLAYER_HUMAN:
            self.grid.update()
            if not self.piece_moved():
                return
            
        
        ptype = (self.white_type if self.game.turn == chess.WHITE else self.black_type) # player type
        
        sleep(20)
            
    def game_display(self):
        BWcolors = ("green,", "off") if self.game.turn == chess.BLACK else ('off', 'green')
        if BWcolors != self.last_BWcolors:
            self.led.colorBW(*BWcolors)
            self.last_BWcolors = BWcolors
        self.lcd.disp_two_lines([str(floor(time())), str(self.game.turn)])
        
    def clear_board(self):
        self.game = chess.Board()
            
    def save_game(self):
        logger.info("Saving game")
    
    @staticmethod
    def intro(*args):
        intro(args)
    
    def check_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            hostname = s.getsockname()[0]
            self.confirm("Local IP is:", hostname)
        except OSError:
            self.confirm("Network", "Unreachable")
        finally:
            s.close()
                
    def move_piece(self, move):
        self.lcd.disp_two_lines(["Moving", str(move)])
        sleep(2)
            
    def play_engine(self):
        result = self.engine.play(self.game, chess.engine.Limit(time=self.engine_time_limit))
        self.engine_results.append(result)
        
    def start_game(self):
        if self.mode == MODE_PVB:
            self.white_type = PLAYER_HUMAN if self.player_color == chess.WHITE else PLAYER_MACHINE
        
        self.led.color('light_orange')
        while True:
            self.lcd.disp_two_lines([" Setup board ", ""])
            sleep(2)
            break
        
        self.led.color('violet')
        if self.confirm("   Press yes", " to start game"):
            self.start_turn = True
            self.status = IN_GAME
            logger.info("Starting %s game", self.mode)
            
    def confirm(self, l1, l2):
        self.lcd.disp_two_lines([l1, l2])
        back, yes, no = self.controls.buttons()
        while not (back or yes or no):
            back, yes, no = self.controls.buttons()
        sleep(cfg.BUTTON_PRESS_DELAY)
        return True if yes else False
        
    @staticmethod
    def log_warning(msg):
        logger.warning(msg)

    def shutdown(self):
        self.lcd.disp_two_lines(["Allow 15 seconds", "  for shutdown"])
        sleep(cfg.SHUTDOWN_DELAY)
        self.lcd.clear()
        self.lcd.backlight(False)
        self.led.shutdown()
        self.status = SHUTDOWN
            

def start():
    global crash_counter
    try:
        board = Board(lcd)
        board.main()
    except Exception as e:
            
        crash_counter += 1
        
        logger.error("Program crashed")
        logger.critical(traceback.format_exc())
        if crash_counter >= cfg.MAXIMUM_CRASHES:
            logger.warning("Maximum crashes reached. Stopping.")
            lcd.disp_two_lines([" Board crashed", "  Check logs"])
            return
        
        if cfg.RESTART_ON_CRASH:
            logger.info("Restarting...")
            try:
                lcd.disp_two_lines([" Board crashed", " Restarting..."])
            except:
                logger.error("Failed to write to LCD")
            sleep(cfg.RESTART_DELAY / 2)
            intro(delay = cfg.RESTART_DELAY / 2)
            start()

if __name__ == "__main__":
    start()

if cfg.SHUTDOWN_AT_END:
    logger.info("Shutting Down")
    os.system("sudo shutdown -h now")

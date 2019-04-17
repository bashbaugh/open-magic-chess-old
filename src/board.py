"""Open Magic Chess
High tech chessboard.

https://github.com/scitronboy/open-magic-chess

Copyright 2019 Benjamin A. and contributors
Licensed under MIT license, located in /LICENSE
"""

import config as cfg

from parts import lcd_driver
lcd = lcd_driver.Serial_lcd()
lcd.clear()
lcd.disp_two_lines(["  Loading....", "Open Magic Chess"])


from time import sleep
from threading import Thread
import traceback
import logging
from logging.handlers import RotatingFileHandler
import socket
import os

import chess
import chess.engine
from parts import controls, board_sensor, mover
import menu

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

logger = logging.getLogger("omc-logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging_sh)
logger.addHandler(logging_rfh)
logger.info("--- Logger started ---")

crash_counter = 0

# CONSTANTS
GAME_MODES = [MODE_PVB, MODE_PVP, MODE_BVB] = 'PVB', 'PVP', 'BVB'

BOARD_STATUSES = [IN_MENU, IN_GAME, GAME_PAUSED, SHUTDOWN] = "in menu", "in game", "game paused", "shutting down"

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
        self.controls = controls.Keyboard_controls()
        self.grid = board_sensor.Reedswitch_grid_sensor()
        self.mover = mover.Gearmotor_movement()
        
        # In-game variables
        self.just_moved = True
        self.white_clock = 0
        self.black_clock = 0
        
        # Game options
        self.mode = None
        self.flip_board = None
        self.player_color = None
        self.engine_time_limit = None
        self.use_clock = None
        self.clock_time = None
        self.clock_time_increment = None
        
        # Engine
        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish")
        self.engine_results =  []
        
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
        self.game_display()
        if self.mode == MODE_PVB:
            if self.game.turn == self.player_color:
                pass
            else:
                if self.just_moved:
                    self.engine_process = Thread(target=self.play_engine)
                    self.lcd.disp_two_lines(["Thinking...", ""])
                    self.engine_process.start()
                    self.just_moved = False
                elif not self.engine_process.isAlive():
                    self.game.push(self.engine_results[-1].move)
                    self.move_piece(self.game.peek())
                    self.just_moved = True
                    self.lcd.disp_two_lines(["Your Turn", ""])
                    
        back, yes, no = self.controls.buttons()
        if True in (back, yes, no):
            self.status = GAME_PAUSED
            
    def clear_board(self):
        self.game = chess.Board()
            
    def game_display(self, redraw=False):
        pass
            
    def save_game(self):
        pass
    
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
        set_up = False
        while not set_up:
            set_up = True
        
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
        
    def shutdown(self):
        self.lcd.disp_two_lines(["Allow 15 seconds", "  for shutdown"])
        sleep(3)
        self.lcd.clear()
        self.lcd.backlight(False)
        self.status = SHUTDOWN
            

def start():
    global crash_counter
    sleep(cfg.LOADING_DELAY) # Just to show off the loading screen!
    try:
        board = Board(lcd)
        board.main()
    except Exception as e:
            
        crash_counter += 1
        
        logger.error("Program crashed")
        logger.critical(traceback.format_exc())
        if crash_counter >= cfg.MAXIMUM_CRASHES:
            logger.warning("Max crashes reached. Stopping.")
            lcd.disp_two_lines([" Board crashed", "  Check logs"])
            return
        
        if cfg.RESTART_ON_CRASH:
            logger.info("Restarting...")
            try:
                lcd.disp_two_lines([" Board crashed", " Restarting..."])
            except:
                logger.error("Failed to write to LCD")
            sleep(cfg.RESTART_DELAY)
            start()
    
    if cfg.SHUTDOWN_AT_END:
        os.system("sudo shutdown -h now")

start()
logger.info("Program finished\n")

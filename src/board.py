"""Open Magic Chess
High tech chessboard.

https://github.com/scitronboy/open-magic-chess

Copyright 2019 Benjamin A. and contributors
"""

import config as cfg

from parts import lcd_driver
lcd = lcd_driver.Default_lcd()
lcd.clear()
lcd.disp_two_lines(["Magic Chessboard", "Loading..."])
#lcd.backlight(True)

if cfg.USE_KEYBOARD:
    import keyboard
from time import sleep
from threading import Thread
import traceback
import logging
from logging.handlers import RotatingFileHandler
import socket
import os
import chess
import chess.engine

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


crash_counter = 0

# CONSTANTS
GAME_MODES = [MODE_PVB, MODE_PVP, MODE_BVB] = 0,1,2

BOARD_STATUSES = [IN_MENU, IN_GAME, GAME_PAUSED, SHUTDOWN] = 0, 1, 2, 3

class Board:
    """ Magic chess board
    """
    
    def __init__(self, lcd):
        self.lcd = lcd
        self.menu_stack = [MAIN_MENU]
        self.co = 0 # current menu option
        self.game = None
        self.status = IN_MENU
        
        # In-game variables
        self.start_turn = True
        self.white_clock = 0
        self.black_clock = 0
        
        # Game options
        self.mode = None
        self.flip_board = None
        self.player_color = None
        self.engine_time_limit = None
        
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
            self.shutdown()
        
    def run_menu(self):
        if self.status is not GAME_PAUSED:
            cm = self.menu_stack[-1] # Current Menu
        else:
            cm = PAUSE_MENU
        
        if cm.optionl1 is None:
            self.lcd.disp_two_lines(cm.options[self.co])
        else:
            self.lcd.clear()
            self.lcd.display_string(cm.optionl1, 1)
            self.lcd.display_string(cm.options[self.co], 2)
        
        back, yes, no = self.buttons()
        while not (back or yes or no):
            back, yes, no = self.buttons()
        sleep(0.5)
        if back:
            self.co = 0
            if len(self.menu_stack) > 1 and self.status is not GAME_PAUSED:
                del self.menu_stack[-1]
        
        if no:
            self.co += 1
            if len(cm.options) == 1:
                cm.no(self)
                cm.next_menu(self)
            if self.co >= len(cm.options):
                self.co = 0
        
        if yes:
            cm.yes(self)
            if len(cm.options) == 1:
                cm.next_menu(self)
            self.co = 0
            
    def run_game(self):
        self.game_display()
        if self.mode == MODE_PVB:
            if self.game.turn == self.player_color:
                pass
            else:
                if self.start_turn:
                    self.engine_process = Thread(target=self.play_engine)
                    self.lcd.disp_two_lines(["Thinking...", ""])
                    self.engine_process.start()
                    self.start_turn = False
                elif not self.engine_process.isAlive():
                    self.game.push(self.engine_results[-1].move)
                    self.move_piece(self.game.peek())
                    self.start_turn = True
                    self.lcd.disp_two_lines(["Your Turn", ""])
                    
        back, yes, no = self.buttons()
        if True in (back, yes, no):
            self.status = GAME_PAUSED
            
    def game_display(self, redraw=False):
        pass
            
    def save_game(self):
        pass
                
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
            
    def confirm(self, l1, l2):
        self.lcd.disp_two_lines([l1, l2])
        back, yes, no = self.buttons()
        while not (back or yes or no):
            back, yes, no = self.buttons()
        sleep(0.2)
        return True if yes else False

    def buttons(self):
        if cfg.USE_KEYBOARD:
            return keyboard.is_pressed('b'), keyboard.is_pressed('y'), keyboard.is_pressed('n')
        else:
            pass
        
    def shutdown(self):
        gpio.cleanup()
        print("Bye")
        self.lcd.disp_two_lines(["Allow 15 seconds", "  for shutdown"])
        sleep(3)
        self.lcd.clear()
        self.lcd.backlight(False)
        self.status = SHUTDOWN
        
# Menus
class MAIN_MENU:
    optionl1 = None
    options = [["Create New Game:", "Player VS Board"],
                ["Create New Game:", "Player VS Player"],
                ["Create New Game:", "Board VS Board"],
                ["   Load Game", ""],
                ["    Shutdown", ""],
                [" Get Local IP", ""],]
    
    def yes(board):
        if board.co == 3:
            board.menu_stack.append(LOAD_GAME_MENU)
        elif board.co == 4:
            if board.confirm(" Are You Sure?", ""):
                board.shutdown()
        elif board.co == 5:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(('10.255.255.255', 1))
                hostname = s.getsockname()[0]
                board.confirm("Local IP is:", hostname)
            except OSError:
                board.confirm("Network", "Unreachable")
            finally:
                s.close()
        else:
            board.mode = board.co
            board.game = chess.Board()
            board.menu_stack.append(CHOOSE_WHITE_SIDE_MENU)
            print(board.mode)
                
class PAUSE_MENU:
    optionl1 = "--Game Paused--"
    options = ["Continue Game?", "Save Game?", "Cancel Game?"]
    
    def yes(board):
        if board.co == 0:
            board.status = IN_GAME
            board.game_display(redraw=True)
        elif board.co == 1:
            board.save_game()
        elif board.co == 2:
            if board.confirm(" Are You Sure?", ""):
                board.status = IN_MENU
                board.menu_stack = [MAIN_MENU]
                
class CHOOSE_WHITE_SIDE_MENU:
    optionl1 = None
    options = [["Flip board y/n:", "White At Front?"]]
    
    def yes(board):
        board.flip_board = True
        
    def no(board):
        board.flip_board = False
        
    def next_menu(board):
        board.game = chess.Board()
        if board.mode == MODE_PVB:
            board.menu_stack.append(CHOOSE_COLOR_MENU)
        else:
            board.confirm("Feature", "Unavailable")

class CHOOSE_COLOR_MENU:
    optionl1 = None
    options = [["  Do you want", "  to be white?"]]
    
    def yes(board):
        board.player_color = chess.WHITE
        
    def no(board):
        board.player_color = chess.BLACK
        
    def next_menu(board):
        board.menu_stack.append(CHOOSE_ENGINE_TIME_LIMIT_MENU)

class LOAD_GAME_MENU:
    optionl1 = None
    options = [["Choose Game:", "no games"]]
    
class CHOOSE_ENGINE_TIME_LIMIT_MENU:
    optionl1 = "AI time limit:"
    options = ["0.1 seconds", "1 second", "10 seconds", "1 minute"]
    
    def yes(board):
        co = board.co
        tl = 0
        
        if co == 0:
            tl = 0.1
        elif co == 1:
            tl = 1
        elif co == 2:
            tl = 10
        elif co == 3:
            tl = 60
        
        board.engine_time_limit = tl
        board.start_game()
            

def start():
    global crash_counter
    sleep(cfg.LOADING_DELAY) # Just to show off the loading screen!
    try:
        board = Board(lcd)
        board.main()
    except Exception as e:
        if e == "KeyboardInterrupt":
            logger.info("KeyboardInterrupt")
            return
            
        crash_counter += 1
        
        logger.error("Program crashed")
        logger.critical(traceback.format_exc())
        if crash_counter >= cfg.MAXIMUM_CRASHES:
            logger.warning("Max crashes reached. Stopping.")
            lcd.disp_two_lines([" Board crashed", "  Check logs"])
            return
        
        if cfg.RESTART_ON_CRASH:
            logger.warning("Restarting...")
            try:
                lcd.disp_two_lines([" Board crashed", " Restarting..."])
            except:
                logger.error("Failed to write to LCD")
            sleep(cfg.LOADING_DELAY + 5)
            start()
    
    if cfg.SHUTDOWN_AT_END:
        os.system("sudo shutdown -h now")

start()
logger.info("Program finished")

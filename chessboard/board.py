"""Magic Chess Board
Play an AI on a real board

https://github.com/scitronboy/open-magic-chess

Written by Benjamin A.
"""

USE_KEYBOARD = True
SHUTDOWN_AT_END = False

import lcd_driver
lcd = lcd_driver.lcd()
lcd.clear()
lcd.disp_two_lines(["Magic Chessboard", "Loading..."])
#lcd.backlight(True)

if USE_KEYBOARD:
    import keyboard 
from time import sleep
from threading import Thread
import os
import RPi.GPIO as gpio
import chess
import chess.engine
#import menu

# PINS
OUTPUTS = [
    WHITE_LED_RED,
    WHITE_LED_GREEN,
    WHITE_LED_BLUE,
    BLACK_LED_RED,
    BLACK_LED_GREEN,
    BLACK_LED_BLUE,
] = [0,0,0,0,0,0]

REED_OUT = [0,0,0,0,0,0,0,0]
REED_IN = [0,0,0,0,0,0,0,0]

INPUTS = [
    BUTTON_BACK,
    BUTTON_YES,
    BUTTON_NO,
] = [0,0,0]

# CONSTANTS
GAME_MODES = [MODE_PVB, MODE_PVP, MODE_BVB] = 0,1,2

    
class Board:
    """ Magic chess board
    """
    
    def __init__(self, lcd):
        self.lcd = lcd
        self.menu_stack = [MAIN_MENU]
        self.co = 0 # current option
        self.active = True
        self.game = None
        
        # Game options
        self.mode = None
        self.player_color = None
        self.engine_time_limit = None
        
        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish")
        
        gpio.setmode(gpio.BCM)
        for pin in OUTPUTS + REED_OUT:
            gpio.setup(pin, gpio.OUT)
            
        for pin in INPUTS + REED_IN:
            gpio.setup(pin, gpio.IN)
            
            
    def main(self):
        try:
            while True:
                if not self.active:
                    break
                self.run_menu()
        except KeyboardInterrupt:
            self.shutdown()
        
    def run_menu(self):
        cm = self.menu_stack[-1] # Current Menu
        
        if not cm.optionl1:
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
            if len(self.menu_stack) > 1:
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
            
    def getPlay(board, result):
        result = engine.play(board, chess.engine.Limit(time=1))
        board.push(result.move)
        print(str(board.peek()))
            
    def confirm(self, l1, l2):
        self.lcd.disp_two_lines([l1, l2])
        back, yes, no = self.buttons()
        while not (back or yes or no):
            back, yes, no = self.buttons()
        return True if yes else False

    def buttons(self):
        if USE_KEYBOARD:
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
        self.active = False
        
# Menus    
class MAIN_MENU:
    optionl1 = False
    options = [["Create New Game:", "Player VS Board"], 
                ["Create New Game:", "Player VS Player"],
                ["Create New Game:", "Board VS Board"],
                ["   Load Game", ""],
                ["    Shutdown", ""]]
    def yes(board):
        if board.co == 3:
            board.menu_stack.append(LOAD_GAME_MENU)
        elif board.co == 4:
            if board.confirm(" Are You Sure?", ""):
                board.shutdown()
        else:
            board.mode = board.co
            board.game = chess.Board()
            board.menu_stack.append(CHOOSE_WHITE_SIDE_MENU)
            print(board.mode)
                
class CHOOSE_WHITE_SIDE_MENU:
    optionl1 = False
    options = [["Flip board y/n:", "White At Front?"]]
    
    def yes(board):
        board.game = chess.Board().mirror()
        
    def no(board):
        board.game = chess.Board()
        
    def next_menu(board):
        if board.mode == MODE_PVB:
            board.menu_stack.append(CHOOSE_COLOR_MENU)
        elif board.mode == MODE_PVP:
            pass
        else:
            board.confirm("Feature", "Unavailable")

class CHOOSE_COLOR_MENU:
    optionl1 = False
    options = [["  Do you want", "  to be white?"]]
    
    def yes(board):
        board.player_color = chess.WHITE
        
    def no(board):
        board.player_color = chess.BLACK
        
    def next_menu(board):
        board.menu_stack.append(CHOOSE_ENGINE_TIME_LIMIT_MENU)

class LOAD_GAME_MENU:
    optionl1 = False
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
        board.wait_for_setup()
    
            
    
board = Board(lcd)
board.main()


if SHUTDOWN_AT_END:
    os.system("sudo shutdown -h now")






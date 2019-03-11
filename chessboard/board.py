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
import socket
import os
import RPi.GPIO as gpio
import chess
import chess.engine
#import menu

# PINS
# SDA = 2; SCL = 3
OUTPUTS = [
    LED_RED,
    LED_GREEN,
    LED_BLUE,
    MOTOR_LEFT,
    MOTOR_RIGHT,
    MOTOR_UP,
    MOTOR_DOWN,
] = [0,0,0,0,0,0,0]

REED_OUT = [0,0,0,0,0,0,0,0]
REED_IN = [0,0,0,0,0,0,0,0]

INPUTS = [
    BUTTON_BACK,
    BUTTON_YES,
    BUTTON_NO,
] = [0,0,0]

# CONSTANTS
GAME_MODES = [MODE_PVB, MODE_PVP, MODE_BVB] = 0,1,2

BOARD_STATUSES = [IN_MENU, IN_GAME, GAME_PAUSED, SHUTDOWN] = 0, 1, 2, 3

    
class Board:
    """ Magic chess board
    """
    
    def __init__(self, lcd):
        self.lcd = lcd
        self.menu_stack = [MAIN_MENU]
        self.co = 0 # current option
        self.game = None
        self.status = IN_MENU
        self.start_turn = True
        
        # Game options
        self.mode = None
        self.flip_board = None
        self.player_color = None
        self.engine_time_limit = None
        
        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish")
        self.engine_results =  []
        
        gpio.setmode(gpio.BCM)
        for pin in OUTPUTS + REED_OUT:
            gpio.setup(pin, gpio.OUT)
            
        for pin in INPUTS + REED_IN:
            gpio.setup(pin, gpio.IN)
            
            
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
                # doesn't even have to be reachable
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
    
            
    
board = Board(lcd)
#sleep(0.5)
board.main()

if SHUTDOWN_AT_END:
    os.system("sudo shutdown -h now")
    
    

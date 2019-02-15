"""Magic Chess Board
Play an AI on a real board

https://github.com/scitronboy/open-magic-chess

Written by Benjamin A.
"""

import lcd_driver
lcd = lcd_driver.lcd()
lcd.clear()
lcd.display_string("Magic Chessboard", 1)
lcd.display_string("loading...", 2)

from time import sleep
import RPi.GPIO as gpio
import chess
import chess.engine
#import menu

# Pins:
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

gpio.setmode(gpio.BCM)
    
class Board:
    """ The magic chess board
    """
    
    def __init__(self, lcd):
        self.lcd = lcd
        self.menu_stack = [Menu.MAIN_MENU]
        for pin in OUTPUTS + REED_OUT:
            gpio.setup(pin, gpio.OUT)
            
        for pin in INPUTS + REED_IN:
            gpio.setup(pin, gpio.IN)
            
    def main(self):
        try:
            while True:
                self.runmenu()
        except KeyboardInterrupt:
            self.shutdown()
        
    def runmenu(self):
        m = self.menu_stack[-1]
        if m == Menu.MAIN_MENU:
            self.lcd.disp_two_lines(m.options[0])
            sleep(5)

    def shutdown(self):
        self.lcd.clear()
        gpio.cleanup()
        
class Menu:
    """ Menu data
    """
    class MAIN_MENU:
        options = [["Create New Game:", "Player VS Board"], 
                   ["Create New Game:", "Player VS Player"],
                   ["Create New Game:", "Board VS Board"],
                   ["Load Game", ""],
                   ["Shutdown", ""]]
    
    
board = Board(lcd)
sleep(1)
board.main()

board.shutdown()
print("Exit")







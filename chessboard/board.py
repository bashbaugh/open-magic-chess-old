"""Magic Chess Board
Play an AI on a real board

https://github.com/scitronboy/open-magic-chess

Written by Benjamin A.
"""

import lcd_driver
lcd = lcd_driver.lcd()
lcd.lcd_clear()
lcd.lcd_display_string("Magic Chessboard", 1)

from time import sleep
import RPi.GPIO as gpio
import chess
import chess.engine
import menu

# Pins:
OUTPUTS = [
    WHITE_LED_RED,
    WHITE_LED_GREEN,
    WHITE_LED_BLUE,
    BLACK_LED_RED,
    BLACK_LED_GREEN,
    BLACK_LED_BLUE
] = [0,0,0,0,0,0]

INPUTS = [
    TEST
] = [0]

gpio.setmode(gpio.BCM)

for pin in OUTPUTS:
    gpio.setup(pin, gpio.OUT)
    
for pin in INPUTS:
    gpio.setup(pin, gpio.IN)
    
    
lcd.lcd_clear()
gpio.cleanup()
print("Exit")








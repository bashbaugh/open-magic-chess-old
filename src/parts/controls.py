"""Controls for the chessboard

buttons() - returns a tuple of buttons that are pressed: (b)ack, (y)es, (n)o

"""

# If you would like to add more control types just add another class below.

import keyboard
from gpiozero import Button
    
class Keyboard_controls:
    """ Keyboard control library for development on Raspberry pi.
    Note that it wasn't working over SSH for me
    """
    def __init__(self):
        pass
    
    def buttons(self):
        return keyboard.is_pressed('b'), keyboard.is_pressed('y'), keyboard.is_pressed('n')
        
class Basic_buttons:
    """Basic GPIO button controls"""
    # button pins (BCM GPIO numbering)
    YES_BUTTON_PIN = 17 
    NO_BUTTON_PIN = 27
    BACK_BUTTON_PIN = 22

    def __init__(self):
        self.b_btn = Button(BACK_BUTTON_PIN)
        self.y_btn = Button(YES_BUTTON_PIN)
        self.n_btn = Button(NO_BUTTON_PIN)

    def buttons(self):
        # return button states
        return self.b_btn.is_pressed, self.y_btn.is_pressed, self.n_btn.is_pressed


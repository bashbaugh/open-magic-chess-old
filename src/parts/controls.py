"""Controls for the chessboard

buttons() - returns a tuple of buttons that are pressed: (b)ack, (y)es, (n)o

"""

# If you would like to add more controls just add another class below.

import keyboard
import gpiozero
    
class Keyboard_controls:
    def __init__(self):
        pass
    
    def buttons(self):
        return keyboard.is_pressed('b'), keyboard.is_pressed('y'), keyboard.is_pressed('n')
        
class Basic_buttons:
    def __init__(self):
        pass
    
# class Base_controls:
#     def __init__():
#         pass
    
#     def
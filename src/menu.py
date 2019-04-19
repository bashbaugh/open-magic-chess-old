"""Menus
"""
from time import sleep

import chess

from constants import *

class MAIN_MENU:
    optionl1 = None
    options = [["Create New Game", ""],
                ["   Load Game", ""],
                ["    Shutdown", ""],
                [" Get Local IP", ""]]
    
    def yes(board):
        if board.co == 0:
            board.menu_stack.append(CHOOSE_GAME_TYPE_MENU)
        elif board.co == 1:
            board.menu_stack.append(LOAD_GAME_MENU)
        elif board.co == 2:
            if board.confirm(" Are You Sure?", ""):
                board.shutdown()
        elif board.co == 3:
            board.check_local_ip()
            
class CHOOSE_GAME_TYPE_MENU:
    optionl1 = "Choose type:"
    options = ["Player vs Player",
                "Player vs Board",
                "Board vs board"]
    
    def yes(board):
        if board.co == 0:
            board.mode = MODE_PVP
        elif board.co == 1:
            board.mode = MODE_PVB
        else:
            board.mode = MODE_BVB
        
        board.menu_stack.append(CHOOSE_WHITE_SIDE_MENU)
        
                
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
                board.intro()
                sleep(0.5)
                
class CHOOSE_WHITE_SIDE_MENU:
    optionl1 = None
    options = [["Flip board y/n:", "White At Front?"]]
    
    def yes(board):
        board.flip_board = True
        CHOOSE_WHITE_SIDE_MENU.next_menu(board)
        
    def no(board):
        board.flip_board = False
        CHOOSE_WHITE_SIDE_MENU.next_menu(board)
        
    def next_menu(board):
        board.clear_board()
        if board.mode == MODE_PVB:
            board.menu_stack.append(CHOOSE_COLOR_MENU)
        else:
            board.confirm("Feature", "Unavailable")

class CHOOSE_COLOR_MENU:
    optionl1 = None
    options = [["  Do you want", "  to be white?"]]
    
    def yes(board):
        board.player_color = chess.WHITE
        board.menu_stack.append(USE_CLOCK_MENU)
        
    def no(board):
        board.player_color = chess.BLACK
        board.menu_stack.append(CHOOSE_ENGINE_TIME_LIMIT_MENU)

class LOAD_GAME_MENU:
    optionl1 = None
    options = [["Choose Game:", "no games"]]
    
class CHOOSE_ENGINE_TIME_LIMIT_MENU:
    optionl1 = "AI time limit:"
    options = ["0.1 seconds", "1 second", "10 seconds", "1 minute"]
    
    def yes(board):
        durations = {0: 0.1, 1: 1, 2: 10, 3: 60}
        
        board.engine_time_limit = durations[board.co]
        board.menu_stack.append(USE_CLOCK_MENU)

class USE_CLOCK_MENU:
    optionl1 = None
    options = [["Use clock?", ""]]
    
    def yes(board):
        board.use_clock = True
        board.menu_stack.append(CLOCK_TIME_MENU)
        
    def no(board):
        board.use_clock = False
        board.start_game()
        
class CLOCK_TIME_MENU:
    optionl1 = "Clock time:"
    options = ["30 seconds", "1 minute", "2 minutes", "5 minutes", "10 minutes", "20 minutes", "30 minutes", "40 minutes", "50 minutes", "60 minutes"]
    
    def yes(board):
        durations = {0: 0.5, 1: 1, 2: 2, 3: 5, 4: 10, 5: 20, 6: 30, 7: 40, 8: 50, 9: 60}
        
        board.clock_time = durations[board.co]
        board.menu_stack.append(CLOCK_TIME_INCREMENT_MENU)
        
class CLOCK_TIME_INCREMENT_MENU:
    optionl1 = "Clock increment:"
    options = [str(x) + " second(s)" for x in range(0, 21, 2)]
    
    def yes(board):
        durations = range(0, 21, 2)
        board.clock_time_increment = durations[board.co]
        board.start_game()
    
    

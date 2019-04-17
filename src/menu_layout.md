

The layout and flow of the menu system. If you make a change to the way the menu system works, please reflect those changes here.

### Main menu

Create game -> Player vs board -> flip board? -> choose color -> engine time limit -> Use clock? -> set up board -> start game

Create game -> player vs player -> flip board?

Create game -> board vs board -> flip board?

Load game -> Select game to load -> set up board -> continue game

Shutdown -> Are you sure?

### Pause Menu

continue game?

save game?

cancel game -> are you sure? -> back to main menu

### Menu behaviour & rules

+ (b) back button goes to previous menu in menu_stack
+ (y) yes button selects option
+ (n) no button selects false for binary-option menu; increments to next option in menu for non-binary menus
+ All binary menus should have `(y/n)` in the prompt to let the user know it is a yes/no question.

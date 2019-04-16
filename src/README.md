## /src directory

This directory contains all the code for the chessboard.

### `board.py`

The main file, contains the code for the chessboard. This file imports the code from all the other files.

### `menus.py`

This file contains the menu functionality. The menu layout plan is listed in `menu_layout.md`

### parts

The `parts` package contains the classes to control each hardware part of the board. If you would like to add a new part, create a control class for the part and add it the the parts directory. More info about creating an alternative part is listed within the part files.

### `config.py`

Contains the configuration for the chessboard.

**Note:** Hardware configuration for each part, such as GPIO pin numbers, is listed within that parts respective file in the `parts` directory.
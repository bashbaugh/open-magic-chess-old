# Magic Chess

An high-tech electronic chessboard.

### Hardware Requirements

Coming soon.

### Software Requirements

+ Python 3.5 - comes preinstalled on Raspbian.
+ python requirements(python-chess, smbus2, RPi.GPIO) - install with `pip3 install -r requirements.txt`
+ stockfish 8 or higher - install with `apt install stockfish`

If you are planning to do python development on this project, you will also need a virtual environment: 

    pip3 install virtualenv
    virtualenv -p python3 venv
    source venv/bin/activate

`source venv/bin/activate` will need to be ru-run every time you restart your pi.

If you are just planning to build the chessboard then you do not need a virtualenv.



# Magic Chess

An high-tech electronic chessboard.

#### Hardware Requirements

Coming soon.

#### Software Requirements

+ Python 3.5 - comes preinstalled on Raspbian.
+ Python requirements (python-chess, smbus2, RPi.GPIO) - install with `pip3 install -r requirements.txt`
+ stockfish 8 or higher - install with `apt install stockfish`

If you are planning to do python development on this project, you will also need a virtual environment: 

    pip3 install virtualenv
    virtualenv -p python3 venv
    source venv/bin/activate

`source venv/bin/activate` will need to be ru-run every time you restart your pi.

If you are just planning to build the chessboard then you do not need a virtualenv.

#### Setup instructions

### Enable I2C

To enable I2C on the raspberry pi, type `sudo raspi-config` and then go to “Interfacing Options” > “I2C” and enable it. 

You might also need to do the following: type `sudo nano /etc/modules` and then add the following to the bottom of the file:

    i2c-bcm2708
    i2c-dev
    
Then press `Ctr+x` then `y` then type `sudo reboot` to reboot the pi.
    
    
#### COntributing

Feel free to contribute in any way you want. Keep in mind that it is best to open an issue before opening a pull request, so that we can discuss your idea/fix/etc.



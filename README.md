# Magic Chess

An high-tech electronic chessboard.

## Hardware Requirements

Coming soon.

## Software Setup instructions

Install raspbian lite on a raspberry pi and set it up so that you can ssh into it:

Download Raspbian Lite from here:

https://www.raspberrypi.org/downloads/raspbian/

Install the image. Here is a tutorial:

https://www.raspberrypi.org/documentation/installation/installing-images/README.md

And then setup and connect SSH. Here is a tutorial:

https://core-electronics.com.au/tutorials/raspberry-pi-zerow-headless-wifi-setup.html


### Python dependencies

SSH into your pi and type `git clone https://github.com/scitronboy/open-magic-chess.git` to download the code.

Then type `cd open-magic-chess` to change into the directory. Now you will need the following:

+ Python 3.5 - comes preinstalled on Raspbian. Typing `python3 --version` should return something containing `3.5`. 
+ Python requirements (python-chess, smbus2, RPi.GPIO) - install with `pip3 install -r requirements.txt`
+ Stockfish 8 or higher - install with `sudo apt install stockfish`

If you are planning to do python development on this project, you will also need a virtual environment: 

    pip3 install virtualenv
    virtualenv -p python3 venv
    source venv/bin/activate

`source venv/bin/activate` will need to be re-run every time you restart your pi.

If you are just planning to build the chessboard then you do not need a virtualenv.

### Enable I2C

You will need to enable I2C on the raspberry pi: type `sudo raspi-config` and then go to “Interfacing Options” > “I2C” and enable it. 

You might also need to do the following: type `sudo nano /etc/modules` and then add the following to the bottom of the file:

    i2c-bcm2708
    i2c-dev
    
Then press `Ctr+x` then `y` then type `sudo reboot` to reboot the pi.
    
    
## Contributing

Feel free to contribute to this project in any way you want. Keep in mind that it is best to open an issue before opening a pull request, so that we can discuss your idea/bug-fix/etc.



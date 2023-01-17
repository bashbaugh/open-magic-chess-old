# Magic Chess Board

**THIS REPOSITORY IS ARCHIVED, PLEASE GO TO https://github.com/bashbaugh/magic-chess**

> **COMING SOON! An open-source high-tech electronic chessboard. _Not finished yet!_ Once this project is finished I will share links to a tutorial.**

### Features

+ Chess AI
+ Stepper motor controlled electromagnet under the board to move pieces
+ Web app
+ LCD control panel
+ Indicator LEDs
+ Player vs player mode, player vs board mode, board vs board mode
+ Game analysis
+ Game save system
+ + More!

## Hardware and Electronics Setup

Read [the Instructable]() tutorial for instructions on how to build the chessboard.

## Software Setup instructions

Install raspbian lite on a raspberry pi zero W and set it up so that you can ssh into it:

[Download Raspbian Lite from here](https://www.raspberrypi.org/downloads/raspbian/).

[Install the image](https://www.raspberrypi.org/documentation/installation/installing-images/README.md).

And then setup and connect headless SSH so that you can access your pi without connecting it to a monitor or keyboard. [Here is a tutorial](https://core-electronics.com.au/tutorials/raspberry-pi-zerow-headless-wifi-setup.html). **If using windows, make sure you click the view tab at the top in file explorer and select "file name extensions."**

Finally, you will need expand your filesystem so that you can take advantage of the full capacity of your SD card. SSH into your pi then type `sudo raspi-config` and then navigate to “Advanced Options” > “Expand Filesystem”. Then press "Finish" and say yes when it asks you to "reboot now".

### Python dependencies

SSH into your pi again and type this to install Git and pip: `sudo apt update && sudo apt install git python3-pip -y` . It will take a minute or two.

Then type `git clone https://github.com/scitronboy/open-magic-chess.git` to download the code.

Then type `cd open-magic-chess` to change into the directory. Now you will need the following:

+ Python 3.7 - comes preinstalled on Raspbian. Typing `python3 --version` should return something containing `3.7`.
+ Python requirements (python-chess, smbus2, gpiozero, etc.) - install with `sudo pip3 install -r requirements.txt`
+ Stockfish 8 or higher - install with `sudo apt install stockfish -y`

<!-- If you are planning to do python development on this project, you will also need a virtual environment:

    pip3 install virtualenv
    virtualenv -p python3 venv
    source venv/bin/activate

`source venv/bin/activate` will need to be re-run every time you restart your pi.

If you are just planning to build the chessboard then you do not need a virtualenv.-->

### Enable I2C

You will need to enable I2C on the raspberry pi: type `sudo raspi-config` and then go to “Interfacing Options” > “I2C” and enable it.

You might also need to type `sudo nano /etc/modules` and then add the following to the bottom of the file:

    i2c-bcm2708
    i2c-dev
    
Then press `Ctr+x` then `y` then enter/return then `sudo reboot` to reboot the pi.

## License

This project is licensed under the [MIT License](https://github.com/scitronboy/open-magic-chess/blob/master/LICENSE).

You are free to modify and distribute copies of this software (read license for more details). If you do so, please give credit to it's creators, Benjamin A. and contributors. Also please link to this GitHub repository!
    
## Contributing

Feel free to contribute to this project in any way you want. Keep in mind that it is best to open an issue before opening a pull request, so that we can discuss your idea/bug-fix/etc. Also look through closed issues before you open your own, so that you don't post something that's already been solved.

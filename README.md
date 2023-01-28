# piti

**piti** is a (very wip) python command-line program for connecting a raspberry pi to a ti-83+'s series calculator using the calculator's link port (2.5mm stereo jack) and the raspberry's GPIO pins.

## Commands

The followings commands are currently supported (in various states of functionality):

* `--versions` - Request info about the calculator's OS and Model version
* `--screenshot` - Take a screenshot of the current calculator screen
* `--list` - Lists all files in calculator memory
* `--request FILE` - Request a specific file from calculator memory
* `--receive` - Receive file(s) selected by the calculator
* `--gpio 6,5` - Set the gpio pins to use (optional)

## Pinout

The following is the default pinout useed by piti, the raspberry pi pins can currently be tweaked through the `--gpio` argument. A custom adaptor will have to be constructed for this purpose.

Function | TI-83+ (2.5mm stereo jack) | Raspberry (BCM)|
---------|--------|-----------|
 Ground  | Sleeve |   GND     |
  1 bit  | Ring (Right)  |   GPIO 5  |
  0 bit  | Tip (Left)   |   GPIO 6  |

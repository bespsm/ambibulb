# AMBIBULB

The word *ambibulb* is the conjuction between the words Ambilight® (Philips TV's feature that projects color onto the wall behind a TV) and a bulb. *ambibulb*  attempts to provide the similar experince with a single-board computer (like Rapsberry PI) and IR remote controled LED light bulb. **Please watch the demo.**

*ambibulb* can play a video and simultaneously transmit IR signal to the light bulb with its most dominant color. This can enhance your viewing experience or make your party more colorful 🌈.


### HARDWARE
* Raspberry PI (tested on 3B+)
* HDMI output (TV, projector, display)
* RGB LED light bulb with IR remote control (supported 17 colors light bulb with 5 levels of brightness)
* IR transmitter (tested on KY-005)
* IR receiver(tested on KY-022, optional)
* wiring

### SOFTWARE DEPENDENCIES
* Raspberry Pi OS (10 buster, headless work as well)
* lirc
* omxplayer
* [info-beamer screenshot util](https://github.com/info-beamer/tools/tree/master/screenshot)
* python3 and the modules (requirements.txt)

### SETUP
1. Install Raspberry PI OS on your [SD card](https://www.raspberrypi.org/documentation/installation/installing-images/)
2. 
...

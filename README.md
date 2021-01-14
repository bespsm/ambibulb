# AMBIBULB

 Ambibulb attempts to provide the similar experience to Ambilight® (Philips TV's feature that projects color onto the wall behind a TV) using Raspberry PI and a simple IR remote controlled LED light bulb. [**Please watch the demo.**](https://youtu.be/R3JeVooaytU)

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
* python3, pip and the modules in *requirements.txt* (recommened to use venv)

### SETUP
1. Install Raspberry PI OS on your [SD card](https://www.raspberrypi.org/documentation/installation/installing-images/)
2. Build and install all software dependecies
3. Connect and set up your IR transmitter to [RPI](https://gist.github.com/prasanthj/c15a5298eb682bde34961c322c95378b)
    - if you can not find [config file](http://lirc-remotes.sourceforge.net/remotes-table.html) for you IR control device, record it with [IR transmitter](https://gist.github.com/prasanthj/c15a5298eb682bde34961c322c95378b). My lirc config is stored [here](conf/osram-led-bulb.conf)
4. Copy to RPI and run the [script](src/ambibulb.py)

### RUN OPTIONS
simple run:
```
 $ python3 ./ambibulb.py demo.mp4
 ```
all options:
```
usage: ambibulb.py [-h] [-w] [-c CYCLE_PERIOD] [-v] media_path

positional arguments:
  media_path            path to media file

optional arguments:
  -h, --help            show this help message and exit
  -w, --with_white      use white light in the algoritm
  -c CYCLE_PERIOD, --cycle_period CYCLE_PERIOD
                        min period color changing, sec. (Default = 0.5 sec)
  -v, --verbosity       show timing steps
```

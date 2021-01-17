# AMBIBULB

 Ambibulb attempts to provide the similar experience to Ambilight® (Philips TV's feature that projects color onto the wall behind a TV) using Raspberry PI and a simple IR remote controlled LED light bulb. [**Please watch the demo.**](https://youtu.be/R3JeVooaytU)

*ambibulb* can play a video and simultaneously transmit IR signal to the light bulb with its most dominant color. This can enhance your viewing experience or make your party more colorful 🌈.

### HARDWARE
* Raspberry PI (tested on 3B+)
* HDMI output (TV, projector, display)
* RGB LED light bulb with IR remote control (supports 16 colors and 5 levels of brightness)
* IR transmitter (tested on KY-005)
* IR receiver(tested on KY-022, optional)
* wiring

### SOFTWARE DEPENDENCIES
* Raspberry Pi OS (10 buster, headless work as well)
* lirc
* omxplayer
* [info-beamer screenshot util](https://github.com/info-beamer/tools/tree/master/screenshot)
* pip packeges in *requirements.txt* (installed automatically)

### SETUP
1. Install Raspberry PI OS on your [SD card](https://www.raspberrypi.org/documentation/installation/installing-images/)
2. Build and install all software dependecies
3. Connect and set up your IR transmitter to [RPI](https://gist.github.com/prasanthj/c15a5298eb682bde34961c322c95378b)
    - if you couldn't find [config file](http://lirc-remotes.sourceforge.net/remotes-table.html) for you IR control device, record it with [IR transmitter](https://gist.github.com/prasanthj/c15a5298eb682bde34961c322c95378b). My lirc config is stored [here](conf/osram-led-bulb.conf)
4. **pip3 install ambibulb** (recommended to install in venv)

### RUN OPTIONS
simple run:
```
 $ ambibulb demo.mp4
 ```
all options:
```
usage: ambibulb [-h] [-w] [-c CYCLE_PERIOD] [-v] [-l LIRC_CONF] media_path

positional arguments:
  media_path            path to media file

optional arguments:
  -h, --help            show this help message and exit
  -w, --with_white      use white light in the algoritm
  -c CYCLE_PERIOD, --cycle_period CYCLE_PERIOD
                        min period color changing, sec. (Default = 0.4 sec)
  -v, --verbosity       show timing steps
  -l LIRC_CONF, --lirc_conf LIRC_CONF
                        lirc config name (Default = 'RGBLED')
```
All *omxplayer* keyboard shortcuts are avaliable during ambibulb execution.

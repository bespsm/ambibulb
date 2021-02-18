# AMBIBULB

 Ambibulb attempts to provide the similar experience to Ambilight® (Philips TV's feature that projects color onto the wall behind a TV) using Raspberry PI and a simple IR remote controlled LED light bulb. [**Please watch the demo.**](https://youtu.be/R3JeVooaytU)

*ambibulb* controls the color of RC lights based based on the dominant color of displayed image. This can enhance your viewing experience or make your party more colorful 🌈.

### HARDWARE
* Raspberry PI (tested on 3B+)
* HDMI output (TV, projector, display)
* RGBW LED light bulb with IR remote control (currently supported model: OSRAM LED STAR+)
* IR transmitter (tested on KY-005)
* IR receiver(tested on KY-022, optional)
* wiring

### SOFTWARE DEPENDENCIES
* Raspberry Pi OS (10 buster, or any other RPI compatibe OS)
* LIRC (Linux Infrared Remote Control)

### SETUP AND INSTALLATION
1. Install Raspberry PI OS on your [SD card](https://www.raspberrypi.org/documentation/installation/installing-images/)
2. Install lirc on your RPI:
```
$ apt install lirc
```
3. Configure lirc, connect and configure IR transmitter, [guideline]( https://gist.github.com/prasanthj/c15a5298eb682bde34961c322c95378b)
4. Install ambibulb. There are 2 ways, either build, install and configure locally:
```
 $ wget https://github.com/bespsm/ambibulb/archive/main.zip
 $ unzip main.zip
 $ cd ambibulb-main
 $ make install
 $ make configure
```
or using pip (recommended in venv) and configure locally:
```
 $ python3 -m pip install --user ambibulb
 $ wget https://github.com/bespsm/ambibulb/archive/main.zip
 $ unzip main.zip
 $ cd ambibulb-main
 $ make configure
 ```

### COMMANDS
Start ambibulb service:
 ```
 $ systemctl --user start ambibulb.service
 ```
Stop ambibulb service:
 ```
 $ systemctl --user stop ambibulb.service
 ```
Check ambibulb service current status, two options:
 ```
 $ systemctl --user status ambibulb.service
 $ journalctl -f
 ```
Configure/change the settings of ambibulb service:
 ```
 $ ambibulb-config
 ```

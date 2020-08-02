# Visualiser

### Prerequisites
 * Python - Ver. 3.7.1 (https://www.python.org/ftp/python/3.7.1/) 
 * flask - Ver. 1.1.2 (https://palletsprojects.com/p/flask/)
 * flask-bootstrap - Ver. 3.3.7.1 (https://github.com/mbr/flask-bootstrap)
 * Watchdog - Ver. 0.10.3 (https://github.com/gorakhargosh/watchdog)
 * Pillow - Ver. 2.2.2 (https://python-imaging.github.io/)
 * Numpy - Ver. 1.19.1 (https://github.com/numpy/numpy)
 * PyAudio - Ver. 0.2.11 (http://people.csail.mit.edu/hubert/pyaudio/)

### Installation

Installation is not necessary, but the following script can act as a set-up script for using the Visualiser webapp on a RaspberryPi:
<pre><code>
#!/bin/bash

#If 'COPF' exists copy logs from Visualiser log path to '/boot/Visualiser_Logs/'
COPF=/boot/COPY-YES
if [ -f "$COPF" ]; then
     sudo rm -r /boot/Visualiser_Logs/*
     sudo cp -Rfa /home/pi/Visualiser/log/. /boot/Visualiser_Logs/
fi

#If 'ZIP' exists containing Visualiser code zip, will move/ unzip it to 'DIRECTORY', overwriting anything there and setting the appropriate permissions
ZIP=/boot/Visualiser.zip
DIRECTORY=/home/pi/Visualiser
if [ -f "$ZIP" ]; then
    if [ -d "$DIRECTORY" ]; then
         sudo rm -rf /home/pi/Visualiser
    fi
    sudo unzip /boot/Visualiser.zip -d /home/pi/
    sudo chmod 777 -R /home/pi/Visualiser
    sudo rm -f /boot/Visualiser.zip
fi

#If 'VCONF_S' exists will allow you to provide a config file for the Visualiser without using the webapp (Assuming 'VCONF_D' is a vaild location)
VCONF_S=/boot/config.txt
VCONF_D=/home/pi/Visualiser/config
if [ -f "$VCONF_S" ]; then
    if [ -d "$VCONF_D" ]; then
	 sudo mv -f /boot/config.txt /home/pi/Visualiser/config/
    fi
fi

exit 0
</code></pre>

### Notes

* If updating RaspberryPi from 2.7 to 3.7.1, the following may be necessary:
	* Remove Python 2.x:
	<pre><code>  
	cd /etc
	sudo apt-get remove python2.7
	sudo apt-get autoremove
	</code></pre>
    
	* Install libffi-dev:
	<pre><code>
	sudo apt-get install libffi-dev
	</code></pre>
    
	* Install pip: 
	<pre><code>
	sudo apt-get install python-pip
	</code></pre>

	* Update RaspberryPi '~/.bashrc' with: 
	<pre><code>
	alias python='/usr/local/bin/python3'
	</code></pre>
    
* Automatic script start from boot on a RaspberryPi can be achieved by appending the following to the '/etc/rc.local' file:
	<pre><code>
	sh /home/pi/start-visualiser-server.sh
	cd /home/pi/Visualiser/webapp
	python app.py "$_IP" &

	cd /home/pi/Visualiser/display/control
	python app.py &
	</code></pre>


## Webapp

### Specific Prerequisites
 * Python - Ver. 3.7.1 (https://www.python.org/ftp/python/3.7.1/) 
 * Flask - Ver. 1.1.2 (https://palletsprojects.com/p/flask/)
 * Flask-bootstrap - Ver. 3.3.7.1 (https://github.com/mbr/flask-bootstrap)

### Notes

* Includes and modifies 'Flask-Colorpicker' - Ver. 0.9 (https://github.com/mrf345/flask_colorpicker/) to allow custom assignment of picker's 'cancel' and 'choose' buttons.

* Config file format is as follow:
	<pre><code>{"colour": "rgb([0-255], [0-255], [0-255])", "pattern_type": "[1/2/3]", "ip": "[IP ADDRESS]", "lang": "[en/it]"}</code></pre>

## Display

### Specific Prerequisites
 * Python - Ver. 3.7.1 (https://www.python.org/ftp/python/3.7.1/) 
 * Watchdog - Ver. 0.10.3 (https://github.com/gorakhargosh/watchdog)
 * Pillow - Ver. 2.2.2 (https://python-imaging.github.io/)
 * Numpy - Ver. 1.19.1 (https://github.com/numpy/numpy)
 * PyAudio - Ver. 0.2.11 (http://people.csail.mit.edu/hubert/pyaudio/)
 
### Notes

* Installation of PyAudio can be tricky, I found this to be helpful: https://www.raspberrypi.org/forums/viewtopic.php?t=25173

* Installation process and C++ libraries for controlling RGB Matrix HAT found at: https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices

* Processing of audio **HEAVLY** based on the work by *Thomas Kou and Hansson Lin* (https://github.com/thomaskou/RGB-Matrix-Audio-Visualizer)

* RGB display code **HEAVLY** based on the work by *hzeller* (https://github.com/hzeller/rpi-rgb-led-matrix)
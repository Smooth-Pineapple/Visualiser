# Visualiser

## Webapp

### Prerequisites
 * flask - Ver. 1.1.2 (https://palletsprojects.com/p/flask/)
 * flask-bootstrap - Ver. 3.3.7.1 (https://github.com/mbr/flask-bootstrap)

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

#Run Visualiser code
#cd /home/pi/Visualiser/webapp
#sudo python app.py &

exit 0
</code></pre>

### Notes

* Includes and modifies 'Flask-Colorpicker' - Ver. 0.9 (https://github.com/mrf345/flask_colorpicker/) to allow custom assignment of picker's 'cancel' and 'choose' buttons.

* Config file format is as follow:

<pre><code>
{"colour": "rgb([0-255], [0-255], [0-255])", "pattern_type": "[1/2/3]", "ip": "[IP ADDRESS]", "lang": "[en/it]"}
</code></pre>

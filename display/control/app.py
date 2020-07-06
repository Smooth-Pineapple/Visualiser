import sys
sys.path.append('../..')

import os
import re
import threading

from serv_logging.serv_logging import Logging
from file_management.file_management import FileManagement
from file_management.data_extraction import DataExtraction
from file_management.watch_config import WatchdogConfig
from display.control.bottom_up import BottomUp

my_path = os.path.dirname(os.path.abspath(__file__))
log_path = str(my_path) + '/../../log/visualiser_display.log'
config_dir = str(my_path) + '/../../config/'
config_path = config_dir + 'config.txt'

class Control():
    def __init__(self):
        self.display_pattern = None
        self.colour_key = 'colour'
        self.pattern_key = 'pattern_type'
        self.brightness_key = 'brightness'

    def get_config(self, parse_ip):
        config_data, config_error = DataExtraction.verify_config_data(FileManagement.read_json(config_path, log_path), self.colour_key, self.pattern_key, self.brightness_key, log_path)

        ip = None

        if parse_ip:
            if 'ip' not in config_data or config_data['ip'] is None:
                logger.write(Logging.ERR, "IP address not found in config, please refer to guide to manually set config data and retrieve logs")
                ip = "No IP"
            else:
                ip = config_data['ip']

                try:
                    ip_regex = '^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'   
                    if re.match(ip_regex, ip):
                        logger.write(Logging.INF, "Valid IP address in config: " + ip) 
                    else:
                        logger.write(Logging.ERR, "Config IP address does not match expected regex, please refer to guide to manually set config data and retrieve logs")
                        ip = "No IP"
                except Exception as e: 
                    logger.write(Logging.ERR, "Config IP address regex error, please refer to guide to manually set config data and retrieve logs: " + str(e))
                    ip = "No IP"

        colour = config_data[self.colour_key]
        pattern = config_data[self.pattern_key]
        brightness = config_data[self.brightness_key]

        logger.write(Logging.INF, "Extracted config data- Colour: " + colour + ", Pattern: " + pattern + ", Brightness: " + brightness) 

        return ip, colour, pattern, brightness

    def load_display(self, parse_ip):
        ip, colour, pattern, brightness = self.get_config(parse_ip)
        print("Calls")
        #if ip is not None:
        #   show symbol
        print(ip, colour, pattern, brightness)
        if self.display_pattern is not None:
            print("stap")
            self.display_pattern.stop()
            self.display_pattern = None

        if pattern == '1':
            print("restart")
            self.display_pattern = BottomUp(colour=colour, brightness=brightness)

        
        if self.display_pattern is not None:
            print("process")
            self.display_pattern.process()


if __name__ == '__main__':
    logger = Logging.getInstance(Logging.DEB)
    logger.open(log_path)

    control = Control()

    monitor_config = WatchdogConfig(control.load_display, config_dir, '*.txt', '', True, False, False, log_path)
    
    try:
        monitor_thread = threading.Thread(target=monitor_config.start_observing())
        monitor_thread.start()
    except Exception as e:
        logger.write(Logging.ERR, "Monitoring thread stopped: " + str(e)) 

    control.load_display(True)    

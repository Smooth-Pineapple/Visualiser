import sys
sys.path.append("..")

import os
import re
import threading

from serv_logging.serv_logging import Logging
from file_management.file_management import FileManagement
from file_management.data_extraction import DataExtraction
from file_management.watch_config import WatchdogConfig
from samples.bottom_up import BottomUp

my_path = os.path.dirname(os.path.abspath(__file__))
log_path = str(my_path) + '/../log/visualiser_display.log'
config_dir = str(my_path) + '/../config/'
config_path = config_dir + 'config.txt'

ip = None
colour = None
pattern = None

colour_key = 'colour'
pattern_key = 'pattern_type'
brightness_key = 'brightness'

def get_config(parse_ip):
    config_data, config_error = DataExtraction.verify_config_data(FileManagement.read_json(config_path, log_path), colour_key, pattern_key, brightness_key, log_path)

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

    colour = config_data[colour_key]
    pattern = config_data[pattern_key]
    brightness = config_data[brightness_key]

    logger.write(Logging.INF, "Extracted config data- Colour: " + colour + ", Pattern: " + pattern + ", Brightness: " + brightness) 

    return ip, colour, pattern, brightness

def load_display(parse_ip):
    ip, colour, pattern, brightness = get_config(parse_ip)
    
    #if pattern
    display_pattern = BottomUp()
    display_pattern.run()


if __name__ == '__main__':
    logger = Logging.getInstance(Logging.DEB)
    logger.open(log_path)

    load_display(True)    

    monitor_config = WatchdogConfig(load_display, config_dir, '*.txt', '', True, False, False, log_path)
    
    try:
        monitor_thread = threading.Thread(target=monitor_config.start_observing())
        monitor_thread.start()
    except Exception as e:
        logger.write(Logging.ERR, "Monitoring thread stopped: " + str(e)) 
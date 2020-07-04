import sys
sys.path.append("..")

import os
import re

from serv_logging.serv_logging import Logging
from file_management.file_management import FileManagement
from file_management.data_extraction import DataExtraction

my_path = os.path.dirname(os.path.abspath(__file__))
log_path = str(my_path) + '/../log/visualiser_server.log'
config_path = str(my_path) + '/../config/config.txt'

ip = None
colour = None
pattern = None

colour_key = 'colour'
pattern_key = 'pattern_type'

if __name__ == '__main__':
    logger = Logging.getInstance(Logging.DEB)
    logger.open(log_path)

    config_data, config_error = DataExtraction.verify_config_data(FileManagement.read_json(config_path, log_path), colour_key, pattern_key, log_path)

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

    logger.write(Logging.INF, "Extracted config data- IP: " + ip + ", Colour: " + colour + ", Pattern: " + pattern) 
    print("Extracted config data- IP: " + ip + ", Colour: " + colour + ", Pattern: " + pattern)
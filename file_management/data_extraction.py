import io
import os
import os.path
import re
import json

from .file_management import FileManagement
from serv_logging.serv_logging import Logging

class DataExtraction:
    @staticmethod
    def __is_pattern_config(pattern_config, log_path):
        logger = Logging.getInstance(Logging.DEB)
        logger.open(log_path)

        try:
            pattern_config_int = int(pattern_config)
            if pattern_config_int < 1 or pattern_config_int > 3:
                raise ValueError 

            return True
        except ValueError:
            logger.write(Logging.ERR, "Invalid pattern config: " + pattern_config)
            return False   

    @staticmethod
    def __verify_config_data(config_data, colour_key, pattern_key, log_path):
        logger = Logging.getInstance(Logging.DEB)
        logger.open(log_path)
        
        config_error = False

        if colour_key not in config_data:
            config_data[colour_key] = 'rgba(18,237,159,1)'
            logger.write(Logging.WAR, "Colour config not present, setting to default") 
            config_error = True
        elif not config_data[colour_key]:
            config_data[colour_key] = 'rgba(0,0,0,0)'

        if (pattern_key not in config_data or not config_data[pattern_key]) or DataExtraction.__is_pattern_config(config_data[pattern_key], log_path) is False:
            config_data[pattern_key] = '1'
            logger.write(Logging.WAR, "Pattern key not present, setting to default") 
            config_error = True

        rgb_regex = '^rgb\\(\\s*(0|[1-9]\\d?|1\\d\\d?|2[0-4]\\d|25[0-5])%?\\s*,\\s*(0|[1-9]\\d?|1\\d\\d?|2[0-4]\\d|25[0-5])%?\\s*,\\s*(0|[1-9]\\d?|1\\d\\d?|2[0-4]\\d|25[0-5])%?\\s*\\)$'
        rgba_regex = '^rgba\\(\\s*(0|[1-9]\\d?|1\\d\\d?|2[0-4]\\d|25[0-5])%?\\s*,\\s*(0|[1-9]\\d?|1\\d\\d?|2[0-4]\\d|25[0-5])%?\\s*,\\s*(0|[1-9]\\d?|1\\d\\d?|2[0-4]\\d|25[0-5])%?\\s*,\\s*((0.[1-9])|[01])\\s*\\)$'
    
        if not re.match(rgb_regex, config_data[colour_key]):
            if not re.match(rgba_regex, config_data[colour_key]):
                config_data[colour_key] = 'rgba(18,237,159,1)'
                logger.write(Logging.WAR, "Colour config does not match RBG or RGBA, setting to default") 
                config_error = True

        return config_data, config_error

    @staticmethod
    def fix_config_data(config_data, colour_key, pattern_key, config_path, log_path):
        logger = Logging.getInstance(Logging.DEB)
        logger.open(log_path)

        config_data, config_error = DataExtraction.__verify_config_data(config_data, colour_key, pattern_key, log_path)

        if config_error is True:
            FileManagement.write_json(config_path, config_data, log_path)
            logger.write(Logging.WAR, "Error in config data requiring update") 

        return config_data
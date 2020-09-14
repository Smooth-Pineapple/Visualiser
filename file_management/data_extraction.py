import io
import os
import os.path
import re
import json

from .file_management import FileManagement
from serv_logging.serv_logging import Logging

class DataExtraction:
    @staticmethod
    def __is_config_int(config_type, key, min, max, log_path):
        logger = Logging.getInstance(Logging.DEB)
        logger.open(log_path)

        try:
            config_type_int = int(config_type)
            if config_type_int < min or config_type_int > max:
                raise ValueError 

            return True
        except ValueError as e:
            logger.write(Logging.ERR, "Exception with config key: " + key + " " + str(e))
            return False   

    @staticmethod
    def verify_config_data(config_data, colour_key, pattern_key, brightness_key, log_path):
        logger = Logging.getInstance(Logging.DEB)
        logger.open(log_path)
        
        config_error = False

        if colour_key not in config_data:
            config_data[colour_key] = 'rgba(18,237,159,1)'
            logger.write(Logging.WAR, "Colour config not present, setting to default") 
            config_error = True
        elif not config_data[colour_key]:
            config_data[colour_key] = 'rgba(0,0,0,0)'

        if (pattern_key not in config_data or not config_data[pattern_key]) or DataExtraction.__is_config_int(config_data[pattern_key], pattern_key, 1, 4, log_path) is False:
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

        if brightness_key not in config_data or DataExtraction.__is_config_int(config_data[brightness_key], brightness_key, 0, 100, log_path) is False:
            config_data[brightness_key] = '50'
            logger.write(Logging.WAR, "Invalid Brightness config, setting to default") 
            config_error = True

        return config_data, config_error

    @staticmethod
    def fix_config_data(config_data, colour_key, pattern_key, brightness_key, config_path, log_path):
        logger = Logging.getInstance(Logging.DEB)
        logger.open(log_path)

        config_data, config_error = DataExtraction.verify_config_data(config_data, colour_key, pattern_key, brightness_key, log_path)

        if config_error is True:
            FileManagement.write_json(config_path, config_data, log_path)
            logger.write(Logging.WAR, "Error in config data so updated file") 

        return config_data
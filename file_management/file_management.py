import io
import os
import os.path
import json

from serv_logging.serv_logging import Logging

class FileManagement:
    @staticmethod 
    def write_json(config_path, data_map, log_path):
        logger = Logging.getInstance(Logging.DEB)
        logger.open(log_path)
        logger.write(Logging.DEB, "Writing config data: " +  json.dumps(data_map) + ", to file: " + config_path) 
        try:
            with open(config_path, 'w') as file:
                file.write(json.dumps(data_map))
        except Exception as e:
            logger.write(Logging.ERR, "Cannot open file to write data: " + str(e))      

    @staticmethod 
    def update_json(config_path, data_map, log_path):
        logger = Logging.getInstance(Logging.DEB)
        logger.open(log_path)
        logger.write(Logging.DEB, "Attempting to update config file: " + config_path)  

        exist_config = FileManagement.read_json(config_path, log_path)
        if exist_config is not None:
            exist_config.update(data_map)
            FileManagement.write_json(config_path, exist_config, log_path)
        else:
            logger.write(Logging.ERR, "Unable to update file")   

    @staticmethod 
    def read_json(config_path, log_path):
        logger = Logging.getInstance(Logging.DEB)
        logger.open(log_path)
        logger.write(Logging.DEB, "Reading config data from file: " + config_path) 

        data_map = {}

        try:
            with io.open(config_path, encoding='utf-8') as file:
                data_map = json.load(file)

            logger.write(Logging.DEB, "Read config data from file: " + json.dumps(data_map)) 
        except Exception as e:
            logger.write(Logging.ERR, "Cannot open file to read data: " + str(e))    

        return data_map

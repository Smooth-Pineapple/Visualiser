import sys
sys.path.append('../..')

import os
import re
import threading

from serv_logging.serv_logging import Logging
from file_management.file_management import FileManagement
from file_management.data_extraction import DataExtraction
from file_management.watch_config import WatchdogConfig
from display.control.samplebase import SampleBase
from display.control.bottom_up import BottomUp
from display.control.block import Block
from display.control.network_notification import NetworkNotification

from display.audio.input_stream import InputStream
from display.audio.audio_spectrum import AudioSpectrum
from display.audio.spectrum_analysis import SpectrumAnalysis
from display.control.spectrum_conversion import SpectrumConversion


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

        self.input_stream = InputStream()
        self.audio_spectrum = AudioSpectrum()
        self.spectrum_analysis = SpectrumAnalysis()
        self.display_spectrum = SpectrumConversion()

    def load_audio_dev(self):
        logger.write(Logging.DEB, "Opening stream") 
        self.input_stream.init_input_stream(2048, 44100)
        self.spectrum_analysis.set_frequencies(0, 44100)

    def close_audio_dev(self):
        logger.write(Logging.DEB, "Closing stream") 
        self.input_stream.stop_input_stream()

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

    def stop(self):
        SampleBase.stop()
        
    def ip_check_display(self):
        ip, _, _, brightness = self.get_config(True)
	
        have_ip = True
        if ip == "No IP":
	        have_ip = False
        
        NetworkNotification(have_ip=have_ip, brightness=brightness).process()

    def load_display(self, parse_ip):
        logger.write(Logging.DEB, "Loading display") 
        _, colour, pattern, brightness = self.get_config(parse_ip)

        if pattern == '1':
            self.display_pattern = BottomUp(colour=colour, brightness=brightness, input_stream=self.input_stream, audio_spectrum=self.audio_spectrum, spectrum_analysis=self.spectrum_analysis, display_spectrum=self.display_spectrum, log_path=log_path)
        elif pattern == '2':
            self.display_pattern = Block(colour=colour, brightness=brightness, input_stream=self.input_stream, audio_spectrum=self.audio_spectrum, spectrum_analysis=self.spectrum_analysis, display_spectrum=self.display_spectrum, log_path=log_path)

        
        if self.display_pattern is not None:
            self.display_pattern.process()
            


if __name__ == '__main__':
    logger = Logging.getInstance(Logging.DEB)
    logger.open(log_path)

    control = Control()

    monitor_config = WatchdogConfig(control.stop, config_dir, '*.txt', '', True, False, False, log_path)
    monitor_thread = threading.Thread(target=monitor_config.start_observing)
    monitor_thread.start()
    
    control.load_audio_dev()
    try:
        control.ip_check_display()
        while True:
            control.load_display(False)
    except KeyboardInterrupt:
        WatchdogConfig.STOP_LOOP = True
        monitor_thread.join()
        sys.exit(0)
    finally:
        control.close_audio_dev()
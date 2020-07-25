import math
import time
import random
import re
import sys
from datetime import datetime

from display.control.samplebase import SampleBase
from serv_logging.serv_logging import Logging

class BottomUp(SampleBase):
    STOP_LOOP = False

    def __init__(self,  colour, brightness, input_stream, audio_spectrum, spectrum_analysis, display_spectrum, log_path, *args, **kwargs):
        super(BottomUp, self).__init__(*args, **kwargs)
        self.__logger = Logging.getInstance(Logging.DEB)
        self.__logger.open(log_path)
        
        self.__logger.write(Logging.DEB, "Starting Bottom Up display")

        BottomUp.STOP_LOOP = False
        
        rgb = []
        for s in re.findall(r'\b\d+\b', colour):
            rgb.append(int(s))

        self.input_stream = input_stream
        self.audio_spectrum = audio_spectrum
        self.spectrum_analysis = spectrum_analysis
        self.display_spectrum = display_spectrum
        
        self.colour = rgb

        self.brightness = int(brightness)
        self.stop_me = False

    def drawBarRow(self, offset_canvas, bar, y, r, g, b, bar_width, height):
        for x in range(bar * bar_width, (bar + 1) * bar_width):
            offset_canvas.SetPixel(x, height - 1 - y, r, g, b)

    def run(self):
        num_bars = 16

        width = self.matrix.width
        height = self.matrix.height

        self.matrix.brightness = self.brightness
  
        bar_width = width / num_bars

        offset_canvas = self.matrix.CreateFrameCanvas()

        try:
            t = 0
            while not BottomUp.STOP_LOOP:
                self.input_stream.tick_input_stream()
                self.audio_spectrum.set_audio_data(self.input_stream.get_input_data())
                self.audio_spectrum.data_to_spectrum()

                self.spectrum_analysis.set_spectrum(self.audio_spectrum.get_spectrum())

                bar_heights = self.display_spectrum.tick(self.spectrum_analysis.get_amplitude_array(num_bars), num_bars)

                for x in range(0, num_bars):
                    y = 0
                    for i in range(0, int(bar_heights[x])):
                        y = i
                        
                        if self.colour == [0, 0, 0, 0]:
                            self.drawBarRow(offset_canvas, x, y, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), bar_width, height)
                        else:
                            self.drawBarRow(offset_canvas, x, y, self.colour[0], self.colour[1], self.colour[2], bar_width, height)

                    for k in range(y, height):
                        y = k
                        self.drawBarRow(offset_canvas, x, y, 0, 0, 0, bar_width, height)

                time.sleep(0.1)
                offset_canvas = self.matrix.SwapOnVSync(offset_canvas)
        except KeyboardInterrupt:
            BottomUp.stop()
            raise KeyboardInterrupt()
        except ValueError as e:
            logger.write(Logging.ERR, "Exception with displaying Bottom Up style: " + str(e))
            BottomUp.stop()
            raise KeyboardInterrupt()

    @staticmethod 
    def stop():
        BottomUp.STOP_LOOP = True
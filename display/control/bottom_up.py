import math
import time
import random
import sys
from datetime import datetime

from display.control.samplebase import SampleBase
from serv_logging.serv_logging import Logging

class BottomUp(SampleBase):
    def __init__(self,  colour, brightness, input_stream, audio_spectrum, spectrum_analysis, display_spectrum, log_path, *args, **kwargs):
        super(BottomUp, self).__init__(colour, brightness, input_stream, audio_spectrum, spectrum_analysis, display_spectrum, *args, **kwargs)
        self.__logger = Logging.getInstance(Logging.DEB)
        self.__logger.open(log_path)
        
        self.__logger.write(Logging.DEB, "Starting Bottom Up display")

    def drawBarRow(self, offset_canvas, bar, y, r, g, b, bar_width, height):
        for x in range(bar * bar_width, (bar + 1) * bar_width):
            self.offset_canvas.SetPixel(x, height - 1 - y, r, g, b)

    def run(self):
        super(BottomUp, self).run() 
        
        num_bars = 16
  
        bar_width = self.width / num_bars

        try:
            t = 0
            while not SampleBase.STOP_LOOP:
                bar_heights = self.get_bar_heights(num_bars)

                for x in range(0, num_bars):
                    y = 0
                    for i in range(0, int(bar_heights[x])):
                        y = i
                        
                        if self.colour == [0, 0, 0, 0]:
                            self.drawBarRow(self.offset_canvas, x, y, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), bar_width, self.height)
                        else:
                            self.drawBarRow(self.offset_canvas, x, y, self.colour[0], self.colour[1], self.colour[2], bar_width, self.height)

                    for k in range(y, self.height):
                        y = k
                        self.drawBarRow(self.offset_canvas, x, y, 0, 0, 0, bar_width, self.height)

                time.sleep(0.1)
                self.offset_canvas = self.matrix.SwapOnVSync(self.offset_canvas)
        except KeyboardInterrupt:
            SampleBase.stop()
            raise KeyboardInterrupt()
        except ValueError as e:
            logger.write(Logging.ERR, "Exception with displaying Bottom Up style: " + str(e))
            SampleBase.stop()
            raise KeyboardInterrupt()
import math
import re
import time
import random
from display.control.samplebase import SampleBase
from serv_logging.serv_logging import Logging


class Libra(SampleBase):
    def __init__(self,  colour, brightness, input_stream, audio_spectrum, spectrum_analysis, display_spectrum, log_path, *args, **kwargs):
        super(Libra, self).__init__(colour, brightness, input_stream, audio_spectrum, spectrum_analysis, display_spectrum, *args, **kwargs)
        
        self.__logger = Logging.getInstance(Logging.DEB)
        self.__logger.open(log_path)
        
        self.direction = 1

        self.__logger.write(Logging.DEB, "Starting Libra display")

    def drawLibra(self, matrix, offset_canvas, r, g, b, width, height):
        if self.matrix.brightness < 1:
            self.direction = 1
        if self.matrix.brightness > 99:
            self.direction = -1
        
        self.matrix.brightness += self.direction

        libraCoOrd = [(20, 9), (22, 12), (31, 10), (39, 3), (46, 11), (42, 23), (28, 26), (27, 28)]
        for x, y in libraCoOrd:
            offset_canvas.SetPixel(x, y, r, g, b)

        offset_canvas = matrix.SwapOnVSync(offset_canvas)

        time.sleep(0.5)

    def run(self):
        super(Libra, self).run() 

        try:
            didLibra = False
            while not SampleBase.STOP_LOOP:
                if self.colour == [0, 0, 0, 0]:
                    self.drawLibra(self.matrix, self.offset_canvas, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), self.width, self.height)
                else:      
                    self.drawLibra(self.matrix, self.offset_canvas, self.colour[0], self.colour[1], self.colour[2], self.width, self.height)

        except KeyboardInterrupt:
            SampleBase.stop()
            raise KeyboardInterrupt()
        except ValueError as e:
            logger.write(Logging.ERR, "Exception with displaying Libra style: " + str(e))
            SampleBase.stop()
            raise KeyboardInterrupt()
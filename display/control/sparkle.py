import math
import re
import time
import random
from display.control.samplebase import SampleBase
from serv_logging.serv_logging import Logging


class Sparkle(SampleBase):
    #STOP_LOOP = False

    def __init__(self,  colour, brightness, input_stream, audio_spectrum, spectrum_analysis, display_spectrum, log_path, *args, **kwargs):
        super(Sparkle, self).__init__(colour, brightness, input_stream, audio_spectrum, spectrum_analysis, display_spectrum, *args, **kwargs)
        
        self.__logger = Logging.getInstance(Logging.DEB)
        self.__logger.open(log_path)
        
        self.__logger.write(Logging.DEB, "Starting Sparkle display")

    def clearBarRow(self, offset_canvas, bar, y, num_bars, bar_width, width, height):
        bar = num_bars + bar
        for x in range(bar * bar_width, (bar + 1) * bar_width):
            isMod = random.randint(1, 50) % 10.0
            if isMod == 0:
                continue
            
            offset_canvas.SetPixel(x, height - 1 - y, 0, 0, 0)
            offset_canvas.SetPixel((width - x) - 1, height - 1 - y, 0, 0, 0)

    def drawBarRow(self, offset_canvas, bar, y, r, g, b, num_bars, bar_width, width, height):
        bar = num_bars + bar
        for x in range(bar * bar_width, (bar + 1) * bar_width):
            isMod = random.randint(1, 20) % 5.0
            if isMod != 0:
                continue

            offset_canvas.SetPixel(x, height - 1 - y, r, g, b)
            offset_canvas.SetPixel((width - x) - 1, height - 1 - y, r, g, b)

    def drawLibra(self, matrix, offset_canvas, r, g, b, width, height):
        offset_canvas = matrix.SwapOnVSync(offset_canvas)
        for x in range(0, width):
            for y in range(0, height):
                offset_canvas.SetPixel(x, y, 0, 0, 0)
        offset_canvas = matrix.SwapOnVSync(offset_canvas)

        libraCoOrd = [(20, 9), (22, 12), (31, 10), (39, 3), (46, 11), (42, 23), (28, 26), (27, 28)]
        for x, y in libraCoOrd:
            offset_canvas.SetPixel(x, y, r, g, b)

        offset_canvas = matrix.SwapOnVSync(offset_canvas)
        
        time.sleep(0.3)
        
        for x in range(0, width):
            for y in range(0, height):
                offset_canvas.SetPixel(x, y, 0, 0, 0)
        offset_canvas = matrix.SwapOnVSync(offset_canvas)

    def run(self):
        super(Sparkle, self).run() 

        num_bars = 8
  
        bar_width = (self.width / 2) / num_bars

        try:
            didLibra = False
            while not SampleBase.STOP_LOOP:
                bar_heights = self.get_bar_heights(num_bars)

                if random.randint(0, 10000) == 28:
                    if self.colour == [0, 0, 0, 0]:
                        self.drawLibra(self.matrix, self.offset_canvas, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), self.width, self.height)
                    else:      
                        self.drawLibra(self.matrix, self.offset_canvas, self.colour[0], self.colour[1], self.colour[2], self.width, self.height)

                    didLibra = True
                    continue

                if didLibra == True:
                    for x in range(0, self.width):
                        for y in range(0, self.height):
                            self.offset_canvas.SetPixel(x, y, 0, 0, 0)
                    self.offset_canvas = self.matrix.SwapOnVSync(self.offset_canvas)

                for x in range(0, num_bars):
                    y = 0
                    for i in range(0, int(bar_heights[x])):
                        isEven = random.randint(1, 20) % 5.0
                        if isEven != 0:
                            continue

                        y = i

                        if self.colour == [0, 0, 0, 0]:
                            self.drawBarRow(self.offset_canvas, x, y, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), num_bars, bar_width, self.width, self.height)
                        else:
                            self.drawBarRow(self.offset_canvas, x, y, self.colour[0], self.colour[1], self.colour[2], num_bars, bar_width, self.width, self.height)
                        
                    for k in range(y, self.height):
                        y = k
                        self.clearBarRow(self.offset_canvas, x, y, num_bars, bar_width, self.width, self.height)
                        
                time.sleep(0.1)
                self.offset_canvas = self.matrix.SwapOnVSync(self.offset_canvas)
        except KeyboardInterrupt:
            SampleBase.stop()
            raise KeyboardInterrupt()
        except ValueError as e:
            logger.write(Logging.ERR, "Exception with displaying Sparkle style: " + str(e))
            SampleBase.stop()
            raise KeyboardInterrupt()
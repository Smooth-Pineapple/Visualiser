import math
import re
import time
import random
from display.control.samplebase import SampleBase
from serv_logging.serv_logging import Logging


class Block(SampleBase):
    #STOP_LOOP = False

    def __init__(self,  colour, brightness, input_stream, audio_spectrum, spectrum_analysis, display_spectrum, log_path, *args, **kwargs):
        super(Block, self).__init__(colour, brightness, input_stream, audio_spectrum, spectrum_analysis, display_spectrum, *args, **kwargs)
        
        self.__logger = Logging.getInstance(Logging.DEB)
        self.__logger.open(log_path)
        
        self.__logger.write(Logging.DEB, "Starting Block display")

    def rotate(self, x, y, angle):
        return {
            "new_x": x * math.cos(angle) - y * math.sin(angle),
            "new_y": x * math.sin(angle) + y * math.cos(angle)
        }

    def run(self):
        super(Block, self).run() 

        cent_x = self.width / 2
        cent_y = self.height / 2

        rotate_square = min(self.matrix.width, self.matrix.height) * 1.41
        min_rotate = cent_x - rotate_square / 2
        max_rotate = cent_x + rotate_square / 2

        deg_to_rad = 2 * 3.14159265 / 360
        rotation = 0

        try:
            while not SampleBase.STOP_LOOP:
                bar_heights = self.get_bar_heights(num_bars=16, HACK=True)

                xX = sum(bar_heights)
                if(xX > 0):
                    xX = xX / 415.0  
                else:
                    xX = 0.01

                display_square = min(self.width, self.height) * xX

                min_display = cent_x - display_square / 2
                max_display = cent_x + display_square / 2

                rotation += 5
                rotation %= 360

                for x in range(int(min_rotate), int(max_rotate)):
                    for y in range(int(min_rotate), int(max_rotate)):
                        ret = self.rotate(x - cent_x, y - cent_x, deg_to_rad * rotation)
                        rot_x = ret["new_x"]
                        rot_y = ret["new_y"]

                        if x >= min_display and x < max_display and y >= min_display and y < max_display:
                            if self.colour == [0, 0, 0, 0]:
                                self.offset_canvas.SetPixel(rot_x + cent_x, rot_y + cent_y, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                            else:
                                self.offset_canvas.SetPixel(rot_x + cent_x, rot_y + cent_y, self.colour[0], self.colour[1], self.colour[2]) 
                        else:
                            self.offset_canvas.SetPixel(rot_x + cent_x, rot_y + cent_y, 0, 0, 0)
                
                time.sleep(0.1)
                self.offset_canvas = self.matrix.SwapOnVSync(self.offset_canvas)
        except KeyboardInterrupt:
            SampleBase.stop()
            raise KeyboardInterrupt()
        except ValueError as e:
            logger.write(Logging.ERR, "Exception with displaying Block style: " + str(e))
            SampleBase.stop()
            raise KeyboardInterrupt()
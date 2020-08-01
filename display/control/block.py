import math
import re
import time

from display.control.samplebase import SampleBase
from serv_logging.serv_logging import Logging


class Block(SampleBase):
    STOP_LOOP = False

    def __init__(self,  colour, brightness, input_stream, audio_spectrum, spectrum_analysis, display_spectrum, log_path, *args, **kwargs):
        super(Block, self).__init__(*args, **kwargs)
        
        self.__logger = Logging.getInstance(Logging.DEB)
        self.__logger.open(log_path)
        
        self.__logger.write(Logging.DEB, "Starting Block display")

        Block.STOP_LOOP = False
        
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

    def rotate(self, x, y, angle):
        return {
            "new_x": x * math.cos(angle) - y * math.sin(angle),
            "new_y": x * math.sin(angle) + y * math.cos(angle)
        }

    def run(self):
        self.matrix.brightness = self.brightness

        width = self.matrix.width
        height = self.matrix.height

        cent_x = width / 2
        cent_y = height / 2

        rotate_square = min(self.matrix.width, self.matrix.height) * 1.41
        min_rotate = cent_x - rotate_square / 2
        max_rotate = cent_x + rotate_square / 2

        deg_to_rad = 2 * 3.14159265 / 360
        rotation = 0
        offset_canvas = self.matrix.CreateFrameCanvas()

        try:
            while not Block.STOP_LOOP:
                
                self.input_stream.tick_input_stream()
                self.audio_spectrum.set_audio_data(self.input_stream.get_input_data())
                self.audio_spectrum.data_to_spectrum()

                self.spectrum_analysis.set_spectrum(self.audio_spectrum.get_spectrum())

                bar_heights = self.display_spectrum.tick(self.spectrum_analysis.get_amplitude_array(16), 16)

                xX = sum(bar_heights)
                if(xX > 0):
                    xX = xX / 415.0  
                else:
                    xX = 0.01

                display_square = min(self.matrix.width, self.matrix.height) * xX

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
                            offset_canvas.SetPixel(rot_x + cent_x, rot_y + cent_y, self.colour[0], self.colour[1], self.colour[2])
                        else:
                            offset_canvas.SetPixel(rot_x + cent_x, rot_y + cent_y, 0, 0, 0)
                
                time.sleep(0.1)
                offset_canvas = self.matrix.SwapOnVSync(offset_canvas)
        except KeyboardInterrupt:
            Block.stop()
            raise KeyboardInterrupt()
        except ValueError as e:
            logger.write(Logging.ERR, "Exception with displaying Block style: " + str(e))
            Block.stop()
            raise KeyboardInterrupt()

    @staticmethod 
    def stop():
        Block.STOP_LOOP = True

"""
n = 100
radius = 1
angle = 0
step = 360/n
pi_over180 = 3.14159265 / 180.0

for _ in range(0, n):
    x = ((math.cos(angle*pi_over180) * xX*2) + 31) * 0.5
    y = ((math.sin(angle*pi_over180) * xX*2) + 31) * 0.5
    offset_canvas.SetPixel(x, y, self.colour[0], self.colour[1], self.colour[2])
    angle = angle + step

#time.sleep(1)
for x in range(0, width):
    for y in range(0, height):
        offset_canvas.SetPixel(x, y, 0, 0, 0)   
"""
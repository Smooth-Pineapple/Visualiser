import time
import math

from display.control.samplebase import SampleBase

class NetworkNotification(SampleBase):
    def __init__(self, have_ip, brightness, *args, **kwargs):
        super(NetworkNotification, self).__init__(None, brightness, None, None, None, None, *args, **kwargs)

        self.brightness = int(brightness)
        self.have_ip = have_ip

    def run(self):
        self.matrix.brightness = self.brightness

        quart_x = self.matrix.width / 4

        n = 100
        radius = 14
        angle = 0
        step = 360/n
        pi_over180 = 3.14159265 / 180.0

        offset_canvas = self.matrix.CreateFrameCanvas()

        t_end = time.time() + 5
        while time.time() < t_end:
            for _ in range(0, n):
                x = ((math.cos(angle * pi_over180) * radius * 2) + 31) * 0.5
                x = x + quart_x
                y = ((math.sin(angle * pi_over180) * radius * 2) + 31) * 0.5
                if self.have_ip is False:
                    offset_canvas.SetPixel(x, y, 255, 0, 0)
                else:
                    offset_canvas.SetPixel(x, y, 0, 255, 0)
                angle = angle + step

            offset_canvas = self.matrix.SwapOnVSync(offset_canvas)
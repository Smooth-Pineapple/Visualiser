import time
from display.control.samplebase import SampleBase

class NetworkNotification(SampleBase):
    def __init__(self, have_ip, brightness, *args, **kwargs):
        super(NetworkNotification, self).__init__(*args, **kwargs)

        self.brightness = int(brightness)
        self.have_ip = have_ip

    def run(self):
        cent_x = self.matrix.width / 2
        cent_y = self.matrix.height / 2

        quart_x = self.matrix.width / 4
        quart_y = self.matrix.height / 4


        offset_canvas = self.matrix.CreateFrameCanvas()

        t_end = time.time() + 5
        while time.time() < t_end:
                for x in range(cent_x - quart_x, cent_x + quart_x):
                    for y in range(cent_y - quart_y, cent_y + quart_y):
                        if self.have_ip is False:
                            offset_canvas.SetPixel(x, y, 255, 0, 0)
                        else:
                            offset_canvas.SetPixel(x, y, 0, 255, 0)

                offset_canvas = self.matrix.SwapOnVSync(offset_canvas)
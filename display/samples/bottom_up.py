from samplebase import SampleBase
import math
import time
import random
from datetime import datetime

class BottomUp(SampleBase):
    def __init__(self, *args, **kwargs):
        super(BottomUp, self).__init__(*args, **kwargs)

    def drawBarRow(self, offset_canvas, bar, y, r, g, b, bar_width, height):
        for x in range(bar * bar_width, (bar + 1) * bar_width):
            offset_canvas.SetPixel(x, height - 1 - y, r, g, b)

    def run(self):
        num_bars = 8

        width = self.matrix.width
        height = self.matrix.height
        self.matrix.brightness = 4

        bar_width = width / num_bars
        bar_heights = [None] * num_bars
        bar_means = [None] * num_bars
        bar_freqs = [None] * num_bars

        height_green = height * 4/12
        height_yellow = height * 8/12
        height_orange = height * 10/12
        height_red = height * 12/12

        num_means = 10 
        means = [1,2,3,4,5,6,7,8,16,32]
        for x in range(0, num_means):
            means[x] = height - means[x] * height / 8
        
        random.seed(datetime.now())
        for x in range(0, num_bars):
            bar_means[x] = random.randint(0, 10)
            bar_freqs[x] = 1 << random.randint(0, 3)

        offset_canvas = self.matrix.CreateFrameCanvas()

        t = 0
        while True:
            if t % 8 == 0:
                for x in range(0, num_bars):
                    bar_means[x] += random.randint(0, 2)
                    if bar_means[x] >= num_means:
                        bar_means[x] = num_means - 1
                    if bar_means[x] < 0:
                        bar_means[x] = 0
        
            t += 1
            for x in range(0, num_bars):
                bar_heights[x] = (height - means[bar_means[x]]) * math.sin(0.1 * t * bar_freqs[x]) + means[bar_means[x]]
                if bar_heights[x] < height / 8:
                    bar_heights[x] = random.randint(1, (height / 8))

            for x in range(0, num_bars):
                y = 0
                for i in range(0, int(bar_heights[x])):
                    y = i
                    
                    if y < height_green:
                        self.drawBarRow(offset_canvas, x, y, 0, 200, 0, bar_width, height)
                    elif y < height_yellow:
                        self.drawBarRow(offset_canvas, x, y, 150, 150, 0, bar_width, height)
                    elif y < height_orange:
                        self.drawBarRow(offset_canvas, x, y, 250, 100, 0, bar_width, height)
                    else:
                    
                        self.drawBarRow(offset_canvas, x, y, 200, 0, 0, bar_width, height)

                for k in range(y, height):
                    y = k
                    self.drawBarRow(offset_canvas, x, y, 0, 0, 0, bar_width, height)

            time.sleep(0.1)
            offset_canvas = self.matrix.SwapOnVSync(offset_canvas)

# Main function
if __name__ == "__main__":
    rotating_block_generator = BottomUp()
    if (not rotating_block_generator.process()):
        rotating_block_generator.print_help()

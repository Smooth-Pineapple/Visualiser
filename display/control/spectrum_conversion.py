import random
class SpectrumConversion:

    MAX_AMPLITUDE = 1

    freqArray = None
    moddedArray = None

    client = None

    thread = None

    def set_array(self, freqArray):
        self.freqArray = freqArray

    def convert_array(self, num_bars):
        self.moddedArray = []
        for i in range(num_bars):
            x1 = self.freqArray[i] - 0.9
            x2 = int(min(min(int(x1 * 32 / self.MAX_AMPLITUDE), 32) * 2.2, 32))
            self.moddedArray.append(x2)
        self.moddedArray[0] = int((self.moddedArray[0] + self.moddedArray[1]) / 2)

    def tick(self, freqArray, num_bars):
        self.set_array(freqArray)
        self.convert_array(num_bars)
        abs_silence = [-14, -59, -59, -59, -59, -59, -59, -59, -59, -59, -59, -59, -59, -59, -59, -61]
        #max_sound = [46, 91, 91, 91, 91, 91, 91, 91, 91, 91, 91, 91, 91, 91, 91, 93]
        max_sound = [60, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110]

        fitted_arr = []
        for x in range(0, len(self.moddedArray)):
            self.moddedArray[x] = abs(abs_silence[x] - self.moddedArray[x])

            fitted_arr.append(int((self.moddedArray[x] / float(max_sound[x])) * 32)) 
            if fitted_arr[x] >= max_sound[x]/2:
                fitted_arr[x] = fitted_arr[x] + random.randint(-5, 5)
 
        return fitted_arr
        
        

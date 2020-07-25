import numpy as np

class AudioSpectrum:

    data = None
    spec = None

    def set_audio_data(self, data):
        self.data = data

    def data_to_spectrum(self):
        b = np.fromstring(self.data, dtype=np.int16)
        s = np.fft.fft(b)/len(b)  
        s = s[range(int(len(b)/2))]

        f = [i for i in range(0, int(len(b)/2))]
        self.spec = (s, f)  

    def get_spectrum(self):
        return self.spec

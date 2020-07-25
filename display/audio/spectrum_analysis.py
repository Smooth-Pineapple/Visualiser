import math
import numpy as np


FREQ_BYTE_MIN = 0
FREQ_BYTE_MAX = 1024


class SpectrumAnalysis:

    min_freq = None
    max_freq = None
    freq_byte_interval = None

    spec = None


    def set_frequencies(self, min_freq, max_freq):
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.freq_byte_interval = (max_freq - min_freq) / (FREQ_BYTE_MAX - FREQ_BYTE_MIN)


    def set_spectrum(self, spec):
        self.spec = spec  
        if self.min_freq is None or self.max_freq is None:
            self.min_freq = FREQ_BYTE_MIN
            self.max_freq = FREQ_BYTE_MAX
            self.freq_byte_interval = 1


    def get_amplitude_in_range(self, freq1, freq2):
        lower = ((freq1 - self.min_freq) / self.freq_byte_interval) + FREQ_BYTE_MIN
        upper = ((freq2 - self.min_freq) / self.freq_byte_interval) + FREQ_BYTE_MIN
        return math.expm1(np.mean(abs(self.spec[0])[int(lower):int(upper):])/2)

    def get_amplitude_at_index(self, index, size):
        interval_size = (self.max_freq - self.min_freq)/size
        freq1 = self.min_freq + (index * interval_size)
        freq2 = self.min_freq + ( (index+1) * interval_size )
        return self.get_amplitude_in_range(freq1, freq2)

    def get_amplitude_array(self, size):
        s = []
        for i in range(size):
            s.append(self.get_amplitude_at_index(i, size))
        return s
